import time

from .crypto import PrivateKey
from .pb.CasperMessage_pb2 import DeployDataProto


def sign_deploy_data(key: PrivateKey, data: DeployDataProto) -> bytes:
    signed_data = DeployDataProto()
    signed_data.CopyFrom(data)
    signed_data.ClearField('deployer')
    signed_data.ClearField('sig')
    signed_data.ClearField('sigAlgorithm')
    return key.sign(signed_data.SerializeToString())


def create_deploy_data(
    key: PrivateKey,
    term: str,
    phlo_price: int,
    phlo_limit: int,
    valid_after_block_no: int = -1,
    timestamp_millis: int = -1,
) -> DeployDataProto:
    if timestamp_millis < 0:
        timestamp_millis = int(time.time() * 1000)
    data = DeployDataProto(
        deployer=key.get_public_key().to_bytes(),
        term=term,
        phloPrice=phlo_price,
        phloLimit=phlo_limit,
        validAfterBlockNumber=valid_after_block_no,
        timestamp=timestamp_millis,
        sigAlgorithm='secp256k1',
    )
    data.sig = sign_deploy_data(key, data)
    return data
