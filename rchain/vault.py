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
new rl(`rho:registry:lookup`), RevVaultCh, vaultCh, revVaultKeyCh, resultCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreate", "$from", *vaultCh) |
    @RevVault!("findOrCreate", "to", *vaultCh) |
    @RevVault!("deployerAuthKey", *revVaultKeyCh) |
    for (@(true, vault) <- vaultCh; key <- revVaultKeyCh) {
      @vault!("transfer", "$to", $amount, *key, *resultCh) |
      for (_ <- resultCh) { Nil }
    }
  }
}
"""

# these are predefined param
TRANSFER_PHLO_LIMIT = 100000
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
