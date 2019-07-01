import logging
from typing import Optional, List

from google.protobuf.empty_pb2 import Empty

from .crypto import PrivateKey
from .util import create_deploy_data

from .pb.DeployService_pb2 import (DataAtNameQuery, ListeningNameDataResponse as Data)
from .pb.DeployService_pb2_grpc import (DeployServiceStub)
from .pb.ProposeService_pb2_grpc import (ProposeServiceStub)
from .pb.RhoTypes_pb2 import (Par, Expr, GUnforgeable, GDeployId)


class RClientException(Exception):

    def _init__(self, message):
        super().__init__(message)


class DataQueries:

    @staticmethod
    def public_names(names: List[str]) -> Par:
        exprs = [Expr(g_string=n) for n in names]
        return Par(exprs=exprs)

    @staticmethod
    def deploy_id(deploy_id: bytes) -> Par:
        g_deploy_id = GDeployId(sig=deploy_id)
        g_unforgeable = GUnforgeable(g_deploy_id_body=g_deploy_id)
        return Par(unforgeables=[g_unforgeable])


class RClient:

    def __init__(self, channel):
        self.channel = channel

    def _check_response(self, response):
        logging.debug('gRPC response: %s', str(response))
        if response.HasField('error'):
            raise RClientException('\n'.join(response.error.messages))

    def deploy(
        self,
        key: PrivateKey,
        term: str,
        phlo_price: int,
        phlo_limit: int,
        valid_after_block_no: int = -1,
        timestamp_millis: int = -1,
    ) -> bytes:
        deploy_data = create_deploy_data(
            key, term, phlo_price, phlo_limit, valid_after_block_no, timestamp_millis
        )
        stub = DeployServiceStub(self.channel)
        response = stub.DoDeploy(deploy_data)
        self._check_response(response)
        return deploy_data.sig

    def propose(self):
        stub = ProposeServiceStub(self.channel)
        response = stub.propose(Empty())
        self._check_response(response)

    def get_data_at_name(self, par: Par, depth: int = -1) -> Optional[Data]:
        query = DataAtNameQuery(depth=depth, name=par)
        stub = DeployServiceStub(self.channel)
        response = stub.listenForDataAtName(query)
        self._check_response(response)
        data = None
        wrapped = response.success.response
        if hasattr(wrapped, 'value'):
            data = Data.FromString(wrapped.value)
        return data

    def get_data_at_public_names(self, names: List[str], depth: int = -1) -> Optional[Data]:
        return self.get_data_at_name(DataQueries.public_names(names), depth)

    def get_data_at_deploy_id(self, deploy_id: bytes, depth: int = -1) -> Optional[Data]:
        return self.get_data_at_name(DataQueries.deploy_id(deploy_id), depth)
