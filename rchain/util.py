import time

from .crypto import PrivateKey, PublicKey
from .pb.CasperMessage_pb2 import DeployDataProto


def _gen_deploy_sig_content(data: DeployDataProto) -> bytes:
    signed_data = DeployDataProto()
    signed_data.term = data.term
    signed_data.timestamp = data.timestamp
    signed_data.phloLimit = data.phloLimit
    signed_data.phloPrice = data.phloPrice
    signed_data.validAfterBlockNumber = data.validAfterBlockNumber
    return signed_data.SerializeToString()


def sign_deploy_data(key: PrivateKey, data: DeployDataProto) -> bytes:
    return key.sign(_gen_deploy_sig_content(data))


def verify_deploy_data(key: PublicKey, sig: bytes, data: DeployDataProto) -> bool:
    return key.verify(sig, _gen_deploy_sig_content(data))


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
