import base64
import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_vapid_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )

    return {
        "publicKey": base64.urlsafe_b64encode(public_key_bytes).decode("utf-8").rstrip("="),
        "privateKey": base64.urlsafe_b64encode(private_key_bytes).decode("utf-8").rstrip("="),
    }

vapid_keys = generate_vapid_keys()
print("Public Key:", vapid_keys["publicKey"])
print("Private Key:", vapid_keys["privateKey"])
