import logging

from google.protobuf.empty_pb2 import Empty

from rchain.crypto import PrivateKey
from rchain.util import create_deploy_data
from .pb import DeployService_pb2_grpc, ProposeService_pb2_grpc


class RClientException(Exception):

    def _init__(self, message):
        super().__init__(message)


class RClient:

    def __init__(self, channel):
        self.channel = channel

    def _check_response(self, response):
        logging.debug('gRPC response: %s', str(response))
        if response.HasField('error'):
            raise RClientException('\n'.join(response.error.messages))

    def deploy(self, key: PrivateKey, term: str, timestamp: int = -1):
        deploy_data = create_deploy_data(key, term, timestamp)
        stub = DeployService_pb2_grpc.DeployServiceStub(self.channel)
        response = stub.DoDeploy(deploy_data)
        self._check_response(response)

    def propose(self):
        stub = ProposeService_pb2_grpc.ProposeServiceStub(self.channel)
        response = stub.propose(Empty())
        self._check_response(response)
