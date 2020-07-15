from dataclasses import dataclass

from rchain.pb.RhoTypes_pb2 import GPrivate, GUnforgeable, Par

"""
These parameter are pre defined params which can help access the data quicklier.
It is not the best way to solve the problem right now.But it is the fast way.
"""
@dataclass
class Params:
    transfer_unforgeable: Par


_testnet_transfer_unforgeable_id = "72d0f333c719323406901bca34c2935e4d92c31402fa80a2c273422e923af550"
_testnet_transfer_template = Par(unforgeables=[GUnforgeable(g_private_body=GPrivate(id=bytes.fromhex(_testnet_transfer_unforgeable_id)))])
testnet_param = Params(transfer_unforgeable=_testnet_transfer_template)

_mainnet_transfer_unforgeable_id = "72d0f333c719323406901bca34c2935e4d92c31402fa80a2c273422e923af550"
_mainnet_transfer_template = Par(unforgeables=[GUnforgeable(g_private_body=GPrivate(id=bytes.fromhex(_mainnet_transfer_unforgeable_id)))])
mainnet_param = Params(transfer_unforgeable=_mainnet_transfer_template)
