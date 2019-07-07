# pyrchain

Interface to RChain RNode RPC.

## Usage

See `./examples/wallets.py` for example usage.

## Building

  ./update-protobufs
  ./update-generated
  export PYTHONPATH="$PWD/generated"
  pipenv install
  pipenv run python examples/wallets.py
