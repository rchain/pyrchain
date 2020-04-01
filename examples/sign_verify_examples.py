import time

from rchain.crypto import PrivateKey, PublicKey
from rchain.util import create_deploy_data, verify_deploy_data

private_key = PrivateKey.generate()
public_key = private_key.get_public_key()

contract = "@0!(2)"

deploy_data = create_deploy_data(key=private_key,
                                 term=contract, phlo_price=1,
                                 phlo_limit=100000,
                                 valid_after_block_no=10,
                                 timestamp_millis=int(time.time() * 1000))

assert verify_deploy_data(public_key, deploy_data.sig, deploy_data)
