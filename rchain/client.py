import logging
import re
from types import TracebackType
from typing import Iterable, List, Optional, Tuple, Type, TypeVar, Union

import grpc

from .crypto import PrivateKey
from .pb.DeployServiceCommon_pb2 import (
    BlockInfo, BlockQuery, BlocksQuery, DataAtNameQuery,
    ExploratoryDeployQuery, FindDeployQuery, IsFinalizedQuery,
    LastFinalizedBlockQuery, LightBlockInfo,
)
from .pb.DeployServiceV1_pb2 import (
    BlockInfoResponse, BlockResponse, DeployResponse,
    ExploratoryDeployResponse, ListeningNameDataPayload as Data,
    ListeningNameDataResponse, VisualizeBlocksResponse,
)
from .pb.DeployServiceV1_pb2_grpc import DeployServiceStub
from .pb.ProposeServiceCommon_pb2 import PrintUnmatchedSendsQuery
from .pb.ProposeServiceV1_pb2 import ProposeResponse
from .pb.ProposeServiceV1_pb2_grpc import ProposeServiceStub
from .pb.RhoTypes_pb2 import Expr, GDeployId, GUnforgeable, Par
from .util import create_deploy_data

GRPC_Response_T = Union[ProposeResponse,
                        DeployResponse,
                        ListeningNameDataResponse,
                        BlockResponse,
                        BlockInfoResponse,
                        ExploratoryDeployResponse,
                        VisualizeBlocksResponse]

GRPC_StreamResponse_T = Union[BlockInfoResponse, VisualizeBlocksResponse]
T = TypeVar("T")

propose_result_match = re.compile(r'Success! Block (?P<block_hash>[0-9a-f]+) created and added.')


class RClientException(Exception):

    def _init__(self, message: str) -> None:
        super().__init__(message)


class DataQueries:

    @staticmethod
    def public_names(names: List[str]) -> Par:
        exprs = [Expr(g_string=n) for n in names]
        return Par(exprs=exprs)

    @staticmethod
    def deploy_id(deploy_id: str) -> Par:
        g_deploy_id = GDeployId(sig=bytes.fromhex(deploy_id))
        g_unforgeable = GUnforgeable(g_deploy_id_body=g_deploy_id)
        return Par(unforgeables=[g_unforgeable])


class RClient:

    def __init__(self, host: str, port: int, grpc_options: Optional[Tuple[Tuple[str, str]]] = None):
        self.channel = grpc.insecure_channel("{}:{}".format(host, port), grpc_options)
        self._deploy_stub = DeployServiceStub(self.channel)

    def close(self) -> None:
        self.channel.close()

    def __enter__(self) -> 'RClient':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self.close()

    def _check_response(self, response: GRPC_Response_T) -> None:
        logging.debug('gRPC response: %s', str(response))
        if response.WhichOneof("message") == 'error':
            raise RClientException('\n'.join(response.error.messages))

    def _handle_stream(self, response: Iterable[GRPC_StreamResponse_T]) -> List[GRPC_StreamResponse_T]:
        result = []
        for resp in response:
            self._check_response(resp)
            result.append(resp)
        return result

    def deploy_with_vabn_filled(
            self,
            key: PrivateKey,
            term: str,
            phlo_price: int,
            phlo_limit: int,
            timestamp_millis: int = -1
    ) -> str:
        latest_blocks = self.show_blocks(1)
        # when the genesis block is not ready, it would be empty in show_blocks
        # it could return more than 1 block when there are multiple blocks at the same height
        assert len(latest_blocks) >= 1, "No latest block found"
        latest_block = latest_blocks[0]
        latest_block_num = latest_block.blockNumber
        return self.deploy(key, term, phlo_price, phlo_limit, latest_block_num, timestamp_millis)

    def exploratory_deploy(self, term: str) -> List[Par]:
        exploratory_query = ExploratoryDeployQuery(term=term)
        response = self._deploy_stub.exploratoryDeploy(exploratory_query)
        self._check_response(response)
        return list(response.result.postBlockData)

    def deploy(
            self,
            key: PrivateKey,
            term: str,
            phlo_price: int,
            phlo_limit: int,
            valid_after_block_no: int = -1,
            timestamp_millis: int = -1
    ) -> str:
        deploy_data = create_deploy_data(
            key, term, phlo_price, phlo_limit, valid_after_block_no, timestamp_millis
        )
        response = self._deploy_stub.doDeploy(deploy_data)
        self._check_response(response)
        # sig of deploy data is deployId
        return deploy_data.sig.hex()

    def show_block(self, block_hash: str) -> BlockInfo:
        block_query = BlockQuery(hash=block_hash)
        response = self._deploy_stub.getBlock(block_query)
        self._check_response(response)
        return response.blockInfo

    def show_blocks(self, depth: int = 1) -> List[LightBlockInfo]:
        blocks_query = BlocksQuery(depth=depth)
        response = self._deploy_stub.getBlocks(blocks_query)
        result = self._handle_stream(response)
        return list(map(lambda x: x.blockInfo, result))  # type: ignore

    def find_deploy(self, deploy_id: str) -> LightBlockInfo:
        find_deploy_query = FindDeployQuery(deployId=bytes.fromhex(deploy_id))
        response = self._deploy_stub.findDeploy(find_deploy_query)
        self._check_response(response)
        return response.blockInfo

    def last_finalized_block(self) -> BlockInfo:
        last_finalized_query = LastFinalizedBlockQuery()
        response = self._deploy_stub.lastFinalizedBlock(last_finalized_query)
        self._check_response(response)
        return response.blockInfo

    def is_finalized(self, block_hash: str) -> bool:
        is_finalized_query = IsFinalizedQuery(hash=block_hash)
        response = self._deploy_stub.isFinalized(is_finalized_query)
        self._check_response(response)
        return response.isFinalized

    def propose(self) -> str:
        stub = ProposeServiceStub(self.channel)
        response: ProposeResponse = stub.propose(PrintUnmatchedSendsQuery(printUnmatchedSends=False))
        self._check_response(response)
        match_result = propose_result_match.match(response.result)
        assert match_result is not None
        return match_result.group("block_hash")

    def get_data_at_name(self, par: Par, depth: int = -1) -> Data:
        query = DataAtNameQuery(depth=depth, name=par)
        response = self._deploy_stub.listenForDataAtName(query)
        self._check_response(response)
        wrapped = response.payload
        return Data.FromString(wrapped.SerializeToString())

    def get_data_at_public_names(self, names: List[str], depth: int = -1) -> Optional[Data]:
        return self.get_data_at_name(DataQueries.public_names(names), depth)

    def get_data_at_deploy_id(self, deploy_id: str, depth: int = -1) -> Optional[Data]:
        return self.get_data_at_name(DataQueries.deploy_id(deploy_id), depth)
