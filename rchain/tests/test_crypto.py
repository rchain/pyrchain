import os

import pytest
from ecdsa.keys import BadSignatureError
from rchain.crypto import PrivateKey, PublicKey, blake2b_32


@pytest.mark.parametrize('input_str,expected_output', [
    ('', '0e5751c026e543b2e8ab2eb06099daa1d1e5df47778f7787faab45cdf12fe3a8'),
    ('foo', 'b8fe9f7f6255a6fa08f668ab632a8d081ad87983c77cd274e48ce450f0b349fd'),
    (
            'sRHyrQZuEdI5WyvJD1YwCVaUpFEHCCZXF7HIIPMUIABwwr6EWNPRB1s3XkYzobM8TxHA2NHpxjzUzIxk',
            'cb44058e45aeca88339b16c53d3e2544246bc9a6aa4f831cf2099d70037aba61'
    ),
])
def test_blake2b_32(input_str: str, expected_output: str) -> None:
    actual_output = blake2b_32(input_str.encode()).digest().hex()
    assert expected_output == actual_output


keys_identities = [
    (
        '1000000000000000000000000000000000000000000000000000000000000000',
        '0408ea9666139527a8c1dd94ce4f071fd23c8b350c5a4bb33748c4ba111faccae0620efabbc8ee2782e24e7c0cfb95c5d735b783be9cf0f8e955af34a30e62b945',
        '1111cnoFDAa7GubxBMHpPLbbediPegnjSdZwNjxg9oqYvSvSmfqQL'
    ),
    (
        '1111111111111111111111111111111111111111111111111111111111111111',
        '044f355bdcb7cc0af728ef3cceb9615d90684bb5b2ca5f859ab0f0b704075871aa385b6b1b8ead809ca67454d9683fcf2ba03456d6fe2c4abe2b07f0fbdbb2f1c1',
        '111125UED2qbF3aman9PYvfeTk81TuP4fVL5nYsEXtFyTtaLPcHW61'
    ),
    (
        '2222222222222222222222222222222222222222222222222222222222222222',
        '04466d7fcae563e5cb09a0d1870bb580344804617879a14949cf22285f1bae3f276728176c3c6431f8eeda4538dc37c865e2784f3a9e77d044f33e407797e1278a',
        '1111yoPaoSxvmNRGDpP9GUGToHaCdUFEu3KdbNgTuyydUgg6cty7g'
    )
]


@pytest.mark.parametrize("key_hex,pub_key_hex,rev_address", keys_identities)
def test_privatekey_function(key_hex: str, pub_key_hex: str, rev_address: str) -> None:
    key = PrivateKey.from_hex(key_hex)
    pub_key = key.get_public_key()
    actual_pub_key_hex = pub_key.to_bytes().hex()
    assert pub_key_hex == actual_pub_key_hex


@pytest.mark.parametrize("key_hex,pub_key_hex,rev_address", keys_identities)
def test_publickey_from_hex(key_hex: str, pub_key_hex: str, rev_address: str) -> None:
    key = PrivateKey.from_hex(key_hex)
    pub_key = PublicKey.from_hex(pub_key_hex)
    expected_pub_key_bytes = key.get_public_key().to_bytes()
    actual_pub_key_bytes = pub_key.to_bytes()
    assert expected_pub_key_bytes == actual_pub_key_bytes


@pytest.mark.parametrize("key_hex,pub_key_hex,rev_address", keys_identities)
def test_key_to_hex(key_hex: str, pub_key_hex: str, rev_address: str) -> None:
    private_key = PrivateKey.from_hex(key_hex)
    assert private_key.to_hex() == key_hex
    public_key = PublicKey.from_hex(pub_key_hex)
    assert public_key.to_hex() == pub_key_hex


@pytest.mark.parametrize("key_hex,pub_key_hex,rev_address", keys_identities)
def test_sign_verify_good(key_hex: str, pub_key_hex: str, rev_address: str) -> None:
    key = PrivateKey.from_hex(key_hex)
    pub_key = PublicKey.from_hex(pub_key_hex)
    message = 'hello rchain'.encode()
    signature = key.sign(message)
    pub_key.verify(signature, message)


@pytest.mark.parametrize("key_hex,pub_key_hex,rev_address", keys_identities)
def test_sign_verify_bad(key_hex: str, pub_key_hex: str, rev_address: str) -> None:
    key = PrivateKey.from_hex(key_hex)
    pub_key = PublicKey.from_hex(pub_key_hex)
    sign_message = 'hello rchain'.encode()
    verify_message = 'hello world'.encode()
    signature = key.sign(sign_message)
    with pytest.raises(BadSignatureError):
        pub_key.verify(signature, verify_message)


@pytest.mark.parametrize("key_hex,pub_key_hex,rev_address", keys_identities)
def test_sign_block_hash_verify_good(key_hex: str, pub_key_hex: str, rev_address: str) -> None:
    key = PrivateKey.from_hex(key_hex)
    pub_key = PublicKey.from_hex(pub_key_hex)
    message = 'hello rchain'.encode()
    digest = blake2b_32(message).digest()
    signature = key.sign_block_hash(digest)
    pub_key.verify_block_hash(signature, digest)


@pytest.mark.parametrize("key_hex,pub_key_hex,rev_address", keys_identities)
def test_sign_block_hash_verify_bad(key_hex: str, pub_key_hex: str, rev_address: str) -> None:
    key = PrivateKey.from_hex(key_hex)
    pub_key = PublicKey.from_hex(pub_key_hex)
    sign_message = 'hello rchain'.encode()
    verify_message = 'hello world'.encode()
    block_hash = blake2b_32(sign_message).digest()
    signature = key.sign_block_hash(block_hash)
    verify_digest = blake2b_32(verify_message).digest()
    with pytest.raises(BadSignatureError):
        pub_key.verify_block_hash(signature, verify_digest)


@pytest.mark.parametrize("key_hex,pub_key_hex,rev_address", keys_identities)
def test_address(key_hex: str, pub_key_hex: str, rev_address: str) -> None:
    pub_key = PublicKey.from_hex(pub_key_hex)
    actual_address = pub_key.get_rev_address()
    assert rev_address == actual_address


def test_private_key_from_eth_path():
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/key.json')
    PrivateKey.from_eth_keyfile(key_path, 'testpassword')
