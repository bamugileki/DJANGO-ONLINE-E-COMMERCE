from datetime import datetime, timedelta, timezone
import ipaddress
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from django.core.management.base import BaseCommand
from django.conf import settings
import socket
import os


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


class Command(BaseCommand):
    help = 'Generate a self-signed SSL certificate with the local IP as SAN'

    def handle(self, *args, **options):
        project_dir = settings.BASE_DIR
        cert_path = os.path.join(project_dir, 'server.crt')
        key_path = os.path.join(project_dir, 'server.key')

        local_ip = get_local_ip()
        self.stdout.write(f"Detected local IP: {local_ip}")

        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        with open(key_path, 'wb') as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, 'KE'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Nairobi'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, 'Nairobi'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'mimicME'),
            x509.NameAttribute(NameOID.COMMON_NAME, local_ip),
        ])

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.now(timezone.utc))
            .not_valid_after(datetime.now(timezone.utc) + timedelta(days=3650))
            .add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName('localhost'),
                    x509.DNSName('127.0.0.1'),
                    x509.IPAddress(ipaddress.IPv4Address(local_ip)),
                ]),
                critical=False,
            )
            .sign(key, hashes.SHA256(), backend=default_backend())
        )

        with open(cert_path, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        self.stdout.write(self.style.SUCCESS(f"Certificate: {cert_path}"))
        self.stdout.write(self.style.SUCCESS(f"Key: {key_path}"))
        self.stdout.write(self.style.SUCCESS(f"IP in SAN: {local_ip}"))
        self.stdout.write("")
        self.stdout.write("Run server with:")
        self.stdout.write(
            f"  python manage.py runsslserver "
            f"--certificate {cert_path} "
            f"--key {key_path} "
            f"0.0.0.0:8000"
        )
