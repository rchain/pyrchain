import unittest

from .crypto import blake2b_32


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
