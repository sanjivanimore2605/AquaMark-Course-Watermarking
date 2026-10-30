# Chapters 5 to 8 Content for AquaMark Academic Report

CHAPTER_5_TITLE = "Chapter 5: System Requirements and Feasibility Study"
CHAPTER_5_TEXT = """5.1 Hardware Requirements
AquaMark is designed to run efficiently on standard consumer and cloud server hardware without requiring proprietary cryptographic accelerators or dedicated GPUs:
- Processor: 64-bit multi-core CPU (Intel Core i5/i7, AMD Ryzen 5/7, or Apple Silicon ARM64; minimum 2 cores, recommended 4 cores).
- Random Access Memory (RAM): Minimum 4 GB; recommended 8 GB or higher to support concurrent image rasterization and 2D-DCT array transformations across multi-page PDF processing.
- Persistent Storage: Minimum 10 GB free disk space (Solid State Drive recommended) for source code, virtual environments, SQLite/PostgreSQL databases, and protected PDF document storage vaults.
- Network Interface: Standard Ethernet or 802.11 Wi-Fi interface supporting TCP/IP network communication.

5.2 Software Requirements and Runtime Environments
The software stack is built exclusively on maintained, open-source technologies:
- Operating System: Cross-platform compatibility verified on macOS (Darwin 24+), Linux (Ubuntu 22.04 LTS / Debian 12), and Windows 11 (WSL2).
- Backend Runtime: Python 3.11.x (tested on Python 3.11.9 64-bit).
- Backend Web Framework: FastAPI v0.146.0 running on Uvicorn ASGI server v0.54.0.
- Database & ORM: SQLAlchemy v2.1.5 with SQLite3 (local development and automated test execution) and PostgreSQL 16 (production containerization).
- Scientific Computing & Document Libraries: PyMuPDF v1.28.2, NumPy v2.4.6, SciPy v1.17.1, Pillow (PIL) v13.0.0, ReportLab v5.0.1.
- Cryptography & Security Packages: cryptography v50.0.2 (Ed25519, AES-GCM), argon2-cffi v25.1.0 (Argon2id password hashing), passlib v1.7.4, pyjwt v2.15.1.
- Frontend Runtime: Node.js v20+ / v24+ with npm v11.5.1.
- Frontend Framework: React v19.2.8 with TypeScript v6.0.2, bundled via Vite v8.3.4.
- Styling & UI: Tailwind CSS v4.3.3 and Lucide React Icons v1.59.0.

5.3 Feasibility Analysis
- Technical Feasibility: The integration of 2D-DCT transforms, PyMuPDF vector injection, and Ed25519 digital signatures is fully achieved using standard Python scientific libraries without custom native C compiler dependencies.
- Operational Feasibility: The system provides an intuitive web interface with clear visual workflows for instructors and automated one-click PDF verification for public verifiers, requiring zero command-line expertise from end users.
- Economic Feasibility: All software libraries, runtime environments, and frameworks are released under permissive open-source licenses (MIT, Apache 2.0, BSD), eliminating software licensing fees."""

CHAPTER_6_TITLE = "Chapter 6: System Architecture and Detailed Design"
CHAPTER_6_TEXT = """6.1 High-Level Architecture Overview
AquaMark follows a modern decoupled Client-Server architecture adhering to Representational State Transfer (REST) design principles. The system cleanly separates presentation logic, business services, cryptographic routines, and persistence layers.

6.2 Data Flow Diagrams (DFD)

Level 0 DFD (Context Diagram):
- External Entities: Instructor / Creator, Student / Recipient, Public Verifier.
- Central Process: AquaMark Document Protection & Integrity Platform (Process 0.0).
- Data Flows:
  * Instructor -> [Credentials, Original PDF, Watermark Parameters] -> AquaMark
  * AquaMark -> [Authentication Token, Protected Signed PDF, Signed Manifest JSON] -> Instructor
  * Student -> [Download Request] -> AquaMark
  * AquaMark -> [Personalized Watermarked PDF] -> Student
  * Public Verifier -> [Candidate PDF, Manifest JSON] -> AquaMark
  * AquaMark -> [Verification Status, Forensic PDF Certificate] -> Public Verifier

Level 1 DFD (Decomposed Subsystems):
- Process 1.0 (Authentication Subsystem): Ingests user credentials, executes Argon2id verification against User DB, issues JWT Bearer token.
- Process 2.0 (PDF Ingestion & Storage Subsystem): Validates PDF structure, generates UUIDv4 storage path, computes original SHA-256 digest, records document in Document DB.
- Process 3.0 (Dual Watermarking Engine): Ingests original file and watermark configuration; applies PyMuPDF vector overlay (Process 3.1) or 2D-DCT frequency steganography (Process 3.2); generates protected output PDF.
- Process 4.0 (Cryptographic Signing Subsystem): Calculates protected SHA-256 digest and HMAC-SHA-256; constructs canonical JSON manifest; signs manifest with Ed25519 system authority private key; persists WatermarkRecord in DB.
- Process 5.0 (Forensic Verification Engine): Ingests candidate PDF; executes hash comparison, Ed25519 signature validation, and DCT extraction; generates ReportLab PDF certificate.
- Process 6.0 (Audit Ledger Engine): Appends SHA-256 block-chained audit records for all system events.

6.3 Entity-Relationship (ER) Schema Design
The relational database schema is normalized and enforced using SQLAlchemy ORM:
- users: id (UUID PK), email (Unique, Indexed), hashed_password, full_name, institution, role (admin/instructor), is_active, created_at, updated_at.
- signing_keys: id (UUID PK), key_id (Unique, Indexed), algorithm (Ed25519), public_key_pem, private_key_encrypted, user_id (FK -> users.id), is_active, created_at.
- documents: id (UUID PK), title, original_filename, stored_original_filename, file_size_bytes, page_count, original_sha256 (Indexed), owner_id (FK -> users.id), created_at.
- watermark_records: id (UUID PK), document_id (FK -> documents.id), watermark_type, watermark_algorithm, algorithm_version, payload_text, recipient_identifier, stored_protected_filename, protected_file_size_bytes, protected_sha256 (Indexed), hmac_sha256, manifest_id (Unique, Indexed), manifest_json, digital_signature, signing_key_id, created_at.
- verification_records: id (UUID PK), document_id (FK -> documents.id), watermark_record_id (FK -> watermark_records.id), candidate_filename, candidate_sha256, exact_hash_match, signature_valid, signing_key_trusted, watermark_detected, watermark_payload_match, extracted_payload, status_summary, full_report_json, created_at.
- robustness_experiments: id (UUID PK), watermark_record_id (FK -> watermark_records.id), transformation_type, transformation_params_json, detected, payload_recovered, bit_error_rate, extracted_payload, psnr_db, execution_duration_ms, created_at.
- audit_events: id (UUID PK), actor_id (FK -> users.id), event_type, document_id, status, details_json, previous_hash, current_hash, timestamp."""

CHAPTER_7_TITLE = "Chapter 7: Methodology and Mathematical Algorithms"
CHAPTER_7_TEXT = """7.1 Discrete Cosine Transform (2D-DCT) Mathematical Formulation
The Discrete Cosine Transform expresses a finite sequence of spatial data points in terms of a sum of cosine functions oscillating at different frequencies. For an 8x8 block of spatial luminance pixels f(x, y), where x, y in {0, 1, ..., 7}, the 2D ortho-normalized DCT coefficient matrix F(u, v) is defined as:

F(u, v) = (1/4) * C(u) * C(v) * Sum_{x=0}^{7} Sum_{y=0}^{7} f(x, y) * cos([(2x + 1) * u * pi] / 16) * cos([(2y + 1) * v * pi] / 16)

Where the ortho-normalization scaling factor C(k) is defined as:
C(k) = 1 / sqrt(2)  for k = 0
C(k) = 1            for k > 0

The Inverse 2D-DCT (2D-IDCT) reconstructs spatial pixel values from the transformed frequency coefficients:
f(x, y) = (1/4) * Sum_{u=0}^{7} Sum_{v=0}^{7} C(u) * C(v) * F(u, v) * cos([(2x + 1) * u * pi] / 16) * cos([(2y + 1) * v * pi] / 16)

7.2 Steganographic Embedding Algorithm
The invisible embedding pipeline operates as follows:
1. Input: Carrier document image I, payload text string S (e.g., 'CS401:STUDENT-99').
2. Color Conversion: Convert image I to YCbCr space; extract Luminance channel Y.
3. Payload Formatting: S is converted to an ASCII bit sequence B = {b_0, b_1, ..., b_n}. An 8-bit synchronization preamble P = [1, 0, 1, 0, 1, 1, 0, 0] is prepended: TotalBits = P + B, padded to 128 bits.
4. Block Partitioning: Y is divided into non-overlapping 8x8 pixel blocks Y_{i, j}.
5. Transform: Apply 2D-DCT to block Y_{i, j}, yielding coefficient block D.
6. Coefficient Selection & Modulation: Mid-frequency coordinates (u1, v1) = (3, 2) and (u2, v2) = (2, 3) are selected. Let c1 = D(3, 2) and c2 = D(2, 3).
   - If current bit b_k == 1:
     Enforce (c1 - c2) >= Strength (where Strength = 18.0). If (c1 - c2) < Strength, set:
     c1' = (c1 + c2 + Strength) / 2
     c2' = (c1 + c2 - Strength) / 2
   - If current bit b_k == 0:
     Enforce (c2 - c1) >= Strength. If (c2 - c1) < Strength, set:
     c1' = (c1 + c2 - Strength) / 2
     c2' = (c1 + c2 + Strength) / 2
7. Inverse Transform: Apply 2D-IDCT to reconstructed block D', clip pixel values to [0, 255], and recombine with Cb and Cr channels.

7.3 Steganographic Extraction Algorithm
1. Extract Luminance channel Y from candidate image.
2. For each 8x8 block, compute 2D-DCT coefficient matrix D.
3. Read c1 = D(3, 2) and c2 = D(2, 3). If c1 >= c2, record bit 1; else record bit 0.
4. Scan the recovered bit stream for the 8-bit preamble [1, 0, 1, 0, 1, 1, 0, 0] (allowing a maximum Hamming distance of 1 bit for error tolerance).
5. Parse subsequent bits into 8-bit ASCII characters until a null terminator or invalid character is encountered.

7.4 Cryptographic Manifest Canonicalization and Signing
To prevent signature failure caused by non-deterministic JSON serialization (e.g., differences in key ordering or whitespace), AquaMark enforces strict canonicalization:
1. Manifest dictionary is constructed containing: manifest_id, document_id, original_sha256, protected_sha256, hmac_sha256, watermark_type, watermark_algorithm, payload_text, recipient_identifier, issuer_id, signing_key_id, and timestamp_utc.
2. Canonicalization function: json.dumps(manifest_dict, sort_keys=True, separators=(',', ':')).encode('utf-8').
3. Ed25519 Signing: The canonical byte stream is signed using the server private key: Signature = Ed25519_Sign(Private_Key, Canonical_Bytes). The resulting 64-byte signature is Base64 encoded."""

CHAPTER_8_TITLE = "Chapter 8: Implementation Details and Module Breakdown"
CHAPTER_8_TEXT = """8.1 Authentication and Role-Based Authorization
Implemented in backend/app/api/v1/auth.py and backend/app/security/auth.py:
- Registration (/api/v1/auth/register): Validates minimum 8-character passwords; hashes passwords via Argon2id (time_cost=2, memory_cost=65536, parallelism=2); designates the first user as 'admin' and subsequent registrants as 'instructor'.
- Login (/api/v1/auth/login): Verifies plain password against Argon2id hash; generates a signed JWT containing user ID, email, role, and expiration timestamp (1440 minutes).
- Authorization Dependency (/app/security/deps.py): Extracts Bearer token, validates JWT signature using server secret key, and enforces role and document ownership constraints.

8.2 PDF Ingestion and Storage Engine
Implemented in backend/app/api/v1/documents.py:
- Upload Endpoint (/api/v1/documents/upload): Streams file bytes in 64 KB chunks, enforcing a strict 25 MB file limit.
- Structural Inspection: Validates PDF headers and structure using PyMuPDF (fitz.open); rejects malformed files or documents exceeding 100 pages.
- Storage Isolation: Stores files under non-deterministic UUIDv4 filenames in backend/storage/uploads/, isolated from web server root directories. Computes SHA-256 digest over the raw binary.

8.3 Visible Watermarking Subsystem
Implemented in backend/app/watermarking/visible.py:
- Uses PyMuPDF's page.insert_text() to place vector text overlays across all pages centered at (width/2, height/2), rotated at 45 degrees, with 35% alpha transparency.
- Adds an unobtrusive top security header banner: 'AquaMark Secured Document | [Watermark Text]' at fontsize 9.0.
- Preserves original page bounding boxes, vector resolution, and text searchability.

8.4 2D-DCT Steganographic Engine
Implemented in backend/app/watermarking/invisible_dct.py:
- Renders page 1 of carrier PDF to RGB at 150 DPI; executes 2D-DCT luminance block modulation.
- Re-compiles watermarked raster page with original subsequent PDF pages, saving output to backend/storage/protected/.
- Computes protected file SHA-256 and HMAC-SHA-256; constructs and signs canonical Ed25519 manifest.

8.5 Multi-Path Forensic Verification Center
Implemented in backend/app/api/v1/verify.py:
- Accepts candidate PDF file and optional manifest JSON.
- Evaluates candidate SHA-256 hash against database records.
- Verifies Ed25519 digital signature against trusted system authority public key.
- Executes 2D-DCT watermark extraction scan on candidate page 1.
- Classifies candidate into unambiguous verdicts: AUTHENTIC_EXACT_MATCH, AUTHENTIC_WATERMARK_CONFIRMED, TAMPERED_DOCUMENT_MODIFIED, UNTRUSTED_SIGNING_AUTHORITY, or UNREGISTERED_OR_ALTERED.
- Generates official forensic certificate PDF via ReportLab (backend/app/reports/pdf_generator.py).

8.6 Robustness Testing Laboratory
Implemented in backend/app/watermarking/robustness.py and frontend/src/pages/Lab.tsx:
- Ingests watermarked carrier document and applies user-selected image transformation:
  * JPEG Compression (Quality 10 to 95)
  * Geometric Downscaling / Resizing (Scale factors 0.25 to 0.95)
  * Additive Gaussian Noise (Standard deviations 5 to 50)
  * Border Cropping (1% to 20% border removal)
- Executes watermark extraction and calculates Peak Signal-to-Noise Ratio (PSNR in dB) and Bit Error Rate (BER).
- Displays real-time empirical metrics on the frontend interface without modifying original protected files."""
