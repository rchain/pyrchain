# pyrchain

Interface to RChain RNode RPC.

## Usage

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

See `./examples/wallets.py` for complete example of vault API usage.
See `rchain.client.RClient` class for available RPC API.

To run the example from this Git repository run:

	pipenv install
	pipenv run python examples/wallets.py

## Development

To update protocol buffers from upstream run:

	./update-protobufs
	./update-generated

This first command will fetch latest RChain `*.proto` files from `dev`
branch into `./protobuf` directory. The second command will generate
gRPC Python code corresponding to the protcol buffers into `rchain.pb`
package (`./rchain/pb`).
