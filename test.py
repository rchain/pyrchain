import logging

import grpc

from rchain.crypto import PrivateKey
from rchain.client import RClient
from rchain.vault import VaultAPI


def main():
    god_key = PrivateKey.generate()
    alice_key = PrivateKey.generate()
    bob_key = PrivateKey.generate()

    god_addr = god_key.get_public_key().get_address()
    alice_addr = alice_key.get_public_key().get_address()
    bob_addr = bob_key.get_public_key().get_address()

    with grpc.insecure_channel('172.27.0.2:40401') as channel:
        client = RClient(channel)

        god_vault_api = VaultAPI(client, god_key)
        alice_vault_api = VaultAPI(client, alice_key)
        bob_vault_api = VaultAPI(client, bob_key)

        god_vault_api.create_genesis_vault(None, 100_000)
        alice_vault_api.create_vault()
        bob_vault_api.create_vault()

        # or
        #god_vault_api.deploy_create_genesis_vault(None, 100_000)
        #alice_vault_api.deploy_create_vault()
        #bob_vault_api.deploy_create_vault()
        #client.propose()

        assert god_vault_api.get_balance() == 100_000
        assert alice_vault_api.get_balance() == 0
        assert bob_vault_api.get_balance() == 0

        god_vault_api.transfer(None, alice_addr, 1000)

        assert god_vault_api.get_balance() == 99_000
        assert alice_vault_api.get_balance() == 1000
        assert bob_vault_api.get_balance() == 0

        alice_vault_api.transfer(None, bob_addr, 400)

        assert god_vault_api.get_balance() == 99_000
        assert alice_vault_api.get_balance() == 600
        assert bob_vault_api.get_balance() == 400


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
