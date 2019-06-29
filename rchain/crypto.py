import hashlib

from ecdsa import SigningKey, VerifyingKey
from ecdsa.curves import SECP256k1
from ecdsa.util import sigencode_der_canonize


def blake2b_32(data=b''):
    return hashlib.blake2b(data, digest_size=32)


class PublicKey:
    def __init__(self, _pub_key: VerifyingKey):
        self._pub_key = _pub_key

    def to_bytes(self) -> bytes:
        return b'\x04' + self._pub_key.to_string()


class PrivateKey:
    @classmethod
    def generate(cls) -> 'PrivateKey':
        return cls(SigningKey.generate(curve=SECP256k1))

    def __init__(self, _key: SigningKey):
        self._key = _key

    def sign(self, data: bytes) -> bytes:
        return self._key.sign(data, hashfunc=blake2b_32, sigencode=sigencode_der_canonize)

    def get_public_key(self) -> PublicKey:
        return PublicKey(self._key.get_verifying_key())
