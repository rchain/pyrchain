from typing import (
    Optional,
    Mapping,
)

import string
import time

from ..client import RClient
from ..crypto import PrivateKey
from ..pb.DeployServiceV1_pb2 import (ListeningNameDataPayload as Data)


CREATE_VAULT_RHO_TPL = """
new rl(`rho:registry:lookup`), RevVaultCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreateVault", "$addr", Nil)
  }
}
"""


BOND_RHO_TPL = """
new retCh, PoSCh, rl(`rho:registry:lookup`), stdout(`rho:io:stdout`) in {
  stdout!("About to lookup pos contract.") |
  rl!(`rho:rchain:pos`, *PoSCh) |
  for(@(_, PoS) <- PoSCh) {
    stdout!("About to bond") |
    @PoS!("bond", $amount, *retCh) |
    for ( @(_, message) <- retCh) {
      stdout!(message)
    }
  }
}
"""


GET_BALANCE_RHO_TPL = """
new rl(`rho:registry:lookup`), deployId(`rho:rchain:deployId`), RevVaultCh, vaultCh, balanceCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreate", "$addr", *vaultCh) |
    for (@(true, vault) <- vaultCh) {
      @vault!("balance", *balanceCh) |
      for (@balance <- balanceCh) {
        deployId!(balance)
      }
    }
  }
}
"""


TRANSFER_RHO_TPL = """
new rl(`rho:registry:lookup`), RevVaultCh, vaultCh, revVaultKeyCh, resultCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreate", "$from", *vaultCh) |
    @RevVault!("deployerAuthKey", *revVaultKeyCh) |
    for (@(true, vault) <- vaultCh; key <- revVaultKeyCh) {
      @vault!("transfer", "$to", $amount, *key, *resultCh) |
      for (_ <- resultCh) { Nil }
    }
  }
}
"""


class VaultAPIException(Exception):

    def _init__(self, message):
        super().__init__(message)



def render_contract_template(template: str, substitutions: Mapping[str, str]) -> str:
    return string.Template(template).substitute(substitutions)



class VaultAPI:

    def __init__(self, client: RClient, key: PrivateKey):
        self.client = client
        self.key = key

    def _get_addr(self, addr: Optional[str]) -> str:
        return addr or self.key.get_public_key().get_rev_address()

    def _deploy(self, contract: str) -> bytes:
        timestamp_mill = int(time.time() * 1000)
        return self.client.deploy_with_vabn_filled(self.key, contract, 1, 1000000000, timestamp_mill)

    def deploy_create_vault(self, addr: Optional[str] = None) -> bytes:
        contract = render_contract_template(
            CREATE_VAULT_RHO_TPL,
            {'addr': self._get_addr(addr)},
        )
        return self._deploy(contract)

    def create_vault(self) -> None:
        self.deploy_create_vault()
        self.client.propose()

    def deploy_bond(self, amount) -> bytes:
        contract = render_contract_template(BOND_RHO_TPL, {'amount': amount})
        return self._deploy(contract)

    def bond(self, amount = 100) -> None:
        self.deploy_bond(amount)
        self.client.propose()

    def deploy_get_balance(self, addr: Optional[str] = None) -> bytes:
        contract = render_contract_template(
            GET_BALANCE_RHO_TPL,
            {'addr': self._get_addr(addr)},
        )
        return self._deploy(contract)

    def get_balance_from_data(self, data: Data) -> int:
        return data.blockInfo[0].postBlockData[0].exprs[0].g_int

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
        contract = render_contract_template(
            TRANSFER_RHO_TPL, {
                'from': self._get_addr(from_addr),
                'to': to_addr,
                'amount': str(amount)
            }
        )
        return self._deploy(contract)

    def transfer(self, from_addr: Optional[str], to_addr: str, amount: int) -> None:
        self.deploy_transfer(from_addr, to_addr, amount)
        self.client.propose()
