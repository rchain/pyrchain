import time
from typing import Type

from ecdsa import SigningKey

from .crypto import PrivateKey
from .pb.CasperMessage_pb2 import DeployData


def sign_deploy_data(key: PrivateKey, data: DeployData) -> bytes:
    signed_data = DeployData()
    signed_data.CopyFrom(data)
    signed_data.ClearField('deployer')
    signed_data.ClearField('sig')
    signed_data.ClearField('sigAlgorithm')
    return key.sign(signed_data.SerializeToString())


def create_deploy_data(key: PrivateKey, term: str, timestamp: int = -1) -> DeployData:
    if timestamp < 0:
        timestamp = int(time.time())
    data = DeployData(
        deployer=key.get_public_key().to_bytes(),
        term=term,
        timestamp=timestamp,
        sigAlgorithm='secp256k1',
    )
    data.sig = sign_deploy_data(key, data)
    return data
