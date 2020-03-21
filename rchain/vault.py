import string
import time
from typing import Mapping

from .client import RClient
from .crypto import PrivateKey

CREATE_VAULT_RHO_TPL = """
new rl(`rho:registry:lookup`), RevVaultCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreateVault", "$addr", Nil)
  }
}
"""

GET_BALANCE_RHO_TPL = """
new return, rl(`rho:registry:lookup`), RevVaultCh, vaultCh, balanceCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreate", "$addr", *vaultCh) |
    for (@(true, vault) <- vaultCh) {
      @vault!("balance", *balanceCh) |
      for (@balance <- balanceCh) {
        return!(balance)
      }
    }
  }
}
"""

TRANSFER_RHO_TPL = """
new rl(`rho:registry:lookup`), RevVaultCh, vaultCh, revVaultKeyCh, deployerId(`rho:rchain:deployerId`), stdout(`rho:io:stdout`), resultCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreate", "$from", *vaultCh) |
    @RevVault!("deployerAuthKey", *deployerId, *revVaultKeyCh) |
    for (@(true, vault) <- vaultCh; key <- revVaultKeyCh) {
      @vault!("transfer", "$to", $amount, *key, *resultCh) |
      for (_ <- resultCh) { Nil }
    }
  }
}
"""

TRANSFER_ENSURE_TO_RHO_TPL = """
new rl(`rho:registry:lookup`), RevVaultCh, vaultCh, toVaultCh, deployerId(`rho:rchain:deployerId`), revVaultKeyCh, resultCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreate", "$from", *vaultCh) |
    @RevVault!("findOrCreate", "$to", *toVaultCh) |
    @RevVault!("deployerAuthKey", *deployerId, *revVaultKeyCh) |
    for (@(true, vault) <- vaultCh; key <- revVaultKeyCh; @(true, toVault) <- toVaultCh;) {
      @vault!("transfer", "$to", $amount, *key, *resultCh) |
      for (_ <- resultCh) { Nil }
    }
  }
}
"""

# these are predefined param
TRANSFER_PHLO_LIMIT = 1000000
TRANSFER_PHLO_PRICE = 1


def render_contract_template(template: str, substitutions: Mapping[str, str]) -> str:
    return string.Template(template).substitute(substitutions)


class VaultAPI:

    def __init__(self, client: RClient):
        self.client = client

    def get_balance(self, rev_addr: str) -> int:
        contract = render_contract_template(
            GET_BALANCE_RHO_TPL,
            {'addr': rev_addr},
        )
        result = self.client.exploratory_deploy(contract)
        return int(result[0].exprs[0].g_int)

    def transfer(self, from_addr: str, to_addr: str, amount: int, key: PrivateKey) -> str:
        """
        Transfer from `from_addr` to `to_addr` in the chain. Just make sure the `to_addr` is created
        in the chain. Otherwise, the transfer would hang until the `to_addr` is created.
        """
        contract = render_contract_template(
            TRANSFER_RHO_TPL, {
                'from': from_addr,
                'to': to_addr,
                'amount': str(amount)
            }
        )
        timestamp_mill = int(time.time() * 1000)
        return self.client.deploy_with_vabn_filled(key, contract, TRANSFER_PHLO_PRICE, TRANSFER_PHLO_LIMIT,
                                                   timestamp_mill)

    def transfer_ensure(self, from_addr: str, to_addr: str, amount: int, key: PrivateKey) -> str:
        """
        The difference between `transfer_ensure` and `transfer` is that , if the to_addr is not created in the
        chain, the `transfer` would hang until the to_addr successfully created in the change and the `transfer_ensure`
        can be sure that if the `to_addr` is not existed in the chain the process would created the vault in the chain
        and make the transfer successfully.
        """
        contract = render_contract_template(
            TRANSFER_ENSURE_TO_RHO_TPL, {
                'from': from_addr,
                'to': to_addr,
                'amount': str(amount)
            }
        )
        timestamp_mill = int(time.time()* 1000)
        return self.client.deploy_with_vabn_filled(key, contract, TRANSFER_PHLO_PRICE, TRANSFER_PHLO_LIMIT,
                                                   timestamp_mill)

    def create_vault(self, addr: str, key: PrivateKey) -> str:
        contract = render_contract_template(
            CREATE_VAULT_RHO_TPL, {
                'addr': addr
            }
        )
        timestamp_mill = int(time.time() * 1000)
        return self.client.deploy_with_vabn_filled(key, contract, TRANSFER_PHLO_PRICE, TRANSFER_PHLO_LIMIT, timestamp_millis=timestamp_mill)