import logging
import hashlib
from pprint import pprint

from ecdsa import SigningKey
from ecdsa.curves import SECP256k1
from ecdsa.util import sigencode_der_canonize

import grpc

from rchain.pb import DeployService_pb2_grpc

from rchain.crypto import PrivateKey, PublicKey
from rchain.rpc import create_deploy_data



def run():
    with grpc.insecure_channel('172.27.0.2:40401') as channel:
        stub = DeployService_pb2_grpc.DeployServiceStub(channel)

        term = '@"foo"!("Hi")'
        key = PrivateKey.generate()
        deploy_data = create_deploy_data(key, term, 1)

        response = stub.DoDeploy(deploy_data)
        print(response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
