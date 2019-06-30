import logging
from pprint import pprint

import grpc

from rchain.crypto import PrivateKey
from rchain.client import RClient


def run():
    key = PrivateKey.generate()
    with grpc.insecure_channel('172.27.0.2:40401') as channel:
        term = '@"foo"!("Hi")'
        client = RClient(channel)
        client.deploy(key, term)
        client.propose()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
