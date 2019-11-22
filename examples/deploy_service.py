import logging

import time
import grpc

from rchain.crypto import PrivateKey
from rchain.client import RClient
from rchain.vault import VaultAPI

term = """
new stderr(`rho:io:stderr`) in {
  stderr!("hello, world!")
}

"""

def main():
    with grpc.insecure_channel('192.168.1.9:40401') as channel:
        client = RClient(channel)
        block_info = client.show_block("1f187078e338c57fbdc0e91ca0470567c31a960c27d4da792f96536366414491")
        print(block_info)

        blocks_infos = client.show_blocks(3)
        print(blocks_infos)
        timestamp = int(time.time() * 1000)
        client.deploy_with_vabn_filled(PrivateKey.from_hex("80366db5fbb8dad7946f27037422715e4176dda41d582224db87b6c3b783d709"), term, 1, 1000000, timestamp)
if __name__ == "__main__":
    main()