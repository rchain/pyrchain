import hashlib
import random
from typing import Any, Optional

import bitcoin.base58
from ecdsa import SigningKey, VerifyingKey
from ecdsa.curves import SECP256k1
from ecdsa.util import sigdecode_der, sigencode_der_canonize
from eth_hash.auto import keccak
from eth_keyfile import extract_key_from_keyfile
from google.protobuf.wrappers_pb2 import Int32Value, StringValue
from rchain.pb.CasperMessage_pb2 import BlockMessageProto


def blake2b_32(data: bytes = b'') -> hashlib.blake2b:
    return hashlib.blake2b(data, digest_size=32)


def gen_deploys_hash_from_block(block: BlockMessageProto) -> bytes:
    hash_obj = b"".join([deploy.SerializeToString() for deploy in block.body.deploys])
    return blake2b_32(hash_obj).digest()


def gen_block_hash_from_block(block: BlockMessageProto) -> bytes:
    signed_obj = b''.join([block.header.SerializeToString(),
                           block.body.SerializeToString(),
                           block.sender,
                           StringValue(value=block.sigAlgorithm).SerializeToString(),
                           Int32Value(value=block.seqNum).SerializeToString(),
                           StringValue(value=block.shardId).SerializeToString(),
                           block.extraBytes])
    return blake2b_32(signed_obj).digest()


class PublicKey:

    @classmethod
    def from_bytes(cls, b: bytes) -> 'PublicKey':
        if len(b) == 65:
            b = b[1:]  # remove 0x04 prefix
        return cls(VerifyingKey.from_string(b, curve=SECP256k1))

    @classmethod
    def from_hex(cls, s: str) -> 'PublicKey':
        return cls.from_bytes(bytes.fromhex(s))

    def __init__(self, _pub_key: VerifyingKey):
        self._pub_key = _pub_key

    def verify(self, signature: bytes, data: bytes) -> bool:
        return self._pub_key.verify(
            signature, data, hashfunc=blake2b_32, sigdecode=sigdecode_der
        )

    def verify_block_hash(self, signature: bytes, block_hash: bytes) -> bool:
        return self._pub_key.verify_digest(signature, block_hash, sigdecode=sigdecode_der)

    def to_hex(self, lower: bool = True) -> str:
        return self.to_bytes().hex().lower() if lower else self.to_bytes().hex()

    def to_bytes(self) -> bytes:
        return b'\x04' + self._pub_key.to_string()

    def get_rev_address(self) -> str:
        prefix = b'\0\0\0\0'
        eth_address = self.get_eth_address()
        pub_key_hash = keccak(bytes.fromhex(eth_address))
        payload = prefix + pub_key_hash
        payload_chksum = blake2b_32(payload).digest()[:4]
        addr_bytes = payload + payload_chksum
        return bitcoin.base58.encode(addr_bytes)

    def get_eth_address(self) -> str:
        return keccak(self.to_bytes()[1:]).hex()[-40:]

    def __hash__(self) -> int:
        return hash(self.to_bytes())

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.to_bytes() == other.to_bytes()


class PrivateKey:
    @classmethod
    def from_eth_keyfile(cls, path: str, password: Optional[str] = None) -> 'PrivateKey':
        key_bytes = extract_key_from_keyfile(path, password)
        return cls.from_bytes(key_bytes)

    @classmethod
    def generate(cls) -> 'PrivateKey':
        return cls(SigningKey.generate(curve=SECP256k1))

    @classmethod
    def from_bytes(cls, b: bytes) -> 'PrivateKey':
        return cls(SigningKey.from_string(b, curve=SECP256k1))

    @classmethod
    def from_hex(cls, s: str) -> 'PrivateKey':
        return cls.from_bytes(bytes.fromhex(s))

    @classmethod
    def from_seed(cls, seed: int) -> 'PrivateKey':
        rand = random.Random(seed)
        key_bytes = rand.getrandbits(32 * 8).to_bytes(32, 'big')
        return cls.from_bytes(key_bytes)

    def __init__(self, _key: SigningKey):
        self._key = _key

    def sign(self, data: bytes) -> bytes:
        return self._key.sign(
            data, hashfunc=blake2b_32, sigencode=sigencode_der_canonize
        )

    def sign_block_hash(self, block_hash: bytes) -> bytes:
        return self._key.sign_digest(block_hash, sigencode=sigencode_der_canonize)

    def to_bytes(self) -> bytes:
        return self._key.to_string()

    def to_hex(self, lower: bool = True) -> str:
        return self.to_bytes().hex().lower() if lower else self.to_bytes().hex()

    def get_public_key(self) -> PublicKey:
        return PublicKey(self._key.get_verifying_key())

    def __hash__(self) -> int:
        return hash(self.to_bytes())

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.to_bytes() == other.to_bytes()
