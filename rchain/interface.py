from abc import ABC

from .crypto import PrivateKey

# from .data_types import BlockInfo, LightBlockInfo


class APIClient(ABC):
    def deploy(self, key: PrivateKey,
               term: str,
               phlo_price: int,
               phlo_limit: int,
               valid_after_block_no: int,
               timestamp_millis: int) -> str:
        raise NotImplementedError()

    def deploy_with_vabn_filled(self, key: PrivateKey,
                                term: str,
                                phlo_price: int,
                                phlo_limit: int,
                                timestamp_millis: int) -> str:
        raise NotImplementedError()

    def show_block(self, block_hash: str):
        raise NotImplementedError()

    def show_blocks(self, depth: int):
        raise NotImplementedError()

    def propose(self) -> str:
        raise NotImplementedError()

    def listen_for_data_at_name(self):
        raise NotImplementedError()
