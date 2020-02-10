# pyrchain

Interface to RChain RNode RPC.

## Install 

Pyrchain is Python 3 library for interfacing with RChain RNode gRPC API. The
library is distributed via PyPI (https://pypi.org/project/pyrchain/). You can
install it for current user by running:

	pip3 install -U pyrchain

See `setup.py` for information about 3rd party library dependencies.


## Tutorial

The features below are provided in pyrchain.

1. generate private key and public key
2. sign a deploy with the private key
3. use grpc api to interact with rnode
4. Vault Api of rchain to do transfer, bonding and etc.


### generate private key and public key

Currently you can generate Private private key from `hex`, `bytes`, `seed` or 
randomly.And you can generate public key from private key `get_public_key` or 
from `hex` or `bytes`. 

#### PrivateKey

    from rchain.crypto import PrivateKey
    
    # randomly generate private key
    PrivateKey.generate()
    
    # generate from hex
    PrivateKey.from_hex("ff2ba092524bafdbc85fa0c7eddb2b41c69bc9bf066a4711a8a16f749199e5be")
    
    # generate from bytes
    PrivateKey.from_bytes(b'\xff+\xa0\x92RK\xaf\xdb\xc8_\xa0\xc7\xed\xdb+A\xc6\x9b\xc9\xbf\x06jG\x11\xa8\xa1ot\x91\x99\xe5\xbe')
    
    # generate from seed
    PrivateKey.from_seed(1)

#### PublicKey

    from rchain.crypto import PrivateKey, PublicKey
    
    # generate from private key
    PrivateKey.generate().get_public_key()
    
    # generate from hex
    PublicKey.from_hex("04ad4793d81c5ee6c91c4baf2689c5299276c4774a8625fa87257f62ba8f3fe31f79d1351bd83af800afdaa94d40fe46c969f0ce2ac2e03e45d5a2d8a7687c39c0")
    
    # generate from bytes
    PublicKey.from_bytes(b'\x04\xadG\x93\xd8\x1c^\xe6\xc9\x1cK\xaf&\x89\xc5)\x92v\xc4wJ\x86%\xfa\x87%\x7fb\xba\x8f?\xe3\x1fy\xd15\x1b\xd8:\xf8\x00\xaf\xda\xa9M@\xfeF\xc9i\xf0\xce*\xc2\xe0>E\xd5\xa2\xd8\xa7h|9\xc0')
    
#### Rev Address
Generate rev address.

    from rchain.crypto import PrivateKey, PublicKey
    PrivateKey.generate().get_public_key().get_rev_address()
    
### Sign a deploy and verify

Currently you can sign a deploy with the private key you generate and verify 
the deploy.

    import time
    from rchain.crypto import PrivateKey, PublicKey
    from rchain.util import create_deploy_data, verify_deploy_data
    
    private_key = PrivateKey.generate()
    public_key = private_key.get_public_key()
    
    contract = "@0!(2)"
    
    deploy_data = create_deploy_data(key=private_key, 
                                    term=contract, phlo_price=1, 
                                    phlo_limit=100000, 
                                    valid_after_blo>ck_no=10, 
                                    timestamp_millis = int(time.time()*1000))
    
    
    assert verify_deploy_data(public_key, deploy_data.sig, deploy_data)
    
### use grpc api client

The following snippet shows example usage of the API the library provides. It
assumes that you have access to a running RNode instance on `localhost` with
gRPC service listening on TCP port 40401 (default).

	import grpc
    import time
	from rchain.crypto import PrivateKey
	from rchain.client import RClient

	admin_key = PrivateKey.generate()
    contract = "@1!(2)"
    
	with grpc.insecure_channel('localhost:40401') as channel:
	    client = RClient(channel)

        # get the latest 10 block in the rnode
        block_infos = client.show_blocks(depth=10)
        
        # get the detailed info in the rnode
        block = client.show_block(block_hash)
        
        # deploy with validate after block number argument
        deploy_id = client.deploy_with_vabn_filled(key=admin_key, 
                                                    term=contract, 
                                                    phlo_price=1, phlo_limit=1000000, 
                                                    timestamp_millis=int(time.time()*1000)) 


### Vault api

You can use Vault api to create vault, transfer in the rchain.

    import grpc
    from rchain.client import RClient
    from rchain.crypto import PrivateKey
    from rchain.vault import VaultAPI

    alice_key = PrivateKey.generate()
    bob_key = PrivateKey.generate()
    alice_rev_addr = alice_key.get_public_key().get_rev_address()
    bob_rev_addr = bob_key.get_public_key().get_rev_address()
    
    
    with grpc.insecure_channel('localhost:40401') as channel:
        client = RClient(channel)

        bob_vault_api   = VaultAPI(client, bob_key)
        alice_vault_api = VaultAPI(client, alice_key)
        
        alice_vault_api.create_vault()
        bob_vault_api.create_vault()
        
        alice_vault_api.transfer(from_addr=alice_rev_addr, to_addr=bob_rev_addr, amount=10000, phlo_price=1, phlo_limit=100000)
       
       

See `./examples/vaults.py` for complete example of vault API usage. See
`rchain.client.RClient` class for available RPC API.

To run the example from this Git repository run:

	pipenv install
	pipenv run python examples/vaults.py

## Development

To update protocol buffers from upstream run:

	./update-protobufs
	./update-generated

This first command will fetch latest RChain `*.proto` files from `dev` branch
into `./protobuf` directory. The second command will generate gRPC Python code
corresponding to the protcol buffers into `rchain.pb` package (`./rchain/pb`).

To run integration tests run:

	python -m pytest rchain/tests
    python -m mypy rchain
    isort --recursive --check-only rchain
