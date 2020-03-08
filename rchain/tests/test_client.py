from concurrent import futures
from contextlib import contextmanager
from typing import Generator, Tuple, Union

import grpc
import pytest
from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.pb.CasperMessage_pb2 import DeployDataProto
from rchain.pb.DeployServiceCommon_pb2 import (
    BlockInfo, BlockQuery, BlocksQuery, BondInfo, DeployInfo, FindDeployQuery,
    IsFinalizedQuery, LastFinalizedBlockQuery, LightBlockInfo,
)
from rchain.pb.DeployServiceV1_pb2 import (
    BlockInfoResponse, BlockResponse, DeployResponse, FindDeployResponse,
    IsFinalizedResponse, LastFinalizedBlockResponse,
)
from rchain.pb.DeployServiceV1_pb2_grpc import (
    DeployServiceServicer, add_DeployServiceServicer_to_server,
)
from rchain.pb.ProposeServiceCommon_pb2 import PrintUnmatchedSendsQuery
from rchain.pb.ProposeServiceV1_pb2 import ProposeResponse
from rchain.pb.ProposeServiceV1_pb2_grpc import (
    ProposeServiceServicer, add_ProposeServiceServicer_to_server,
)
from rchain.util import create_deploy_data, verify_deploy_data

key = PrivateKey.generate()


@contextmanager
def deploy_service(deploy_service: Union[DeployServiceServicer, ProposeServiceServicer]) -> Generator[
    Tuple[grpc.Server, int], None, None]:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    if isinstance(deploy_service, DeployServiceServicer):
        add_DeployServiceServicer_to_server(deploy_service, server)
    if isinstance(deploy_service, ProposeServiceServicer):
        add_ProposeServiceServicer_to_server(deploy_service, server)
    port = server.add_insecure_port("0.0.0.0:9766")
    assert port != 0
    server.start()
    yield server, port
    server.stop(0)


TEST_HOST = '127.0.0.1'


@pytest.mark.parametrize("key,terms,phlo_price,phlo_limit,valid_after_block_no,timestamp_millis", [
    (key, "@0!(2)", 1, 10000, 1, 1000),
    (key, "@0!(2) | @1!(1)", 1, 10000, 10, 1000),
    (key, "@0!(2)", 10, 200000, 10, 3000),
])
def test_client_deploy(key: PrivateKey, terms: str, phlo_price: int, phlo_limit: int, valid_after_block_no: int,
                       timestamp_millis: int) -> None:
    class DummyDeploySerivce(DeployServiceServicer):
        def doDeploy(self, request: DeployDataProto, context: grpc.ServicerContext) -> DeployResponse:
            return DeployResponse(result=request.sig.hex())

    with deploy_service(DummyDeploySerivce()) as (server, port), \
            RClient(TEST_HOST, port) as client:
        ret = client.deploy(key, terms, phlo_price, phlo_limit, valid_after_block_no, timestamp_millis)
        assert verify_deploy_data(key.get_public_key(), bytes.fromhex(ret),
                                  create_deploy_data(key, terms, phlo_price, phlo_limit, valid_after_block_no,
                                                     timestamp_millis))


def test_client_show_block() -> None:
    request_block_hash = "asdasdasdasd"
    sender = "a"
    seqNum = 1
    sig = "sig"
    sigAlgorithm = "sigal"
    shardId = "rchain"
    extraBytes = b"extraBytes"
    version = 1
    timestamp = 10000000
    headerExtraBytes = b"headerExtraBytes"
    parentsHashList = ["abc"]
    blockNumber = 1
    preStateHash = "preStateHash"
    postStateHash = "postStateHash"
    bodyExtraBytes = b"bodyExtraBytes"
    bond = BondInfo(validator="a", stake=100)
    blockSize = "100"
    deployCount = 1
    faultTolerance = 0.2
    deploy = DeployInfo(
        deployer="a",
        term="1",
        timestamp=timestamp,
        sig=sig,
        sigAlgorithm=sigAlgorithm,
        phloPrice=1,
        phloLimit=100000,
        validAfterBlockNumber=1,
        cost=100,
        errored=False,
        systemDeployError="none"

    )

    class DummyDeploySerivce(DeployServiceServicer):
        def getBlock(self, request: BlockQuery, context: grpc.ServicerContext) -> BlockResponse:
            return BlockResponse(blockInfo=BlockInfo(blockInfo=LightBlockInfo(
                blockHash=request_block_hash,
                sender=sender, seqNum=seqNum, sig=sig, sigAlgorithm=sigAlgorithm, shardId=shardId,
                extraBytes=extraBytes, version=version, timestamp=timestamp, headerExtraBytes=headerExtraBytes,
                parentsHashList=parentsHashList, blockNumber=blockNumber, preStateHash=preStateHash,
                postStateHash=postStateHash, bodyExtraBytes=bodyExtraBytes, bonds=[bond], blockSize=blockSize,
                deployCount=deployCount, faultTolerance=faultTolerance
            ), deploys=[deploy]))

    with deploy_service(DummyDeploySerivce()) as (server, port), \
            RClient(TEST_HOST, port) as client:
        block = client.show_block(request_block_hash)
        block_info = block.blockInfo
        assert block_info.blockHash == request_block_hash
        assert block_info.sender == sender
        assert block_info.seqNum == seqNum
        assert block_info.sig == sig
        assert block_info.sigAlgorithm == sigAlgorithm
        assert block_info.shardId == shardId
        assert block_info.extraBytes == extraBytes
        assert block_info.version == version
        assert block_info.timestamp == timestamp
        assert block_info.headerExtraBytes == headerExtraBytes
        assert block_info.parentsHashList == parentsHashList
        assert block_info.blockNumber == blockNumber
        assert block_info.preStateHash == preStateHash
        assert block_info.postStateHash == postStateHash
        assert block_info.bodyExtraBytes == bodyExtraBytes
        assert block_info.blockSize == blockSize
        assert block_info.deployCount == deployCount
        assert pytest.approx(block_info.faultTolerance, faultTolerance)
        bond_info = block_info.bonds[0]
        assert bond_info.validator == bond.validator
        assert bond_info.stake == bond.stake

        deploy_info = block.deploys[0]
        assert deploy_info.deployer == deploy.deployer
        assert deploy_info.term == deploy.term
        assert deploy_info.timestamp == deploy.timestamp
        assert deploy_info.sig == deploy.sig
        assert deploy_info.sigAlgorithm == deploy.sigAlgorithm
        assert deploy_info.phloPrice == deploy.phloPrice
        assert deploy_info.phloLimit == deploy.phloLimit
        assert deploy_info.validAfterBlockNumber == deploy.validAfterBlockNumber
        assert deploy_info.cost == deploy.cost
        assert deploy_info.errored == deploy.errored
        assert deploy_info.systemDeployError == deploy.systemDeployError


def test_client_show_blocks() -> None:
    request_block_hash = "asdasdasdasd"
    sender = "a"
    seqNum = 1
    sig = "sig"
    sigAlgorithm = "sigal"
    shardId = "rchain"
    extraBytes = b"extraBytes"
    version = 1
    timestamp = 10000000
    headerExtraBytes = b"headerExtraBytes"
    parentsHashList = ["abc"]
    blockNumber = 1
    preStateHash = "preStateHash"
    postStateHash = "postStateHash"
    bodyExtraBytes = b"bodyExtraBytes"
    bond = BondInfo(validator="a", stake=100)
    blockSize = "100"
    deployCount = 1
    faultTolerance = 0.2

    class DummyDeploySerivce(DeployServiceServicer):
        def getBlocks(self, request: BlocksQuery, context: grpc.ServicerContext) -> Generator[
            BlockInfoResponse, None, None]:
            yield BlockInfoResponse(blockInfo=LightBlockInfo(
                blockHash=request_block_hash,
                sender=sender, seqNum=seqNum, sig=sig, sigAlgorithm=sigAlgorithm, shardId=shardId,
                extraBytes=extraBytes, version=version, timestamp=timestamp, headerExtraBytes=headerExtraBytes,
                parentsHashList=parentsHashList, blockNumber=blockNumber, preStateHash=preStateHash,
                postStateHash=postStateHash, bodyExtraBytes=bodyExtraBytes, bonds=[bond], blockSize=blockSize,
                deployCount=deployCount, faultTolerance=faultTolerance))

    with deploy_service(DummyDeploySerivce()) as (server, port), \
            RClient(TEST_HOST, port) as client:
        blocks = client.show_blocks()
        block_info = blocks[0]
        assert len(blocks) == 1
        assert block_info.blockHash == request_block_hash
        assert block_info.sender == sender
        assert block_info.seqNum == seqNum
        assert block_info.sig == sig
        assert block_info.sigAlgorithm == sigAlgorithm
        assert block_info.shardId == shardId
        assert block_info.extraBytes == extraBytes
        assert block_info.version == version
        assert block_info.timestamp == timestamp
        assert block_info.headerExtraBytes == headerExtraBytes
        assert block_info.parentsHashList == parentsHashList
        assert block_info.blockNumber == blockNumber
        assert block_info.preStateHash == preStateHash
        assert block_info.postStateHash == postStateHash
        assert block_info.bodyExtraBytes == bodyExtraBytes
        assert block_info.blockSize == blockSize
        assert block_info.deployCount == deployCount
        assert pytest.approx(block_info.faultTolerance, faultTolerance)
        bond_info = block_info.bonds[0]
        assert bond_info.validator == bond.validator
        assert bond_info.stake == bond.stake


def test_client_propose() -> None:
    block_hash = "abcabcabc"

    class DummyProposeService(ProposeServiceServicer):
        def propose(self, request: PrintUnmatchedSendsQuery, context: grpc.ServicerContext) -> ProposeResponse:
            return ProposeResponse(result="Success! Block {} created and added.".format(block_hash))

    with deploy_service(DummyProposeService()) as (server, port), \
            RClient(TEST_HOST, port) as client:
        hash = client.propose()
        assert hash == block_hash


def test_client_find_deploy() -> None:
    deploy_id = '61e594124ca6af84a5468d98b34a4f3431ef39c54c6cf07fe6fbf8b079ef64f6'

    class DummyDeployService(DeployServiceServicer):
        def findDeploy(self, request: FindDeployQuery, context: grpc.ServicerContext) -> FindDeployResponse:
            return FindDeployResponse(blockInfo=LightBlockInfo())

    with deploy_service(DummyDeployService()) as (server, port), \
            RClient(TEST_HOST, port) as client:
        assert client.find_deploy(deploy_id)


def test_client_last_finalized_block() -> None:
    class DummyDeployService(DeployServiceServicer):
        def lastFinalizedBlock(self, request: LastFinalizedBlockQuery,
                               context: grpc.ServicerContext) -> LastFinalizedBlockResponse:
            return LastFinalizedBlockResponse(blockInfo=BlockInfo())

    with deploy_service(DummyDeployService()) as (server, port), \
            RClient(TEST_HOST, port) as client:
        assert client.last_finalized_block()


def test_client_is_finalized_block() -> None:
    class DummyDeployService(DeployServiceServicer):
        def isFinalized(self, request: IsFinalizedQuery, context: grpc.ServicerContext) -> IsFinalizedResponse:
            return IsFinalizedResponse(isFinalized=True)

    with deploy_service(DummyDeployService()) as (server, port), \
            RClient(TEST_HOST, port) as client:
        assert client.is_finalized('asd')
