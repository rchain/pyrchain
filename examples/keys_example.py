from rchain.crypto import PrivateKey, PublicKey

# randomly generate private key
PrivateKey.generate()

# generate private key from hex
PrivateKey.from_hex("ff2ba092524bafdbc85fa0c7eddb2b41c69bc9bf066a4711a8a16f749199e5be")

# generate private key from bytes
PrivateKey.from_bytes(b'\xff+\xa0\x92RK\xaf\xdb\xc8_\xa0\xc7\xed\xdb+A\xc6\x9b\xc9\xbf\x06jG\x11\xa8\xa1ot\x91\x99\xe5\xbe')

# generate private key from seed
PrivateKey.from_seed(1)

# generate private key from eth key path
PrivateKey.from_eth_keyfile('/path/to/the/key', 'password')

# generate public key from private key
PrivateKey.generate().get_public_key()

# generate public key from hex
PublicKey.from_hex(
    "04ad4793d81c5ee6c91c4baf2689c5299276c4774a8625fa87257f62ba8f3fe31f79d1351bd83af800afdaa94d40fe46c969f0ce2ac2e03e45d5a2d8a7687c39c0")

# generate public key from bytes
pub = PublicKey.from_bytes(
    b'\x04\xadG\x93\xd8\x1c^\xe6\xc9\x1cK\xaf&\x89\xc5)\x92v\xc4wJ\x86%\xfa\x87%\x7fb\xba\x8f?\xe3\x1fy\xd15\x1b\xd8:\xf8\x00\xaf\xda\xa9M@\xfeF\xc9i\xf0\xce*\xc2\xe0>E\xd5\xa2\xd8\xa7h|9\xc0')

# generate rev address from public key
pub.get_rev_address()
