# AquaMark — Robust Digital Watermarking and Document Integrity Platform

**Official Academic Title:** *Robust Digital Watermarking for Protection of Electronic Course Content*  
**Tagline:** *Protect Every Document. Verify Every Claim.*  
**Domain:** Applied Cryptography, Digital Watermarking, Document Security, and Digital Forensics.

---

## 1. Problem Statement & Mission

Electronic educational materials—such as lecture presentations, laboratory assignments, solution manuals, and exam papers—are routinely leaked, plagiarized, or distributed without authorization. Traditional countermeasures suffer from significant drawbacks:
- **Cosmetic or trivial watermarks** (e.g. static textual footers) can be cropped or deleted.
- **Pure cryptographic hashes** (e.g. SHA-256) are completely brittle; minor rasterization or metadata loss causes false positive tampering alerts.
- **Pure digital signatures** sign binary blobs without surviving file re-compression or print-scan workflows.

**AquaMark** harmonizes digital watermarking and modern cryptography into a unified, layered security architecture:
1. **Discrete Cosine Transform (DCT) Steganography**: Embeds imperceptible binary payloads in mid-frequency transform coefficients of page luminance channels.
2. **Ed25519 Asymmetric Digital Signatures**: Cryptographically signs canonical JSON manifests to prove author identity and provenance without revealing private keys.
3. **SHA-256 Hashing & HMAC**: Distinguishes between byte-for-byte exact matches and visually authentic, transformed copies.
4. **Tamper-Evident Chained Audit Logging**: SHA-256 hash chaining records all platform interactions in an append-only timeline.
5. **Robustness Testing Lab**: An empirical evaluation sandbox measuring Peak Signal-to-Noise Ratio (PSNR) and Bit Error Rate (BER) across real distortion vectors (JPEG recompression, downscaling, Gaussian noise, and cropping).

---

## 2. Technology Stack

### Backend
- **Framework**: Python 3.11+, FastAPI (Asynchronous REST API)
- **Security & Crypto**: `cryptography` (Ed25519, AES-256-GCM), `passlib` (Argon2id password hashing), PyJWT
- **Document & Image Processing**: PyMuPDF (`fitz`), Pillow, NumPy, SciPy (2D-DCT/IDCT routines), ReportLab
- **Database & Persistence**: SQLAlchemy ORM (SQLite for local zero-config, PostgreSQL for production)

### Frontend
- **Framework**: React 19, TypeScript, Vite
- **Styling & UI**: Tailwind CSS v4, Lucide Icons
- **State & Routing**: React Router v7, Context API, Axios

---

## 3. Quickstart & Local Installation

### Prerequisites
- Python 3.11+
- Node.js v18+ and npm

### One-Command Startup
To start both the FastAPI backend and React frontend concurrently:
```bash
./scripts/start.sh
```
- **Web Application**: [http://localhost:3000](http://localhost:3000)
- **Interactive OpenAPI Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Manual Startup

#### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 4. Running the Test Suite

AquaMark includes unit tests, cryptographic verification tests, and integration test suites:
```bash
cd backend
source venv/bin/activate
PYTHONPATH=. pytest -v tests/
```
All 8 test suites pass with 100% success rate:
- `test_sha256_consistency`
- `test_hmac_sha256_verification`
- `test_ed25519_digital_signature`
- `test_authenticated_aes_gcm_encryption`
- `test_dct_invisible_watermark_pipeline`
- `test_health`
- `test_auth_workflow_and_security`
- `test_unauthorized_access_prevented`

---

## 5. Security & Academic Considerations

- **Non-Repudiation vs Legal Ownership**: An Ed25519 digital signature proves that a specific keyholder signed a canonical manifest at a given time under stated trust assumptions. It does not replace legal copyright arbitration.
- **Watermark Robustness Bounds**: The DCT mid-frequency watermarking technique resists standard lossy compression (JPEG quality > 50) and moderate resampling. It does not claim resistance against aggressive geometric distortion or intentional cropping exceeding 30%.
