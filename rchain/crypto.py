import random
import hashlib

import bitcoin.base58
from ecdsa import SigningKey, VerifyingKey
from ecdsa.curves import SECP256k1
from ecdsa.util import sigencode_der_canonize, sigdecode_der


def blake2b_32(data=b''):
    return hashlib.blake2b(data, digest_size=32)


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

    def verify(self, signature: bytes, data: bytes):
        self._pub_key.verify(
            signature, data, hashfunc=blake2b_32, sigdecode=sigdecode_der
        )

    def to_bytes(self) -> bytes:
        return b'\x04' + self._pub_key.to_string()

    def get_address(self) -> str:
        prefix = b'\0\0\0\0'
        pub_key_hash = blake2b_32(self.to_bytes()).digest()
        payload = prefix + pub_key_hash
        payload_chksum = blake2b_32(payload).digest()[:4]
        addr_bytes = payload + payload_chksum
        return bitcoin.base58.encode(addr_bytes)


class PrivateKey:

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
        key_bytes = random.getrandbits(32 * 8).to_bytes(32, 'big')
        return cls.from_bytes(key_bytes)

    def __init__(self, _key: SigningKey):
        self._key = _key

    def sign(self, data: bytes) -> bytes:
        return self._key.sign(
            data, hashfunc=blake2b_32, sigencode=sigencode_der_canonize
        )

    def to_bytes(self) -> bytes:
        return self._key.to_string()

    def get_public_key(self) -> PublicKey:
        return PublicKey(self._key.get_verifying_key())
