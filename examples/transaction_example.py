from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.pb.RhoTypes_pb2 import GPrivate, GUnforgeable, Par
from rchain.vault import VaultAPI

TESTNET_SERVER = ['node0.testnet.rchain-dev.tk',
                  'node1.testnet.rchain-dev.tk',
                  'node2.testnet.rchain-dev.tk',
                  'node3.testnet.rchain-dev.tk']
TESTNET_READONLY = ['observer.testnet.rchain.coop']

MAINET_SERVER =  ['node0.root-shard.mainnet.rchain.coop',
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

with RClient(TESTNET_READONLY[0], 40401) as client:
    from rchain.param import testnet_param
    # these param are fixed when the network starts on the genesis
    # the param will never change except hard-fork
    # but different network has different param based on the genesis block
    client.install_param(testnet_param)
    block_hash ='8012e93f480d561045f1046d74f8cb7c31a96206e49dbdf15b22a636e18a4693'
    testnet_transactions = client.get_transaction(block_hash)

with RClient(READONLY_SERVER[0], 40401) as client:
    from rchain.param import mainnet_param
    # these param are fixed when the network starts on the genesis
    # the param will never change except hard-fork
    # but different network has different param based on the genesis block
    client.install_param(mainnet_param)
    block_hash ='fe5ceeec3cc5e3d909ef1a688ce2a6c416a474870b13bb9ed96252043593ba5d'

    # only after install_param, the client can get the judge if
    # the transaction happened in the deploy otherwise, it would throw ValueError
    mainnet_transactions = client.get_transaction(block_hash)
