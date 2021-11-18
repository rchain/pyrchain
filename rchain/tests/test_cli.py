import grpc
import pytest
from click.testing import CliRunner

from rchain.__main__ import cli
from rchain.crypto import PrivateKey
from rchain.pb.CasperMessage_pb2 import DeployDataProto
from rchain.pb.DeployServiceV1_pb2 import DeployResponse
from rchain.pb.DeployServiceV1_pb2_grpc import DeployServiceServicer
from rchain.util import verify_deploy_data

from .test_client import deploy_service

key = PrivateKey.generate()


def test_get_rev_from_private():
    runner = CliRunner()
    result = runner.invoke(cli, ['get-rev-addr', '--input-type', 'private', '--input',
                                 "1000000000000000000000000000000000000000000000000000000000000000"])
    assert result.exit_code == 0
    assert result.output == '1111cnoFDAa7GubxBMHpPLbbediPegnjSdZwNjxg9oqYvSvSmfqQL\n'


def test_get_rev_from_pub():
    runner = CliRunner()
    result = runner.invoke(cli, ['get-rev-addr', '--input-type', 'public', '--input',
                                 "0408ea9666139527a8c1dd94ce4f071fd23c8b350c5a4bb33748c4ba111faccae0620efabbc8ee2782e24e7c0cfb95c5d735b783be9cf0f8e955af34a30e62b945"])
    assert result.exit_code == 0
    assert result.output == '1111cnoFDAa7GubxBMHpPLbbediPegnjSdZwNjxg9oqYvSvSmfqQL\n'


def test_get_rev_from_eth():
    runner = CliRunner()
    result = runner.invoke(cli, ['get-rev-addr', '--input-type', 'eth', '--input',
                                 "7b2419e0ee0bd034f7bf24874c12512acac6e21c"])
    assert result.exit_code == 0
    assert result.output == '1111cnoFDAa7GubxBMHpPLbbediPegnjSdZwNjxg9oqYvSvSmfqQL\n'


def test_get_rev_from_err():
    runner = CliRunner()
    result = runner.invoke(cli, ['get-rev-addr', '--input-type', 'eth', '--input',
                                 "7b2419e0ee0bd034f7bf24874c12512acac6e1c"])
    assert result.exit_code == 1
    assert result.output == ''


@pytest.mark.parametrize("key,terms,phlo_price,phlo_limit,valid_after_block_no,timestamp_millis", [
    (key, "@0!(2)", 1, 10000, 1, 1000),
    (key, "@0!(2) | @1!(1)", 1, 10000, 10, 1000),
    (key, "@0!(2)", 10, 200000, 10, 3000),
])
def test_sign_deploy(key: PrivateKey, terms: str, phlo_price: int, phlo_limit: int, valid_after_block_no: int,
                     timestamp_millis: int):
    runner = CliRunner()
    result = runner.invoke(cli, ['sign-deploy', '--private-key', key.to_hex(),
                                 '--term', terms,
                                 "--phlo-price", phlo_price,
                                 "--phlo-limit", phlo_limit,
                                 "--valid-after-block-number", valid_after_block_no,
                                 "--timestamp", timestamp_millis,
                                 "--sig-algorithm", "secp256k1"
                                 ])
    assert result.exit_code == 0
    sig = result.output.strip()

    data = DeployDataProto(
        deployer=key.get_public_key().to_bytes(),
        term=terms,
        phloPrice=phlo_price,
        phloLimit=phlo_limit,
        validAfterBlockNumber=valid_after_block_no,
        timestamp=timestamp_millis,
        sigAlgorithm='secp256k1',
    )
    assert verify_deploy_data(key.get_public_key(), bytes.fromhex(sig), data)


@pytest.mark.parametrize("key,terms,phlo_price,phlo_limit,valid_after_block_no,timestamp_millis", [
    (key, "@0!(2)", 1, 10000, 1, 1000),
    (key, "@0!(2) | @1!(1)", 1, 10000, 10, 1000),
    (key, "@0!(2)", 10, 200000, 10, 3000),
])
def test_submit_deploy(key: PrivateKey, terms: str, phlo_price: int, phlo_limit: int, valid_after_block_no: int,
                       timestamp_millis: int):
    class DummyDeploySerivce(DeployServiceServicer):
        def doDeploy(self, request: DeployDataProto, context: grpc.ServicerContext) -> DeployResponse:
            return DeployResponse(result=request.sig.hex())

    with deploy_service(DummyDeploySerivce()) as (server, port):
        runner = CliRunner()
        result = runner.invoke(cli, ['submit-deploy', '--deployer', key.get_public_key().to_hex(),
                                     '--term', terms,
                                     "--phlo-price", phlo_price,
                                     "--phlo-limit", phlo_limit,
                                     "--valid-after-block-number", valid_after_block_no,
                                     "--timestamp", timestamp_millis,
                                     "--sig-algorithm", "secp256k1",
                                     "--sig", "1111",
                                     "--host", 'localhost',
                                     "--port", port
                                     ])
        assert result.exit_code == 0
