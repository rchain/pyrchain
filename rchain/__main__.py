import click

from rchain.client import RClient
from rchain.crypto import PrivateKey, PublicKey, generate_rev_addr_from_eth
from rchain.pb.CasperMessage_pb2 import DeployDataProto
from rchain.util import create_deploy_data


@click.command()
@click.option('--input-type', type=click.Choice(['eth', 'public', 'private'], case_sensitive=False),
              help='the kind of the input you are going to provide.')
@click.option('--input', help='the concrete content of your input type')
def get_rev_addr(input_type: str, input: str) -> None:
    if input_type == 'eth':
        click.echo(generate_rev_addr_from_eth(input))
    elif input_type == 'public':
        pub = PublicKey.from_hex(input)
        click.echo(pub.get_rev_address())
    elif input_type == 'private':
        private = PrivateKey.from_hex(input)
        click.echo(private.get_public_key().get_rev_address())
    else:
        raise NotImplementedError("Not supported type {}".format(input_type))


@click.command()
@click.option('--private-key', help='the private key hex string is used to sign')
@click.option('--term', help='the rholang term')
@click.option('--phlo-price', type=int, help='phlo price')
@click.option('--phlo-limit', type=int, help='phlo limit')
@click.option('--valid-after-block-number', type=int,
              help='valid after block number, usually used the latest block number')
@click.option('--timestamp', type=int, help='timestamp, unit millisecond')
@click.option('--sig-algorithm', type=click.Choice(['secp256k1']),
              help='signature algorithm. Currently only support secp256k1')
def sign_deploy(private_key: str, term: str, phlo_price: int, phlo_limit: int, valid_after_block_number: int,
                timestamp: int, sig_algorithm: str) -> None:
    pri = PrivateKey.from_hex(private_key)
    signed_deploy = create_deploy_data(
        pri, term, phlo_price, phlo_limit, valid_after_block_number, timestamp
    )
    click.echo(signed_deploy.sig.hex())


@click.command()
@click.option('--deployer', help='the public key hex string is used to sign')
@click.option('--term', help='the rholang term')
@click.option('--phlo-price', type=int, help='phlo price')
@click.option('--phlo-limit', type=int, help='phlo limit')
@click.option('--valid-after-block-number', type=int,
              help='valid after block number, usually used the latest block number')
@click.option('--timestamp', type=int, help='timestamp, unit millisecond')
@click.option('--sig-algorithm', type=click.Choice(['secp256k1']),
              help='signature algorithm. Currently only support secp256k1')  # not used actually
@click.option('--sig', help='the signature of the deploy')
@click.option('--host', help='validator host the deploy is going to send to')
@click.option('--port', type=int, help='validator grpc port the deploy is going to send to')
def submit_deploy(deployer: str, term: str, phlo_price: int, phlo_limit: int, valid_after_block_number: int,
                  timestamp: int, sig_algorithm: str, sig: str, host: str,
                  port: int) -> None:
    deploy = DeployDataProto(
        deployer=bytes.fromhex(deployer),
        term=term,
        phloPrice=phlo_price,
        phloLimit=phlo_limit,
        validAfterBlockNumber=valid_after_block_number,
        timestamp=timestamp,
        sigAlgorithm='secp256k1',
        sig=bytes.fromhex(sig)
    )
    with RClient(host, port) as client:
        client.send_deploy(deploy)


@click.group()
def cli() -> None:
    pass


cli.add_command(get_rev_addr)
cli.add_command(sign_deploy)
cli.add_command(submit_deploy)

if __name__ == '__main__':
    cli()
