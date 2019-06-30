import logging

from google.protobuf.empty_pb2 import Empty

from .crypto import PrivateKey
from .util import create_deploy_data
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

    def deploy(
        self,
        key: PrivateKey,
        term: str,
        phlo_price: int,
        phlo_limit: int,
        valid_after_block_no: int = -1,
        timestamp_millis: int = -1,
    ):
        deploy_data = create_deploy_data(
            key, term, phlo_price, phlo_limit, valid_after_block_no, timestamp_millis
        )
        stub = DeployService_pb2_grpc.DeployServiceStub(self.channel)
        response = stub.DoDeploy(deploy_data)
        self._check_response(response)

    def propose(self):
        stub = ProposeService_pb2_grpc.ProposeServiceStub(self.channel)
        response = stub.propose(Empty())
        self._check_response(response)
