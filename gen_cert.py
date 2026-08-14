"""
Run this once to generate a self-signed HTTPS certificate for the Air Mouse
server. Phones require HTTPS to grant access to motion sensors, so we need
a cert even though this never leaves your local network.

Usage:
    python gen_cert.py
"""

import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

BASE_DIR = Path(__file__).parent

def main():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "airmouse.local")])
    now = datetime.datetime.now(datetime.timezone.utc)

    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=3650))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("airmouse.local")]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    (BASE_DIR / "key.pem").write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    (BASE_DIR / "cert.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    print("Created cert.pem and key.pem in", BASE_DIR)
    print("Now run: python server.py")


if __name__ == "__main__":
    main()
