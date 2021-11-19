import json

import click

from rchain.client import RClient
from rchain.crypto import PrivateKey, PublicKey, generate_rev_addr_from_eth
from rchain.pb.CasperMessage_pb2 import DeployDataProto
from rchain.util import create_deploy_data


@click.group()
@click.option('--json-output', default=False, is_flag=True)
@click.pass_context
def cli(ctx: click.core.Context, json_output: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj['json_output'] = json_output

@cli.command()
@click.pass_context
@click.option('--input-type', type=click.Choice(['eth', 'public', 'private'], case_sensitive=False),
              help='the kind of the input you are going to provide.')
@click.option('--input', help='the concrete content of your input type')
def get_rev_addr(ctx: click.core.Context, input_type: str, input: str) -> None:
    if input_type == 'eth':
        if input.startswith("0x"):
            input = input[2:]
        addr = generate_rev_addr_from_eth(input)
    elif input_type == 'public':
        pub = PublicKey.from_hex(input)
        addr = pub.get_rev_address()
    elif input_type == 'private':
        private = PrivateKey.from_hex(input)
        addr  = private.get_public_key().get_rev_address()
    else:
        raise NotImplementedError("Not supported type {}".format(input_type))

    if ctx.obj['json_output']:
        click.echo(json.dumps({"revAddress": addr}))
    else:
        click.echo("Rev Address is : {}".format(addr))


@cli.command()
@click.pass_context
@click.option('--private-key', help='the private key hex string is used to sign')
@click.option('--term', help='the rholang term')
@click.option('--phlo-price', type=int, help='phlo price')
@click.option('--phlo-limit', type=int, help='phlo limit')
@click.option('--valid-after-block-number', type=int,
              help='valid after block number, usually used the latest block number')
@click.option('--timestamp', type=int, help='timestamp, unit millisecond')
@click.option('--sig-algorithm', type=click.Choice(['secp256k1']),
              help='signature algorithm. Currently only support secp256k1')
def sign_deploy(ctx: click.core.Context, private_key: str, term: str, phlo_price: int, phlo_limit: int, valid_after_block_number: int,
                timestamp: int, sig_algorithm: str) -> None:
    pri = PrivateKey.from_hex(private_key)
    signed_deploy = create_deploy_data(
        pri, term, phlo_price, phlo_limit, valid_after_block_number, timestamp
    )
    deploy_id = signed_deploy.sig.hex()

    if ctx.obj['json_output']:
        click.echo(json.dumps({"signature": deploy_id}))
    else:
        click.echo("The deploy signature is : {}".format(deploy_id))


@cli.command()
@click.pass_context
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
def submit_deploy(ctx: click.core.Context, deployer: str, term: str, phlo_price: int, phlo_limit: int, valid_after_block_number: int,
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
        ret = client.send_deploy(deploy)

    if ctx.obj["json_output"]:
        click.echo(json.dumps({"deployID": ret}))
    else:
        click.echo("Send {} deploy succeeded".format(sig))

if __name__ == '__main__':
    cli()
