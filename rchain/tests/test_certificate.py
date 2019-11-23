import unittest

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509.oid import NameOID
from rchain.certificate import (
    generate_node_tls_key_cert_id, get_node_id_raw, get_node_tls_cert_pem,
    get_node_tls_cn, get_node_tls_key_pem,
)


class TestCertificate(unittest.TestCase):
    identities = [
        (
            b"""-----BEGIN PRIVATE KEY-----
MEECAQAwEwYHKoZIzj0CAQYIKoZIzj0DAQcEJzAlAgEBBCDgWIf2/YwI9Hfql9uz
vI7Q9rxtqFgD/v+xc6oCZHrG8A==
-----END PRIVATE KEY-----
""",
            b'\xf7\x08\x8duZ\xc1n\xa6\x11\xa4B\x89\x1a\xc0\x16\x0e\xde\t\x00\xa5',
            "f7088d755ac16ea611a442891ac0160ede0900a5",
        ),
        (
            b"""-----BEGIN PRIVATE KEY-----
MEECAQAwEwYHKoZIzj0CAQYIKoZIzj0DAQcEJzAlAgEBBCC9vPBp5CSZw2zs9lWn
MdjHRMlYWpo+ZYTWnnE0P2Mysg==
-----END PRIVATE KEY-----
""",
            b'\x900\xf1G/w\x91\x9bw@\xae\xa5\xb2\x05\xe3\x85qwK\x1d',
            "9030f1472f77919b7740aea5b205e38571774b1d",
        ),
        (
            b"""-----BEGIN PRIVATE KEY-----
MEECAQAwEwYHKoZIzj0CAQYIKoZIzj0DAQcEJzAlAgEBBCB47F2X0/9s3M5N5rKW
cHuiNCGoQZXxz82LhOLhUQaFmg==
-----END PRIVATE KEY-----
""",
            b'PJ\xdb\x8f\xdbj \xf5\xf0\x83\xdf\xd7a\x90\x16\x97Y\xd0\x0eu',
            "504adb8fdb6a20f5f083dfd76190169759d00e75",
        )
    ]

    def check_cert(self, actual_cert: x509.Certificate, expected_tls_cn: str):
        self.assertIsInstance(actual_cert.signature_hash_algorithm, hashes.SHA256)
        self.assertEqual(actual_cert.signature_algorithm_oid.dotted_string, '1.2.840.10045.4.3.2')  # ecdsa-with-sha256
        actual_issuer_cn = actual_cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        self.assertEqual(actual_issuer_cn, expected_tls_cn)
        actual_subject_cn = actual_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        self.assertEqual(actual_subject_cn, expected_tls_cn)

    def test_get_node_tls_key_pem(self):
        for private_key_pem, tls_cn_name, _ in self.identities:
            private_key = load_pem_private_key(private_key_pem, None, default_backend())
            self.assertEqual(private_key_pem.decode('utf8'), get_node_tls_key_pem(private_key))

    def test_get_node_tls_cn(self):
        for private_key_pem, expected_node_id_raw, expected_tls_cn in self.identities:
            private_key = load_pem_private_key(private_key_pem, None, default_backend())
            actual_node_id_raw = get_node_id_raw(private_key)
            actual_tls_cn = get_node_tls_cn(actual_node_id_raw)
            self.assertEqual(actual_node_id_raw, expected_node_id_raw)
            self.assertEqual(actual_tls_cn, expected_tls_cn)

    def test_get_node_tls_cert_pem(self):
        for private_key_pem, expected_node_id_raw, expected_tls_cn in self.identities:
            private_key = load_pem_private_key(private_key_pem, None, default_backend())
            cert_pem = get_node_tls_cert_pem(private_key)
            actual_cert = x509.load_pem_x509_certificate(cert_pem.encode('utf8'), default_backend())
            self.check_cert(actual_cert, expected_tls_cn)

    def test_generate_node_tls_key_cert_id(self):
        key_pem, cert_pem, node_id = generate_node_tls_key_cert_id()
        private_key = load_pem_private_key(key_pem.encode('utf8'), None, default_backend())
        cert = x509.load_pem_x509_certificate(cert_pem.encode('utf8'), default_backend())
        expected_tls_cn = get_node_tls_cn(get_node_id_raw(private_key))
        self.check_cert(cert, expected_tls_cn)
