import logging
from pprint import pprint

import grpc

import DeployService_pb2
import DeployService_pb2_grpc

def run():
    with grpc.insecure_channel('node4.devnet.rchain-dev.tk:40401') as channel:
        stub = DeployService_pb2_grpc.DeployServiceStub(channel)
        response = stub.getBlocks(DeployService_pb2.BlocksQuery(depth=1))
        for x in response:
            pprint(type(x.success.response.value))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
