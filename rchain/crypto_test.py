import unittest

from ecdsa.keys import BadSignatureError

from .crypto import blake2b_32, PrivateKey, PublicKey


class TestCrypto(unittest.TestCase):

    def test_blake2b_32(self):
        in_out_list = [
            ('', '0e5751c026e543b2e8ab2eb06099daa1d1e5df47778f7787faab45cdf12fe3a8'),
            ('foo', 'b8fe9f7f6255a6fa08f668ab632a8d081ad87983c77cd274e48ce450f0b349fd'),
            (
                'sRHyrQZuEdI5WyvJD1YwCVaUpFEHCCZXF7HIIPMUIABwwr6EWNPRB1s3XkYzobM8TxHA2NHpxjzUzIxk',
                'cb44058e45aeca88339b16c53d3e2544246bc9a6aa4f831cf2099d70037aba61'
            ),
        ]
        for input_str, expected_output in in_out_list:
            actual_output = blake2b_32(input_str.encode()).digest().hex()
            self.assertEqual(expected_output, actual_output)

    identities = [
        (
            '1000000000000000000000000000000000000000000000000000000000000000',
            '0408ea9666139527a8c1dd94ce4f071fd23c8b350c5a4bb33748c4ba111faccae0620efabbc8ee2782e24e7c0cfb95c5d735b783be9cf0f8e955af34a30e62b945',
            '1111sc15PERLugDRdfPHkSfYPpar8i1NcwM5hKsE64HVUG2zCF5sy'
        ),
        (
            '1111111111111111111111111111111111111111111111111111111111111111',
            '044f355bdcb7cc0af728ef3cceb9615d90684bb5b2ca5f859ab0f0b704075871aa385b6b1b8ead809ca67454d9683fcf2ba03456d6fe2c4abe2b07f0fbdbb2f1c1',
            '1111GcGEJX6me9vVN5cPGbFHSXepo8BvQ9r9CFcNmYSemHDvdpPZB'
        ),
        (
            '2222222222222222222222222222222222222222222222222222222222222222',
            '04466d7fcae563e5cb09a0d1870bb580344804617879a14949cf22285f1bae3f276728176c3c6431f8eeda4538dc37c865e2784f3a9e77d044f33e407797e1278a',
            '11112JaqFvFpwWBEUc1jhLRkY2BuF7vgMxYCc3hepqdj2ad9U7Lg3g'
        )
    ]

    def test_privatekey_from_hex(self):
        for key_hex, expected_pub_key_hex, _ in self.identities:
            key = PrivateKey.from_hex(key_hex)
            pub_key = key.get_public_key()
            actual_pub_key_hex = pub_key.to_bytes().hex()
            self.assertEqual(expected_pub_key_hex, actual_pub_key_hex)

    def test_publickey_from_hex(self):
        for key_hex, pub_key_hex, _ in self.identities:
            key = PrivateKey.from_hex(key_hex)
            pub_key = PublicKey.from_hex(pub_key_hex)
            expected_pub_key_bytes = key.get_public_key().to_bytes()
            actual_pub_key_bytes = pub_key.to_bytes()
            self.assertEqual(expected_pub_key_bytes, actual_pub_key_bytes)

    def test_sign_verify_good(self):
        for key_hex, pub_key_hex, _ in self.identities:
            key = PrivateKey.from_hex(key_hex)
            pub_key = PublicKey.from_hex(pub_key_hex)
            message = 'hello rchain'.encode()
            signature = key.sign(message)
            pub_key.verify(signature, message)

    def test_sign_verify_bad(self):
        for key_hex, pub_key_hex, _ in self.identities:
            key = PrivateKey.from_hex(key_hex)
            pub_key = PublicKey.from_hex(pub_key_hex)
            sign_message = 'hello rchain'.encode()
            verify_message = 'hello world'.encode()
            signature = key.sign(sign_message)
            with self.assertRaises(BadSignatureError):
                pub_key.verify(signature, verify_message)

    def test_address(self):
        for _, pub_key_hex, expected_address in self.identities:
            pub_key = PublicKey.from_hex(pub_key_hex)
            actual_address = pub_key.get_address()
            self.assertEqual(expected_address, actual_address)
