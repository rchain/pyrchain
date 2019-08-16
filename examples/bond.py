# Requires the following line in wallets.txt
#
# 0x06a441c277bf454c5d159b0e5bdafca69b296733,1000000,0

import grpc

from rchain.crypto import PrivateKey
from rchain.client import RClient

from rchain.vault import VaultAPI

alice_key = PrivateKey.from_hex("2a6cd3b196a0b154446a23443cee70629cdb3db0398ea6fb099175708f47f590")
alice_public_key = alice_key.get_public_key()

print("Private key is " + alice_key.to_hex())
print("Public key is " + alice_public_key.to_hex())
print("Eth address is " + alice_public_key.get_eth_address())
print("Rev address is " + alice_public_key.get_rev_address())

with grpc.insecure_channel('localhost:10401') as channel:
    client = RClient(channel)

    alice_vault_api = VaultAPI(client, alice_key)
    alice_vault_api.bond(amount = 100)
    
    alice_bal_deploy_id = alice_vault_api.deploy_get_balance()
    client.propose()

    alice_bal = alice_vault_api.get_balance_from_deploy_id(alice_bal_deploy_id)
    assert alice_bal == 999900