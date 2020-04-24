import time

import grpc
from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.vault import render_contract_template, TRANSFER_RHO_TPL, TRANSFER_PHLO_LIMIT, TRANSFER_PHLO_PRICE
from rchain.util import create_deploy_data

a = PrivateKey.generate()
b = PrivateKey.generate()

# get the latest block number
with RClient('node0.root-shard.mainnet.rchain.coop', 40401) as client:
    # get the latest 10 block in the rnode
    latest_blocks = client.show_blocks(depth=1)
    latest_block = latest_blocks[0]
    latest_block_num = latest_block.blockNumber

# sign the transfer deploy
from_addr = a.get_public_key().get_rev_address()
to_addr = b.get_public_key().get_rev_address()
amount = 10000
contract = render_contract_template(
    TRANSFER_RHO_TPL, {
        'from': from_addr,
        'to': to_addr,
        'amount': str(amount)
    }
)
timestamp_mill = int(time.time() * 1000)
# this would create the protobuf needs to be signed and sign the protobuf and return protobuf back
deploy = create_deploy_data(a, contract, TRANSFER_PHLO_PRICE, TRANSFER_PHLO_LIMIT, latest_block_num, timestamp_mill)
# deploy.sig is the deployId and you can use find_deploy to fetch the deployed block


with RClient('node0.root-shard.mainnet.rchain.coop', 40401) as client:
    # send the signed deploy to the network
    resp = client.send_deploy(deploy)

