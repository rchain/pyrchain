from typing import Optional

from ..client import RClient
from ..crypto import PrivateKey
from ..util import load_contract
from ..pb.DeployService_pb2 import (ListeningNameDataResponse as Data)


class VaultAPIException(Exception):

    def _init__(self, message):
        super().__init__(message)


class VaultAPI:

    def __init__(self, client: RClient, key: PrivateKey):
        self.client = client
        self.key = key

    def _get_addr(self, addr: Optional[str]) -> str:
        return addr or self.key.get_public_key().get_address()

    def _deploy(self, filename: str, args: dict) -> bytes:
        return self.client.deploy(
            self.key, load_contract(__name__, filename, args), 1, 1000000000
        )

    def deploy_create_vault(self, addr: Optional[str] = None) -> bytes:
        return self._deploy('create_vault.rho.tpl', {'addr': self._get_addr(addr)})

    def create_vault(self, addr: Optional[str] = None) -> None:
        self.deploy_create_vault()
        self.client.propose()

    def deploy_create_genesis_vault(self, addr: Optional[str], balance: int) -> bytes:
        return self._deploy(
            'create_genesis_vault.rho.tpl', {
                'addr': self._get_addr(addr),
                'balance': balance
            }
        )

    def create_genesis_vault(self, addr: Optional[str], balance: int) -> None:
        self.deploy_create_genesis_vault(addr, balance)
        self.client.propose()

    def deploy_get_balance(self, addr: Optional[str] = None) -> bytes:
        return self._deploy('get_balance.rho.tpl', {
            'addr': self._get_addr(addr),
        })

    def get_balance_from_data(self, data: Data) -> int:
        return data.blockResults[0].postBlockData[0].exprs[0].g_int

    def get_balance_from_deploy_id(self, deploy_id: bytes, depth: int = -1) -> int:
        data = self.client.get_data_at_deploy_id(deploy_id, depth=depth)
        if not data:
            raise VaultAPIException('No data at deployId')
        return self.get_balance_from_data(data)

    def get_balance(self, addr: Optional[str] = None, depth: int = -1) -> int:
        deploy_id = self.deploy_get_balance(addr)
        self.client.propose()
        return self.get_balance_from_deploy_id(deploy_id, depth=depth)

    def deploy_transfer(
        self, from_addr: Optional[str], to_addr: str, amount: int
    ) -> bytes:
        return self._deploy(
            'transfer.rho.tpl', {
                'from': self._get_addr(from_addr),
                'to': to_addr,
                'amount': amount
            }
        )

    def transfer(self, from_addr: Optional[str], to_addr: str, amount: int) -> bytes:
        self.deploy_transfer(from_addr, to_addr, amount)
        self.client.propose()
