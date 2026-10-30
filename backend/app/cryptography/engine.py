import os
import json
import hashlib
import hmac
import base64
from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import settings

def calculate_sha256(file_path: str) -> str:
    """Calculates SHA-256 hash of a file efficiently in 64KB blocks."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def calculate_sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def calculate_hmac_sha256(key: str, message: str) -> str:
    """HMAC-SHA-256 for integrity verification."""
    h = hmac.new(key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    return h.hexdigest()

def verify_hmac_sha256(key: str, message: str, expected_hmac: str) -> bool:
    actual = calculate_hmac_sha256(key, message)
    return hmac.compare_digest(actual, expected_hmac)

# Ed25519 Digital Signatures
def generate_ed25519_keypair() -> Tuple[str, str]:
    """Generates an Ed25519 keypair formatted in PEM."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("utf-8")
    
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")
    
    return priv_pem, pub_pem

def sign_canonical_manifest(private_key_pem: str, manifest_dict: Dict[str, Any]) -> str:
    """
    Signs a canonical JSON representation of the protection manifest.
    Canonicalization sorts keys and removes whitespace.
    """
    canonical_bytes = json.dumps(manifest_dict, sort_keys=True, separators=(',', ':')).encode("utf-8")
    private_key = serialization.load_pem_private_key(private_key_pem.encode("utf-8"), password=None)
    signature = private_key.sign(canonical_bytes)
    return base64.b64encode(signature).decode("utf-8")

def verify_manifest_signature(public_key_pem: str, manifest_dict: Dict[str, Any], signature_b64: str) -> bool:
    """Verifies an Ed25519 signature on canonical manifest bytes."""
    try:
        canonical_bytes = json.dumps(manifest_dict, sort_keys=True, separators=(',', ':')).encode("utf-8")
        signature = base64.b64decode(signature_b64)
        public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
        public_key.verify(signature, canonical_bytes)
        return True
    except Exception:
        return False

# Authenticated Encryption with AES-256-GCM
def encrypt_sensitive_metadata(data: str, key_32_bytes: bytes = None) -> Tuple[str, str]:
    """
    Encrypts string with AES-256-GCM using a 96-bit unique nonce.
    Returns (ciphertext_b64, nonce_b64)
    """
    if key_32_bytes is None:
        key_32_bytes = hashlib.sha256(settings.SECRET_KEY.encode("utf-8")).digest()
    
    aesgcm = AESGCM(key_32_bytes)
    nonce = os.urandom(12)  # 96-bit nonce
    ciphertext = aesgcm.encrypt(nonce, data.encode("utf-8"), None)
    return base64.b64encode(ciphertext).decode("utf-8"), base64.b64encode(nonce).decode("utf-8")

def decrypt_sensitive_metadata(ciphertext_b64: str, nonce_b64: str, key_32_bytes: bytes = None) -> str:
    if key_32_bytes is None:
        key_32_bytes = hashlib.sha256(settings.SECRET_KEY.encode("utf-8")).digest()
    
    aesgcm = AESGCM(key_32_bytes)
    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
    return decrypted_bytes.decode("utf-8")

# Default System Authority Key Management
SYSTEM_KEY_ID = "aquamark-root-authority-v1"
_system_priv_path = os.path.join(settings.KEYS_DIR, f"{SYSTEM_KEY_ID}.priv.pem")
_system_pub_path = os.path.join(settings.KEYS_DIR, f"{SYSTEM_KEY_ID}.pub.pem")

def get_or_create_system_keypair() -> Tuple[str, str]:
    if os.path.exists(_system_priv_path) and os.path.exists(_system_pub_path):
        with open(_system_priv_path, "r") as f:
            priv = f.read()
        with open(_system_pub_path, "r") as f:
            pub = f.read()
        return priv, pub
    
    priv, pub = generate_ed25519_keypair()
    with open(_system_priv_path, "w") as f:
        f.write(priv)
    with open(_system_pub_path, "w") as f:
        f.write(pub)
    return priv, pub
