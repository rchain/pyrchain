# Requires the following line in wallets.txt
#
# 0x06a441c277bf454c5d159b0e5bdafca69b296733,1000000,0

import grpc
from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.vault import VaultAPI

alice_key = PrivateKey.from_hex("b2527b00340a83e302beae2a8daf6d654e8e57541acfa261cc1b5635eb16aa15")
alice_public_key = alice_key.get_public_key()

print("Private key is " + alice_key.to_hex())
print("Public key is " + alice_public_key.to_hex())
print("Eth address is " + alice_public_key.get_eth_address())
print("Rev address is " + alice_public_key.get_rev_address())

with grpc.insecure_channel('rchain-kuxgz.bootstrap:40401') as channel:
    client = RClient(channel)

    alice_vault_api = VaultAPI(client, alice_key)
    alice_vault_api.bond(amount = 100)
    
    alice_bal_deploy_id = alice_vault_api.deploy_get_balance()
    client.propose()

    alice_bal = alice_vault_api.get_balance_from_deploy_id(alice_bal_deploy_id)
    assert alice_bal == 3900
