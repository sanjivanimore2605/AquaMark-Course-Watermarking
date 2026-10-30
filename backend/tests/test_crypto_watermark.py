import os
import io
import pytest
from PIL import Image
from app.cryptography.engine import (
    calculate_sha256_bytes,
    calculate_hmac_sha256,
    verify_hmac_sha256,
    generate_ed25519_keypair,
    sign_canonical_manifest,
    verify_manifest_signature,
    encrypt_sensitive_metadata,
    decrypt_sensitive_metadata
)
from app.watermarking.invisible_dct import (
    text_to_bit_array,
    bit_array_to_text,
    embed_dct_watermark_image,
    extract_dct_watermark_image
)

def test_sha256_consistency():
    data = b"AquaMark Course Material 2026"
    h1 = calculate_sha256_bytes(data)
    h2 = calculate_sha256_bytes(data)
    assert h1 == h2
    assert len(h1) == 64
    # Check change avalanche effect
    h_modified = calculate_sha256_bytes(b"AquaMark Course Material 2027")
    assert h1 != h_modified

def test_hmac_sha256_verification():
    key = "super_secret_signing_key_32_bytes_len"
    msg = "original_sha256:protected_sha256:timestamp"
    h = calculate_hmac_sha256(key, msg)
    assert verify_hmac_sha256(key, msg, h) is True
    # Test modified message rejection
    assert verify_hmac_sha256(key, "tampered_msg", h) is False

def test_ed25519_digital_signature():
    priv_pem, pub_pem = generate_ed25519_keypair()
    manifest = {
        "manifest_id": "man_12345",
        "original_sha256": "abc12345",
        "protected_sha256": "def67890",
        "watermark_algorithm": "DCT-SpreadSpectrum-v1"
    }
    sig = sign_canonical_manifest(priv_pem, manifest)
    assert verify_manifest_signature(pub_pem, manifest, sig) is True
    
    # Tampering test
    tampered_manifest = manifest.copy()
    tampered_manifest["protected_sha256"] = "tampered_hash_value"
    assert verify_manifest_signature(pub_pem, tampered_manifest, sig) is False

def test_authenticated_aes_gcm_encryption():
    secret_text = "StudentID:CS-2026-99201;Email:alice@university.edu"
    ct, nonce = encrypt_sensitive_metadata(secret_text)
    decrypted = decrypt_sensitive_metadata(ct, nonce)
    assert decrypted == secret_text

def test_dct_invisible_watermark_pipeline():
    # Create test carrier image (e.g., simulated document canvas 256x256)
    img = Image.new("RGB", (256, 256), color=(240, 240, 240))
    payload = "AQ:CS-99"
    
    watermarked_img, num_bits = embed_dct_watermark_image(img, payload)
    assert num_bits > 0
    
    extracted, confidence = extract_dct_watermark_image(watermarked_img)
    assert extracted == payload
    assert confidence == 1.0
