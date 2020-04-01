from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.vault import VaultAPI

MAINNET_SERVER = ['node0.root-shard.mainnet.rchain.coop',
                  'node1.root-shard.mainnet.rchain.coop',
                  'node2.root-shard.mainnet.rchain.coop',
                  'node3.root-shard.mainnet.rchain.coop',
                  'node4.root-shard.mainnet.rchain.coop',
                  'node5.root-shard.mainnet.rchain.coop',
                  'node6.root-shard.mainnet.rchain.coop',
                  'node7.root-shard.mainnet.rchain.coop',
                  'node8.root-shard.mainnet.rchain.coop']
READONLY_SERVER = ['observer-asia.services.mainnet.rchain.coop',
                   'observer-us.services.mainnet.rchain.coop',
                   'observer-eu.services.mainnet.rchain.coop']

alice = PrivateKey.from_hex('61e594124ca6af84a5468d98b34a4f3431ef39c54c6cf07fe6fbf8b079ef64f6')
bob = PrivateKey.generate()

exploratory_term = 'new return in{return!("a")}'

with RClient(READONLY_SERVER[0], 40401) as client:
    vault = VaultAPI(client)
    # get the balance of a vault
    # get balance can only perform in the read-only node
    bob_balance = vault.get_balance(bob.get_public_key().get_rev_address())

with RClient(MAINNET_SERVER[0], 40401) as  client:
    # because transfer need a valid deploy
    # the transfer need the private to perform signing
    vault = VaultAPI(client)
    deployId = vault.transfer(alice.get_public_key().get_rev_address(), bob.get_public_key().get_rev_address(), 100000, alice)
