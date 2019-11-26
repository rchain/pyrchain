import logging

import grpc
from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.vault import VaultAPI


def main():
    god_key    = PrivateKey.from_hex("9a801debae8bb97fe54c99389cafa576c60612503348578125b65ab182ff5850")
    alice_key  = PrivateKey.from_hex("b2527b00340a83e302beae2a8daf6d654e8e57541acfa261cc1b5635eb16aa15")
    bob_key    = PrivateKey.from_hex("567ea426deaeb8233f134c3a266149fb196d6eea7d28b447dfefff92002cb400")

    alice_addr   = PrivateKey.from_hex("b2527b00340a83e302beae2a8daf6d654e8e57541acfa261cc1b5635eb16aa15").get_public_key().get_rev_address()
    god_addr = PrivateKey.from_hex("9a801debae8bb97fe54c99389cafa576c60612503348578125b65ab182ff5850").get_public_key().get_rev_address()
    bob_addr   = PrivateKey.from_hex("567ea426deaeb8233f134c3a266149fb196d6eea7d28b447dfefff92002cb400").get_public_key().get_rev_address()

    with grpc.insecure_channel('rchain-kuxgz.bootstrap:40401') as channel:
        client = RClient(channel)

        god_vault_api   = VaultAPI(client, god_key)
        alice_vault_api = VaultAPI(client, alice_key)
        bob_vault_api   = VaultAPI(client, bob_key)

        # Most methods without deploy_ prefix create block (propose) after
        # deploy. To deploy a batch and then create block do:
        #
        #  alice_vault_api.deploy_create_vault()
        #  bob_vault_api.deploy_create_vault()
        #  client.propose()

        alice_vault_api.create_vault()
        bob_vault_api.create_vault()

        assert alice_vault_api.get_balance()   == 5000
        assert god_vault_api.get_balance() == 0
        assert bob_vault_api.get_balance()   == 0

        alice_vault_api.transfer(None, bob_addr, 1000)

        # Example way to get balances in one block:

        god_bal_deploy_id   = god_vault_api.deploy_get_balance()
        alice_bal_deploy_id = alice_vault_api.deploy_get_balance()
        bob_bal_deploy_id   = bob_vault_api.deploy_get_balance()
        client.propose()

        god_bal   = god_vault_api.get_balance_from_deploy_id(god_bal_deploy_id)
        alice_bal = alice_vault_api.get_balance_from_deploy_id(alice_bal_deploy_id)
        bob_bal   = bob_vault_api.get_balance_from_deploy_id(bob_bal_deploy_id)

        assert god_bal   == 0
        assert alice_bal == 4000
        assert bob_bal   == 1000

        bob_vault_api.transfer(None, god_addr, 400)

        assert god_vault_api.get_balance()   == 400
        assert alice_vault_api.get_balance() == 4000
        assert bob_vault_api.get_balance()   == 600


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
