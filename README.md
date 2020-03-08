# pyrchain

Interface to RChain RNode RPC.

## Install 

Pyrchain is Python 3 library for interfacing with RChain RNode gRPC API. The
library is distributed via PyPI (https://pypi.org/project/pyrchain/). You can
install it for current user by running:

	pip3 install -U pyrchain

See `setup.py` for information about 3rd party library dependencies.


## Examples

The features below are provided in pyrchain.

1. [generate private key and public key](./examples/keys_example.py)
2. [sign a deploy with the private key](./examples/sign_verify_examples.py)
3. [use grpc api to interact with rnode](./examples/grpc_api_example.py)
4. [Vault Api of rchain to do transfer and check balance](./examples/vault_example.py)     

## Development

To install the development package:

    pip install -e .[dev]

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
