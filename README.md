# pyrchain

Interface to RChain RNode RPC.

## Usage

Pyrchain is Python 3 library for interfacing with RChain RNode gRPC API. The
library is distributed via PyPI (https://pypi.org/project/pyrchain/). You can
install it for current user by running:

	pip3 install --user pyrchain

See `setup.py` for information about 3rd party library dependencies.

The following snippet shows example usage of the API the library provides. It
assumes that you have access to a running RNode instance on `localhost` with
gRPC service listening on TCP port 40401 (default).

	import grpc

	from rchain.crypto import PrivateKey
	from rchain.client import RClient
	from rchain.vault import VaultAPI

	admin_key = PrivateKey.generate()
	alice_key = PrivateKey.generate()

	with grpc.insecure_channel('localhost:40401') as channel:
	    client = RClient(channel)

	    admin_vault_api = VaultAPI(client, admin_key)
	    alice_vault_api = VaultAPI(client, alice_key)

	    admin_vault_api.create_genesis_vault(None, 100_000)
	    admin_vault_api.transfer(None, alice_key.get_public_key().get_address(), 1000)
	    assert alice_vault_api.get_balance() == 1000

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

To run unit tests run:

	pipenv run python -m unittest rchain/*_test.py

## References

- https://github.com/rchain-community/rchain-api

  #### JavaScript API for RChain RNode RPC
  
  Includes Rholang parser. Has dApp users already.
  
- https://github.com/rchain-community/rchain-grpc/

  #### Python API for RChain RNode RPC
  
  Seems to cover more of the available gRPC APIs. The author of pyrchain wasn't aware of rchain-grpc existence.
