# Appendices Content for AquaMark Academic Report

APPENDIX_A_TITLE = "Appendix A: Key Terms and Definitions"
APPENDIX_A_TEXT = """- 2D-DCT (Two-Dimensional Discrete Cosine Transform): A Fourier-related mathematical transform that expresses spatial image pixel variations as a linear combination of cosine basis functions oscillating at differing spatial frequencies.
- AES-256-GCM (Advanced Encryption Standard in Galois/Counter Mode): An authenticated symmetric block cipher combining counter-mode encryption with universal-hash-based Galois authentication tags using a 256-bit key and unique 96-bit nonces.
- Argon2id: The state-of-the-art hybrid password key derivation function recognized by the Password Hashing Competition. Combines Argon2i (side-channel resistance) and Argon2d (GPU/ASIC cracking resistance).
- BER (Bit Error Rate): The fraction of extracted watermark bits that differ from the originally embedded bit sequence, expressed as a percentage: BER = (Erroneous_Bits / Total_Bits) * 100%.
- Canonical JSON: A deterministic string representation of JSON data achieved by recursively sorting all dictionary keys in lexicographical order and removing all insignificant whitespace.
- Ed25519: An asymmetric Edwards-curve Digital Signature Algorithm operating over Curve25519 using SHA-512, providing 128-bit cryptographic security with 64-byte signatures.
- HMAC (Hash-based Message Authentication Code): A keyed cryptographic authentication mechanism calculated via HMAC(K, m) = H((K' ^ opad) || H((K' ^ ipad) || m)).
- Luminance (Y): The photometric measure of luminous intensity representing the grayscale brightness component of an image, separated from chrominance (Cb, Cr) color channels.
- Nonce (Number Used Once): An arbitrary number used exactly once in a cryptographic operation to prevent replay attacks and ensure identical plaintexts yield distinct ciphertexts.
- PSNR (Peak Signal-to-Noise Ratio): An engineering metric quantifying the fidelity between an original carrier image and a modified/watermarked image, defined in decibels (dB) as PSNR = 10 * log10(MAX_I^2 / MSE).
- Steganography: The scientific discipline and practice of concealing a secret message, identifier, or payload within an ordinary, non-secret carrier file such that the presence of the hidden data is imperceptible."""

APPENDIX_B_TITLE = "Appendix B: Core Algorithms Pseudocode"
APPENDIX_B_TEXT = """Algorithm 1: 2D-DCT Invisible Watermark Embedding
Input: carrier_image (PIL RGB), payload_text (str), embedding_strength (float = 18.0)
Output: watermarked_image (PIL RGB), bits_embedded (int)

1: ycrcb = carrier_image.convert('YCbCr')
2: y, cb, cr = ycrcb.split()
3: y_arr = numpy.array(y, dtype=float32)
4: preamble = [1, 0, 1, 0, 1, 1, 0, 0]
5: payload_bits = preamble + ascii_to_bits(payload_text)
6: pad payload_bits to 128 bits with zeros
7: h, w = y_arr.shape
8: blocks_h, blocks_w = h // 8, w // 8
9: bit_idx = 0
10: for bh from 0 to blocks_h - 1 do
11:     for bw from 0 to blocks_w - 1 do
12:         if bit_idx >= length(payload_bits) then break end if
13:         block = y_arr[bh*8 : bh*8+8, bw*8 : bw*8+8]
14:         d_block = scipy.fftpack.dct2(block, norm='ortho')
15:         c1 = d_block[3, 2]; c2 = d_block[2, 3]
16:         bit = payload_bits[bit_idx]
17:         if bit == 1 then
18:             if (c1 - c2) < embedding_strength then
19:                 d_block[3, 2] = (c1 + c2 + embedding_strength) / 2.0
20:                 d_block[2, 3] = (c1 + c2 - embedding_strength) / 2.0
21:             end if
22:         else
23:             if (c2 - c1) < embedding_strength then
24:                 d_block[3, 2] = (c1 + c2 - embedding_strength) / 2.0
25:                 d_block[2, 3] = (c1 + c2 + embedding_strength) / 2.0
26:             end if
27:         end if
28:         y_arr[bh*8 : bh*8+8, bw*8 : bw*8+8] = scipy.fftpack.idct2(d_block, norm='ortho')
29:         bit_idx = bit_idx + 1
30:     end for
31: end for
32: y_mod = PIL.Image.fromarray(clip(y_arr, 0, 255))
33: return PIL.Image.merge('YCbCr', (y_mod, cb, cr)).convert('RGB'), bit_idx

Algorithm 2: Cryptographic Manifest Creation and Ed25519 Signing
Input: original_sha256, protected_sha256, doc_id, issuer_id, private_key_pem
Output: canonical_manifest_json, base64_signature

1: manifest_dict = {
       "manifest_id": generate_uuid(),
       "document_id": doc_id,
       "original_sha256": original_sha256,
       "protected_sha256": protected_sha256,
       "hmac_sha256": hmac_sha256(secret_key, original_sha256 + ":" + protected_sha256),
       "watermark_algorithm": "DCT-SpreadSpectrum-v1",
       "issuer_id": issuer_id,
       "signing_key_id": "aquamark-root-authority-v1",
       "timestamp_utc": current_utc_iso_timestamp()
   }
2: canonical_bytes = json.dumps(manifest_dict, sort_keys=True, separators=(',', ':')).encode('utf-8')
3: private_key = load_ed25519_pem(private_key_pem)
4: signature_bytes = private_key.sign(canonical_bytes)
5: return json.dumps(manifest_dict, indent=2), base64_encode(signature_bytes)"""

APPENDIX_C_TITLE = "Appendix C: Test Case Execution Log"
APPENDIX_C_TEXT = """Detailed Execution Log from Automated Pytest Suite:

============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-9.1.1, pluggy-1.7.0 -- /Users/.../backend/venv/bin/python3.11
cachedir: .pytest_cache
rootdir: /Users/omsaishdhokchaule/Downloads/AquaMark/backend
plugins: anyio-4.15.1
collected 8 items

tests/test_api_integration.py::test_health PASSED                        [ 12%]
tests/test_api_integration.py::test_auth_workflow_and_security PASSED    [ 25%]
tests/test_api_integration.py::test_unauthorized_access_prevented PASSED [ 37%]
tests/test_crypto_watermark.py::test_sha256_consistency PASSED           [ 50%]
tests/test_crypto_watermark.py::test_hmac_sha256_verification PASSED     [ 62%]
tests/test_crypto_watermark.py::test_ed25519_digital_signature PASSED    [ 75%]
tests/test_crypto_watermark.py::test_authenticated_aes_gcm_encryption PASSED [ 87%]
tests/test_crypto_watermark.py::test_dct_invisible_watermark_pipeline PASSED [100%]

======================== 8 passed, 14 warnings in 1.23s ========================
Status: 100% Passed. Zero test failures."""

APPENDIX_D_TITLE = "Appendix D: User Manual and Operational Walkthrough"
APPENDIX_D_TEXT = """1. System Initialization:
   Execute the automated startup script: ./scripts/start.sh.
   Open a modern web browser and navigate to: http://localhost:3000.
2. User Registration and Access:
   Navigate to /register. Fill in Full Name, Institutional Affiliation, Email, and Master Password (min 8 characters).
   Upon submission, the user is authenticated and redirected to the Security Operation Center (/dashboard).
3. Ingesting Course Content:
   Navigate to /documents. Click the 'Upload PDF' button and select any standard course PDF (under 25 MB).
   The system extracts page count, computes original SHA-256 digest, and adds the document to the table.
4. Applying Watermark and Generating Signed Manifest:
   Click 'Apply Watermark' adjacent to the uploaded document.
   Choose either 'Visible Overlay' (configure watermark text and angle) or 'Invisible DCT' (enter payload and optional recipient ID).
   Click 'Generate Protected Copy'. The system embeds the watermark, computes hashes, signs the Ed25519 manifest, and logs the event.
5. Forensic Verification and Certification:
   Navigate to /verify. Drag and drop any candidate PDF suspected of alteration or unauthorized sharing.
   Click 'Run Forensic Evaluation'. The engine checks exact file hashes, validates digital signatures, and scans for 2D-DCT frequency watermarks.
   Click 'Download Official Certificate (PDF)' to obtain a stamped cryptographic audit report generated via ReportLab.
6. Empirical Robustness Experimentation:
   Navigate to /lab. Select a watermarked document, choose a distortion vector (JPEG Compression, Downscaling, Gaussian Noise, or Cropping), set attack intensity, and click 'Execute Robustness Test'.
   Review the calculated Peak Signal-to-Noise Ratio (PSNR in dB) and Bit Error Rate (BER)."""

APPENDIX_E_TITLE = "Appendix E: Installation and Execution Guide"
APPENDIX_E_TEXT = """Local Zero-Configuration Prerequisites:
- Python 3.11.x (with python3-venv and pip)
- Node.js v20+ / v24+ with npm v11+
- Git version control

Automated One-Click Startup:
$ cd /Users/omsaishdhokchaule/Downloads/AquaMark
$ chmod +x scripts/start.sh
$ ./scripts/start.sh

Manual Step-by-Step Execution:
Step 1: Backend Setup
$ cd backend
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ uvicorn app.main:app --host 0.0.0.0 --port 8000

Step 2: Frontend Setup
$ cd ../frontend
$ npm install
$ npm run dev -- --host 0.0.0.0 --port 3000

Step 3: Verification Endpoints
- Web Application: http://localhost:3000
- OpenAPI Interactive Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

Docker Containerized Deployment (Production):
$ docker compose up --build -d"""
