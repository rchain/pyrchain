import grpc
import time
from rchain.crypto import PrivateKey
from rchain.client import RClient

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

admin_key = PrivateKey.generate()
contract = "@1!(2)"

exploratory_term = 'new return in{return!("a")}'

block_hash = '4d135ce5773a05a782d1c52a7dfb42c4142b1a471bc3c57d77eee4d5affdef9a'


# read-only node can not deploy with deploy request
with RClient(READONLY_SERVER[0], 40401) as client:
    # get the latest 10 block in the rnode
    block_infos = client.show_blocks(depth=10)

    # get the detailed info in the rnode
    block = client.show_block(block_hash)

    # get the last finalize block from the node
    last_finalize_block = client.last_finalized_block()

    # confirm if a block is finalized
    assert client.is_finalized(block_hash)

    # exploratory deploy can only used for read-only node
    # this method is for exploring the data in the tuple space
    result = client.exploratory_deploy(exploratory_term)


# only valid validator can process deploy request
# all the methods above can be processed by the validator except exploratory deploy
with RClient(MAINNET_SERVER[1], 40401) as client:

    # normal deploy
    deploy_id = client.deploy(key=admin_key, term=contract, phlo_price=1, phlo_limit=1000000, valid_after_block_no=100,
                              timestamp_millis=int(time.time() * 1000))
    # deploy with validate after block number argument
    # the difference between `deploy` and `deploy_with_vabn_filled` is that
    # valid after block number is not auto filled by fetching the newest block number which would be assure
    # your block number is valid for the validator
    # Strongly recommend you use this method unless you know what you are doing.
    deploy_id2 = client.deploy_with_vabn_filled(key=admin_key,
                                                term=contract,
                                                phlo_price=1, phlo_limit=1000000,
                                                timestamp_millis=int(time.time() * 1000))
    # this will raise a exception
    client.exploratory_deploy(exploratory_term)