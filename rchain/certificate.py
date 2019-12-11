import base64
from datetime import datetime, timedelta
from typing import Tuple

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
from eth_hash.auto import keccak


def get_node_tls_key_pem(key: ec.EllipticCurvePrivateKeyWithSerialization) -> str:
    b = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    return b.decode('ascii')


def get_node_id_raw(key: ec.EllipticCurvePrivateKeyWithSerialization) -> bytes:
    W = key.public_key().public_numbers()
    pk_bytes = W.x.to_bytes(32, 'big') + W.y.to_bytes(32, 'big')
    return keccak(pk_bytes)[12:]


def get_node_tls_cn(node_id_raw: bytes) -> str:
    return base64.b16encode(node_id_raw).decode('ascii').lower()


def get_node_tls_cert_pem(key: ec.EllipticCurvePrivateKeyWithSerialization) -> str:
    b = x509.CertificateBuilder()
    b = b.serial_number(x509.random_serial_number())
    b = b.public_key(key.public_key())
    node_id_raw = get_node_id_raw(key)
    cn = get_node_tls_cn(node_id_raw)
    x509_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn)])
    b = b.subject_name(x509_name)
    b = b.issuer_name(x509_name)

    now = datetime.now()
    b = b.not_valid_before(now - timedelta(days=1))
    b = b.not_valid_after(now + timedelta(days=365 * 10))

    cert = b.sign(
        private_key=key, algorithm=hashes.SHA256(), backend=default_backend())
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    return cert_pem.decode('ascii')


def generate_node_tls_key_cert_id() -> Tuple[str, str, str]:
    key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    key_pem = get_node_tls_key_pem(key)  # type: ignore
    node_id_raw = get_node_id_raw(key)  # type: ignore
    node_id = node_id_raw.hex()
    cert_pem = get_node_tls_cert_pem(key)  # type:ignore
    return key_pem, cert_pem, node_id
