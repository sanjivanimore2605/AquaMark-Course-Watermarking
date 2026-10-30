# Chapters 1 to 4 Content for AquaMark Academic Report

CHAPTER_1_TITLE = "Chapter 1: Introduction"
CHAPTER_1_TEXT = """1.1 The Growth of Digital Educational Content
Over the past decade, and accelerated by remote and blended pedagogical models, higher education institutions have shifted decisively from printed course packets to digital distribution. Course content—including lecture slide presentations, detailed lecture notes, problem sets, programming laboratory manuals, grading rubrics, and high-stakes examination question papers—is overwhelmingly authored, distributed, and archived in the Portable Document Format (PDF). 

The ubiquitous adoption of PDF stems from its ability to preserve exact typographic layout, vector graphics, mathematical typesetting, and color schemes across disparate operating systems and viewing hardware. However, the very characteristics that make digital educational documents convenient—frictionless duplication, instantaneous network transmission, and zero degradation across direct byte-level copies—have introduced critical vulnerabilities for educational institutions and content creators.

1.2 Intellectual Property Risks and Academic Vulnerabilities
Educational course content embodies substantial institutional investment and faculty intellectual property. When distributed electronically without robust provenance and protection mechanisms, several prominent risks emerge:
1. Unauthorized Public Redistribution: Course materials uploaded to protected Learning Management Systems (LMS) are frequently downloaded by enrolled students and redistributed on commercial document-sharing repositories (e.g., Chegg, Course Hero, Studocu) or public social media platforms (e.g., Telegram channels, Reddit forums). In many instances, institutional headers and copyright notices are deliberately stripped before re-upload.
2. Examination and Assignment Leakage: High-stakes assessment instruments, including mid-semester examination papers and unreleased problem sets, can be leaked prior to or during evaluation windows, compromising institutional academic integrity.
3. Undetected Document Modification: Malicious or disingenuous actors may alter grading criteria, laboratory instructions, or exam dates within a distributed PDF and claim that the modified copy represents the authoritative institutional issuance.
4. Loss of Traceability: When a leaked document surfaces on an external website, standard file metadata (such as author name or creation timestamp) can be completely purged using free online utilities within seconds, leaving course administrators with no forensic link to the specific student or account from which the document originated.

1.3 Motivation Behind AquaMark
Conventional security controls applied to educational content exhibit severe engineering trade-offs:
- Pure Visual Watermarking: Printing a visible text watermark across document pages provides psychological deterrence. However, visual watermarks can be cropped from margins, masked with opaque white rectangles, or removed using automated PDF editing tools.
- Pure Cryptographic Hashing: Computing a Secure Hash Algorithm (such as SHA-256) over a PDF yields a 256-bit digest that detects any binary modification. However, cryptographic hashes are inherently brittle: if a student merely re-saves the PDF in a different PDF reader, opens and prints it to a virtual PDF driver, or recompresses embedded images, the binary hash changes entirely, producing a false-positive tampering alarm even when the underlying semantic content is completely untouched.
- Metadata Steganography: Hiding author or recipient information inside standard PDF metadata fields (/Info dictionary or XMP streams) is fragile; standard sanitization utilities strip metadata without modifying the visual document.

AquaMark is motivated by the realization that educational document protection requires a Layered Trust Architecture. Rather than relying on a single brittle technique, AquaMark coordinates visible vector watermarking for immediate deterrence, frequency-domain digital watermarking (2D-DCT steganography) for resilient leak tracing, and asymmetric digital signatures (Ed25519) combined with cryptographic manifests for mathematical integrity verification.

1.4 Scope and Operational Boundaries
The scope of the AquaMark platform encompasses:
- Secure ingestion, structural validation, and storage of educational PDF documents up to 100 pages and 25 MB.
- Application of customizable visible vector watermarks across all pages with controlled rotation, alpha opacity, and top security banners.
- Implementation of a discrete cosine transform (2D-DCT) steganographic pipeline embedding 128-bit payloads into mid-frequency luminance blocks of carrier pages with synchronization preambles.
- Cryptographic manifest generation, canonical JSON serialization, and Ed25519 digital signature signing.
- Detached and database-backed multi-path forensic verification yielding downloadable cryptographic certificate reports in PDF format.
- Tamper-evident chained audit logging utilizing SHA-256 block linking.
- An interactive empirical Robustness Testing Lab measuring Peak Signal-to-Noise Ratio (PSNR) and Bit Error Rate (BER).

Explicit Operational Boundaries:
AquaMark does not claim to prevent an authorized student from taking an analog photograph of a computer monitor (the "analog hole"), nor does it prevent manual re-typing of content. Furthermore, an Ed25519 digital signature verifies that a specific private key signed the manifest record; it does not constitute legal proof of original intellectual authorship prior to signing."""

CHAPTER_2_TITLE = "Chapter 2: Problem Statement and Objectives"
CHAPTER_2_TEXT = """2.1 Formal Problem Statement
Educational institutions lack an integrated, trustworthy, and verifiable system to protect electronic course content against unauthorized distribution, prove document authenticity, and trace leak sources across digital workflows without corrupting vector document geometry or producing false-positive tampering alarms.

Specifically, existing document distribution workflows fail to solve three interconnected challenges:
1. The Attribution Challenge: Identifying the specific recipient or account that leaked an authorized copy when visual notices have been erased or cropped.
2. The Integrity Challenge: Distinguishing between benign document re-compression (which preserves semantic authenticity) and malicious document modification (which alters academic content).
3. The Provenance Challenge: Providing mathematical non-repudiation that an institution issued a specific document at an authenticated timestamp without exposing master secret keys.

2.2 Primary Project Objectives
To address these challenges, AquaMark was developed with the following primary engineering objectives:
1. Design and Implement a Layered Document Protection Pipeline: Unify visible vector watermarking, invisible frequency steganography, and asymmetric digital signatures into a coherent, automated workflow.
2. Develop a Robust Invisible Watermarking Engine: Implement a 2D Discrete Cosine Transform (2D-DCT) pipeline capable of embedding recipient-specific identifiers into page luminance channels that survive lossy compression, format conversion, and moderate cropping.
3. Construct a Cryptographic Manifest and Signing Subsystem: Define a versioned, canonical JSON manifest schema signed via Ed25519 public-key cryptography to provide verifiable integrity and non-repudiation.
4. Build a Multi-Path Forensic Verification Center: Implement automated document inspection capable of reporting exact file matches, signature authenticity, and extracted steganographic payloads, culminating in official PDF verification certificates.
5. Create an Interactive Robustness Testing Lab: Provide an empirical laboratory within the user interface allowing users to subject watermarked documents to controlled attacks (JPEG compression, downscaling, noise, cropping) and measure quantitative metrics (PSNR and BER).
6. Implement Tamper-Evident Chained Audit Logging: Establish an immutable audit trail using SHA-256 hash chaining to track all administrative, watermarking, and verification operations.

2.3 Stakeholders and Intended Users
- University Instructors and Professors: Primary creators who upload syllabus files, problem sets, and exams; apply personalized watermarks; and verify candidate leaked files.
- Academic Administrators and Examination Boards: Authorities who audit institutional document records, investigate academic dishonesty, and issue certified forensic reports.
- Students and Authorized Learners: Legitimate recipients who access personalized, cryptographically watermarked copies for coursework.
- Forensic Verifiers and Employers: Third-party entities who verify the authenticity of academic transcripts, certificates, or course syllabi using the public verification portal.

2.4 Assumptions and Constraints
- Documents are provided in the standard ISO 32000-1 (PDF) specification.
- Uploaded files do not exceed 25 MB in size or 100 pages in length to protect server resources in typical educational environments.
- Server private keys are stored securely within isolated filesystem directories; hardware security module (HSM) integration represents future enterprise scope.
- In zero-docker local deployments, persistent data is maintained via SQLite, with seamless PostgreSQL support configured via Docker Compose."""

CHAPTER_3_TITLE = "Chapter 3: Literature Review and Existing Approaches"
CHAPTER_3_TEXT = """3.1 Survey of Document Protection Mechanisms
The field of electronic document security spans multiple distinct scientific domains across cryptography, information hiding, and access control. 

3.1.1 Visible Digital Watermarking
Visible watermarks overlay alphanumeric text, logos, or patterns directly over document pages. As articulated by Cox et al. [1], visible watermarks serve primarily as psychological deterrents. In digital documents, visible watermarks are commonly injected as vector text streams (e.g., using PDF operators such as Tj or TJ with graphics state transparency).
- Advantages: Immediately apparent to casual viewers; discourages overt screenshots; does not require specialized extraction software to convey ownership.
- Limitations: Highly susceptible to cropping, opacity reduction via PDF editing software, and localized content removal.

3.1.2 Invisible Digital Watermarking (Spatial vs. Frequency Domain)
Digital steganography and invisible watermarking embed information directly within carrier data representations:
1. Spatial Domain Techniques: Early techniques, such as Least Significant Bit (LSB) substitution [2], modify the lowest-order bits of pixel values. While computationally trivial and possessing high data payload capacity, spatial LSB watermarks are extremely fragile; standard JPEG re-compression or low-pass filtering completely destroys the embedded payload.
2. Frequency Domain Techniques: Transform-based methods project spatial pixels into orthogonal frequency representations using transforms such as the Discrete Cosine Transform (DCT) [3], Discrete Wavelet Transform (DWT) [4], or Discrete Fourier Transform (DFT). The 2D-DCT algorithm, foundational to the JPEG compression standard, separates image energy into low-, mid-, and high-frequency bands. Research by Podilchuk and Delp [5] established that embedding watermark energy into mid-frequency coefficients achieves an optimal trade-off: avoiding perceptible artifacts (which occur when low frequencies are altered) while surviving high-frequency quantization during lossy compression.

3.1.3 Cryptographic Hashing (SHA-256)
Cryptographic hash functions, standardized in NIST FIPS PUB 180-4 [6], map arbitrary binary inputs to fixed-length digests (256 bits for SHA-256). These functions guarantee pre-image resistance, second pre-image resistance, and collision resistance. While essential for establishing exact binary identity, cryptographic hashes are inherently brittle: any benign alteration of non-visual PDF metadata breaks the hash, rendering hash matching alone insufficient for real-world forensic verification.

3.1.4 Asymmetric Digital Signatures (Ed25519)
Digital signatures provide data integrity, authenticity, and non-repudiation. As formalized by Bernstein et al. [7], the Edwards-curve Digital Signature Algorithm (EdDSA) instantiated over Curve25519 (Ed25519) provides 128-bit cryptographic security equivalent to 3072-bit RSA. Ed25519 offers 64-byte signatures, rapid signature generation and verification, and resistance to side-channel timing attacks. In document workflows, digital signatures are applied to canonical manifests rather than entire raw files to decouple metadata verification from raster format changes.

3.1.5 Password Hashing Standards (Argon2id)
Legacy applications frequently employed MD5 or SHA-256 for password verification, exposing credentials to high-throughput GPU and ASIC dictionary attacks. The Password Hashing Competition selected Argon2 [8] as the modern standard. Its hybrid variant, Argon2id, combines data-independent memory access (resisting side-channel cache attacks) and data-dependent memory access (resisting GPU-accelerated brute-forcing).

3.2 Literature Comparison Table
The following matrix evaluates existing protection paradigms against AquaMark's multi-layered model:

+--------------------+---------------+-----------------+----------------+-----------------+
| Technology         | Visual Notice | Survives Lossy  | Non-Repudiation| Detects Single  |
|                    | (Deterrence)  | Compression     | (Authorship)   | Bit Alterations |
+--------------------+---------------+-----------------+----------------+-----------------+
| Visible Watermark  | YES           | NO (Croppable)  | NO             | NO              |
| Spatial LSB Stego  | NO            | NO (Fragile)    | NO             | NO              |
| Pure SHA-256 Hash  | NO            | NO (Brittle)    | NO             | YES             |
| Standalone Ed25519 | NO            | NO (Wrapper-dep)| YES            | YES (On Digest) |
| AquaMark Proposed  | YES           | YES (2D-DCT)    | YES (Ed25519)  | YES (SHA-256)   |
+--------------------+---------------+-----------------+----------------+-----------------+

3.3 Identified Research and Engineering Gap
While cryptographic signatures, hashing, and watermarking are individually well-studied, existing open-source and commercial solutions generally treat them as disjoint tools. Proprietary Digital Rights Management (DRM) software imposes intrusive client software, proprietary viewers, and restrictive key-exchange protocols that impede educational accessibility. Conversely, open-source PDF utilities lack cryptographic non-repudiation manifests and empirical robustness testing suites. AquaMark bridges this gap by engineering an open, standards-compliant, full-stack platform that unifies visible vector overlays, 2D-DCT frequency watermarking, Ed25519 signed manifests, and tamper-evident audit chaining within a single, cohesive architecture."""

CHAPTER_4_TITLE = "Chapter 4: Proposed System and Research Contribution"
CHAPTER_4_TEXT = """4.1 Proposed Layered Trust Architecture
AquaMark introduces a structured Layered Trust Architecture for educational document management. The architecture is organized into four foundational tiers:

1. Ingestion and Structural Normalization Tier:
Untrusted PDF files are validated structurally using PyMuPDF (fitz), verifying page counts, internal object streams, and file bounds (up to 25 MB). Files are assigned non-deterministic UUIDv4 storage names in isolated directories outside the web server root to prevent path traversal vulnerabilities.

2. Visual Deterrence and Identification Tier:
Applies customized vector overlays across all pages with user-configured rotation, font sizing, and alpha transparency. Top banner security notices are inserted to provide explicit copyright and institutional provenance notices.

3. Frequency-Domain Steganographic Embedding Tier:
Carrier pages are converted to the YCbCr color model at 150 DPI. The Luminance (Y) channel is partitioned into 8x8 blocks, transformed via 2D ortho-normalized DCT, and modulated at mid-frequency coefficient pairs (3,2) and (2,3) to embed a 128-bit payload prefixed by an 8-bit synchronization preamble [1,0,1,0,1,1,0,0].

4. Cryptographic Authentication and Provenance Tier:
A canonical JSON manifest is constructed, containing original and protected SHA-256 hashes, algorithm specifications, recipient identifiers, and timestamps. The manifest is signed with the server's Ed25519 private key. All operations are appended to an immutable audit ledger chained via SHA-256 hashes.

4.2 Scientific and Engineering Contributions
AquaMark contributes the following practical engineering integrations:
1. Dual-Domain Document Protection: Integrates spatial vector marking and frequency-domain DCT watermarking into a single execution pipeline, balancing human readability with algorithmic resilience.
2. Canonical Cryptographic Manifestation: Solves the brittle-hash dilemma by signing canonical serialized metadata that records both the original byte fingerprint and the watermarked output digest.
3. Empirical Robustness Evaluation Sandbox: Integrates an automated testing lab directly into the web application, providing instructors and evaluators with immediate, reproducible measurements of Peak Signal-to-Noise Ratio (PSNR) and Bit Error Rate (BER) across standard image transformations.
4. Tamper-Evident Chained Audit Provenance: Implements an internal blockchain-style hash chain ($H_i = \text{SHA-256}(H_{i-1} \parallel \text{Event})$) that prevents post-hoc log alteration or deletion."""
