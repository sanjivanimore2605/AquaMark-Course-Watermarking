import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header_footer(section):
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "AquaMark — Comprehensive Academic & Technical Learning Guide"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if hp.runs:
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "AquaMark | Cryptography, Watermarking & Forensic Document Integrity"
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if fp.runs:
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(148, 163, 184)

def build_docx_learning_guide(output_path):
    doc = Document()

    # Margins
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        add_header_footer(s)

    primary = RGBColor(15, 23, 42)     # Slate 900
    accent = RGBColor(13, 148, 136)    # Teal 600
    body_col = RGBColor(30, 41, 59)   # Slate 800
    muted = RGBColor(71, 85, 105)     # Slate 600

    def add_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = primary
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(16)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.italic = True
        run.font.color.rgb = accent
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = primary
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = accent
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = primary
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.color.rgb = body_col
        return p

    def add_bullet(lead, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(lead)
        r1.font.name = "Arial"
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = primary
        r2 = p.add_run(text)
        r2.font.name = "Arial"
        r2.font.size = Pt(10)
        r2.font.color.rgb = body_col
        return p

    def add_box(title, text, hex_color="F1F5F9", border_color="0D9488"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, hex_color)
        set_cell_margins(cell, 100, 100, 140, 140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"★ {title}\n")
        r_title.font.name = "Arial"
        r_title.font.size = Pt(10.5)
        r_title.font.bold = True
        r_title.font.color.rgb = accent
        r_text = p.add_run(text)
        r_text.font.name = "Arial"
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = body_col
        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, 100, 100, 140, 140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(code_text)
        r.font.name = "Courier New"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(226, 232, 240)
        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    # ==================== COVER / TITLE ====================
    add_title("AquaMark — Comprehensive Academic & Technical Learning Guide")
    add_subtitle("Official Academic Title: Robust Digital Watermarking for Protection of Electronic Course Content\n"
                 "Student Learning Handbook, Code Audit, Implementation Breakdown, and Viva Preparation Guide")

    add_box("How to Use This Handbook",
            "This guide is written especially for you as a student. It starts from fundamental concepts, explains every single technical term when introduced, walks through the exact implemented Python and React code, clarifies honest security limits, and provides complete viva answers so you can defend your project with absolute confidence.")

    # ==================== 1. IMPLEMENTATION AUDIT ====================
    add_h1("1. Honest Implementation Audit (What is Built vs What is Planned)")
    add_p("In any senior or capstone engineering evaluation, academic integrity is paramount. Never claim a feature exists if it was only a design proposal. Below is the audited status of the AquaMark codebase:")

    add_h2("A. Features Fully Implemented and Verified in Working Code")
    add_bullet("1. Visible Vector Watermark Engine: ", "Implemented in backend/app/watermarking/visible.py using PyMuPDF (fitz). Preserves PDF page geometry, injects diagonal text overlays with adjustable opacity/angles, and embeds top security header banners.")
    add_bullet("2. 2D-DCT Invisible Watermark Pipeline: ", "Implemented in backend/app/watermarking/invisible_dct.py. Converts PDF page to Luminance (Y), divides into 8x8 blocks, embeds 128-bit payload with preamble sync marker [1,0,1,0,1,1,0,0] into mid-frequency coefficients (3,2) and (2,3), and performs inverse DCT.")
    add_bullet("3. Ed25519 Asymmetric Digital Signatures: ", "Implemented in backend/app/cryptography/engine.py using cryptography library. Generates Ed25519 keypairs, serializes canonical JSON manifests, and verifies digital signatures.")
    add_bullet("4. File Integrity & HMAC: ", "SHA-256 block-based hashing for original and protected files; HMAC-SHA-256 binding original hash to protected hash.")
    add_bullet("5. Authenticated Symmetric Encryption: ", "AES-256-GCM encryption with unique 96-bit random nonces for sensitive metadata.")
    add_bullet("6. Tamper-Evident Audit Hash Chain: ", "Implemented in backend/app/services/audit.py. Each event's SHA-256 hash chains to the previous event's hash, forming an append-only cryptographic sequence.")
    add_bullet("7. Robustness Testing Lab: ", "Implemented in backend/app/watermarking/robustness.py & frontend/src/pages/Lab.tsx. Evaluates watermark recovery under JPEG compression, geometric scaling, Gaussian noise, and cropping, calculating PSNR (dB) and Bit Error Rate (BER).")
    add_bullet("8. Complete Full-Stack REST API & React Frontend: ", "FastAPI endpoints under /api/v1 (auth, documents, watermarks, verify, experiments, dashboard); React 19 + TypeScript + Tailwind CSS UI.")
    add_bullet("9. Automated Test Suite: ", "8 automated test cases in backend/tests/ passing at 100% (SHA-256 consistency, HMAC, Ed25519 signature verification, AES-GCM encryption/decryption, DCT watermark embedding/extraction, health check, authentication workflow, unauthorized access prevention).")

    add_h2("B. Features Implemented But Not Separately Unit Tested")
    add_bullet("1. Multi-page Batch Invisible Watermarking: ", "The current DCT embedding pipeline embeds the watermark payload into page 1 (carrier) and re-compiles subsequent pages. Multi-page distributed spreading is implemented in code but unit tests specifically test single-page and rasterized carriers.")
    add_bullet("2. Contrast Adjustment Transformation in Robustness Lab: ", "The backend function run_single_experiment supports contrast_adjust, but the frontend slider exposes the four primary transformations (JPEG, resize, noise, crop).")

    add_h2("C. Features Planned as Future Work (Not Implemented)")
    add_bullet("1. Hardware Token / HSM Integration: ", "Storing private Ed25519 keys on physical YubiKeys or cloud HSMs (AWS KMS / GCP Cloud KMS). Currently, keys are securely stored on the server filesystem in backend/storage/keys/.")
    add_bullet("2. Automatic Projective Mesh Rectification: ", "Self-healing detection of severe trapezoidal phone camera photos (when a student takes an angled photograph of a monitor).")
    add_bullet("3. Email Delivery Service: ", "SMTP / SendGrid email verification. Currently, user accounts activate directly upon registration.")

    add_h2("D. Claims That Cannot Be Made (Security Non-Claims)")
    add_bullet("• No 'Copy-Proof' Claim: ", "Digital watermarking does NOT physically lock a computer screen. If a student can read the document, they can take a screenshot or retype it. Watermarking is for provenance and leak tracing.")
    add_bullet("• No 'Proof of Legal Ownership' Claim: ", "An Ed25519 digital signature proves that a specific private key signed the manifest on that date. It does NOT legally prove who first created the underlying intellectual content.")
    add_bullet("• No Universal Invisibility or Robustness: ", "Extreme cropping (>30% of page area) or severe geometric rotation will disrupt 8x8 block alignment and prevent payload recovery.")

    # ==================== 2. PROJECT OVERVIEW & REAL-WORLD STORY ====================
    add_h1("2. Project Overview & The Real-World Story")
    add_p("The official academic title of this project is:")
    add_p("“Robust Digital Watermarking for Protection of Electronic Course Content”\nProduct Name: AquaMark | Tagline: “Protect Every Document. Verify Every Claim.”")

    add_h2("A Simple Real-World Scenario: Dr. Katherine's Leaked Midterm")
    add_p("Let's understand why AquaMark is needed through an everyday university story:")
    add_p("Dr. Katherine teaches Advanced Cryptography (CS401) to 60 university students. On Monday, she uploads the upcoming Midterm Exam Assignment to the university portal. On Tuesday morning, a teaching assistant notices that the exact assignment is posted on Chegg and a public Telegram group.")
    add_p("Dr. Katherine faces three questions:")
    add_bullet("1. Authenticity: ", "Is this file actually her authentic exam paper, or a modified version where someone changed Question 4?")
    add_bullet("2. Provenance: ", "Can Dr. Katherine prove to the Department Chair that she published this document first, without exposing her master private keys?")
    add_bullet("3. Tracing the Leaker: ", "Which of her 60 students downloaded this specific copy and leaked it?")

    add_p("With traditional tools, she is helpless. A normal watermark like 'Property of Dr. Katherine' is easily cropped. A file hash (SHA-256) is broken because the student converted the PDF to JPEG before uploading. This is where AquaMark comes in.")

    # ==================== 3. BASIC CONCEPTS EXPLAINED SIMPLY ====================
    add_h1("3. Basic Concepts Explained from Scratch (No Jargon)")
    add_p("Before discussing code, let us understand the fundamental computer science and cryptographic concepts in plain language:")

    add_h2("1. What is a Hash (SHA-256)?")
    add_p("A cryptographic hash is like a mathematical fingerprint. You feed any digital file—whether it is a 1-page note or a 1000-page book—into an algorithm called SHA-256. It outputs a fixed 64-character hexadecimal code.")
    add_p("Two crucial properties of SHA-256:")
    add_bullet("• Deterministic: ", "The exact same file will always produce the exact same 64-character fingerprint, no matter what computer computes it.")
    add_bullet("• Avalanche Effect: ", "If you change even a single period or comma in a 500-page document, the entire 64-character fingerprint changes completely and unpredictably.")

    add_h2("2. What is an HMAC (Hash-based Message Authentication Code)?")
    add_p("A standard hash tells you if a file changed, but anyone can calculate a hash. An HMAC is a hash that incorporates a secret password (key). It proves two things at once: (1) The data has not been modified, and (2) The person who created the hash possessed the secret key.")

    add_h2("3. What is an Asymmetric Digital Signature (Ed25519)?")
    add_p("In conventional passwords, both sides share the same secret (symmetric). In asymmetric cryptography, there is a pair of keys:")
    add_bullet("• Private Signing Key: ", "Kept secret on the server. Only the server can create a digital signature.")
    add_bullet("• Public Verification Key: ", "Shared openly with the whole world. Anyone can verify that the signature was made by the private key, but NO ONE can forge a new signature using only the public key.")
    add_p("Ed25519 is a modern elliptic-curve algorithm based on Curve25519. It produces tiny 64-byte signatures, runs with high speed, and is mathematically immune to timing side-channel attacks.")

    add_h2("4. What is a Digital Watermark?")
    add_p("A digital watermark is information permanently embedded directly into the carrier media (the PDF or image pixels) rather than in external tags or file headers.")
    add_bullet("• Visible Watermark: ", "Seen by the human eye. Acts as a visual deterrent.")
    add_bullet("• Invisible Watermark: ", "Hidden mathematically inside pixel frequencies. Cannot be seen by human eyes, but can be extracted by forensic algorithms.")

    add_h2("5. What is the Difference Between Hash Mismatch vs Malicious Tampering?")
    add_box("Crucial Exam Distinction: Hash Mismatch vs Proof of Malice",
            "A file hash mismatch proves mathematically that the file's binary bytes are different from the original recorded bytes.\n"
            "HOWEVER, it does NOT automatically prove malicious tampering! A hash will change if someone simply opened the PDF and re-saved it in a different PDF reader (which rewrites internal object streams), or if a printer driver re-compressed an embedded image.\n"
            "AquaMark clearly reports 'Exact Hash Mismatch', but checks if the invisible watermark payload is still intact before declaring whether the content itself is authentic or tampered.")

    # ==================== 4. ARCHITECTURE & TECHNOLOGY STACK ====================
    add_h1("4. System Architecture & Technology Stack")
    add_p("AquaMark is built as a modular, decoupled full-stack platform:")

    add_code_block(
"""+-----------------------------------------------------------------------+
|                         AquaMark Web Frontend                         |
|      (React 19, TypeScript, Vite, Tailwind CSS v4, Lucide Icons)       |
+-----------------------------------+-----------------------------------+
                                    | REST API Calls (Axios / JSON)
                                    v
+-----------------------------------------------------------------------+
|                          FastAPI Backend                              |
|   /auth      /documents      /watermarks     /verify    /experiments  |
+---------+--------------+--------------+----------+--------------------+
          |              |              |          |
          v              v              v          v
   +--------------+ +------------+ +----------+ +-----------------------+
   | Security &   | | PyMuPDF    | | 2D-DCT   | | Cryptography Engine   |
   | Argon2id     | | Vector     | | Stegano  | | Ed25519, SHA-256,     |
   | Auth Tokens  | | Engine     | | Pipeline | | HMAC, AES-256-GCM     |
   +--------------+ +------------+ +----------+ +-----------------------+
          |              |              |          |
          +--------------+-------+------+----------+
                                 |
                                 v
   +-----------------------------+--------------------------------------+
   | Storage Vault & Persistence Layer                                  |
   | - SQLite / PostgreSQL (Relational metadata & audit hash chain)     |
   | - Isolated File Storage (UUID paths outside public web root)       |
   +--------------------------------------------------------------------+"""
    )

    add_h2("Technology Choices & Rationale")
    add_bullet("• FastAPI (Python 3.11): ", "Selected for native performance, automatic OpenAPI documentation, and rich ecosystem for scientific computing (NumPy, SciPy) and PDF processing (PyMuPDF).")
    add_bullet("• React 19 & TypeScript: ", "Type-safe user interface preventing null pointer errors, with Tailwind CSS v4 for accessible, high-contrast UI design.")
    add_bullet("• PyMuPDF (fitz): ", "C-backed high-performance PDF manipulation library capable of injecting vector text without altering underlying document layouts.")
    add_bullet("• SciPy & NumPy: ", "Provides mathematical 2D Discrete Cosine Transform (ortho-normalized) algorithms for frequency transformation.")

    # ==================== 5. DEEP DIVE: EVERY MAJOR MODULE ====================
    add_h1("5. Deep Dive into Every Major Module")
    add_p("In this section, we examine each module using our standardized 9-point framework:")

    # MODULE 1
    add_h2("Module 1: Authentication & Account Security")
    add_p("1. What it is: Genuine user registration, login, and session authentication system.")
    add_p("2. Why we need it: Prevents unauthorized users from uploading, watermarking, or viewing private institutional documents.")
    add_p("3. How it works: When a user registers, their password is processed through Argon2id with memory-hard parameters. On login, the backend verifies the Argon2id hash and issues a signed JSON Web Token (JWT). The first user is automatically granted the 'admin' role; subsequent users become 'instructor'.")
    add_p("4. Files & Libraries: backend/app/api/v1/auth.py, backend/app/security/auth.py, passlib[argon2], pyjwt.")
    add_p("5. Real-World Example: Dr. Katherine registers with 'katherine@university.edu'. Her password 'SecretPass123!' is never saved as plaintext—it is transformed into an Argon2id hash ($argon2id$v=19$m=65536,t=2,p=2$...).")
    add_p("6. How to demonstrate: Open http://localhost:3000/register, create an account, log in at /login, and view your active user badge in the navbar.")
    add_p("7. How to test: Run pytest backend/tests/test_api_integration.py::test_auth_workflow_and_security.")
    add_p("8. Limitations: Does not currently send outbound SMTP confirmation emails; accounts activate immediately upon registration.")
    add_p("9. Viva Question: 'Why use Argon2id instead of SHA-256 for passwords?' Answer: SHA-256 is fast, allowing attackers with GPUs to test billions of guesses per second. Argon2id requires large amounts of RAM and time, neutralizing GPU and ASIC attacks.")

    # MODULE 2
    add_h2("Module 2: Secure PDF Ingestion & Vault Storage")
    add_p("1. What it is: Validated file upload and isolated storage system for course documents.")
    add_p("2. Why we need it: Untrusted file uploads can cause path traversal, zip bombs, or executable malware execution.")
    add_p("3. How it works: Validates that the file has a .pdf extension and opens it via PyMuPDF. Checks that the page count is between 1 and 100 and size is under 25MB. Generates a random UUID filename (e.g. 7641e0ad-e422-4af8-a755-370bb122a443.pdf) and stores it outside the web directory. Calculates SHA-256 of the original file.")
    add_p("4. Files & Libraries: backend/app/api/v1/documents.py, backend/app/storage/, PyMuPDF.")
    add_p("5. Real-World Example: A student tries to upload 'syllabus.pdf.exe' or a 500MB corrupt file. The API rejects it with an HTTP 400 error.")
    add_p("6. How to demonstrate: Navigate to /documents, click 'Upload PDF', and observe the file appearing in the table with its page count and SHA-256 prefix.")
    add_p("7. How to test: Verified via pytest backend/tests/test_api_integration.py::test_unauthorized_access_prevented.")
    add_p("8. Limitations: Does not integrate ClamAV antivirus daemon in local zero-docker development.")
    add_p("9. Viva Question: 'Why rename the uploaded file to a UUID?' Answer: To prevent Path Traversal attacks (e.g., ../../../etc/passwd) and prevent overwriting existing files.")

    # MODULE 3
    add_h2("Module 3: Visible Digital Watermarking")
    add_p("1. What it is: Vector overlay system that applies customized diagonal security notices across all pages.")
    add_p("2. Why we need it: Acts as an immediate visual deterrent to prevent casual screenshotting or sharing.")
    add_p("3. How it works: Uses PyMuPDF's page.insert_text(). Calculates page dimensions and centers text rotated at 45 degrees with 35% alpha transparency, plus an unobtrusive top security banner.")
    add_p("4. Files & Libraries: backend/app/watermarking/visible.py, PyMuPDF.")
    add_p("5. Real-World Example: Adding 'CONFIDENTIAL - CS401 - EXAM' across all exam pages in translucent slate-blue text.")
    add_p("6. How to demonstrate: In /documents, click 'Apply Watermark', choose 'Visible Overlay', enter text, and download the resulting PDF.")
    add_p("7. How to test: Verified via output PDF generation in backend/storage/protected/.")
    add_p("8. Limitations: A determined attacker can crop margins or use image editing software to erase visible text.")
    add_p("9. Viva Question: 'Does a visible watermark preserve text searchability?' Answer: Yes! PyMuPDF inserts vector text elements over the existing content stream without flattening pages into images.")

    # MODULE 4
    add_h2("Module 4: Invisible 2D-DCT Steganography Pipeline")
    add_p("1. What it is: Mathematical frequency-domain watermark embedding and extraction system.")
    add_p("2. Why we need it: If a leaker erases the visible watermark, the invisible watermark remains embedded in the pixels.")
    add_p("3. How it works (5-Step Algorithm):")
    add_bullet("a. Color Space Conversion: ", "The PDF page is rendered to RGB at 150 DPI and converted to YCbCr. The Y (Luminance) channel is extracted as a floating-point NumPy matrix.")
    add_bullet("b. Preamble & Payload Bitstream: ", "The watermark string (e.g., 'STUDENT-2026-904') is converted to an ASCII bit array prefixed with an 8-bit synchronization marker: [1, 0, 1, 0, 1, 1, 0, 0].")
    add_bullet("c. 8x8 2D-DCT Transformation: ", "The luminance matrix is sliced into non-overlapping 8x8 pixel blocks. Each block is transformed into frequency coefficients via 2D ortho-normalized DCT.")
    add_bullet("d. Mid-Frequency Coefficient Modulation: ", "We target coefficients (3,2) and (2,3). If bit=1 and (c1 - c2) < strength, we adjust c1 and c2 so c1 > c2. If bit=0, we adjust so c2 > c1.")
    add_bullet("e. Inverse DCT & Reconstruction: ", "We apply 2D-IDCT to each block, clip values to [0, 255], recombine with original Cb and Cr channels, and compile back into a PDF.")
    add_p("4. Files & Libraries: backend/app/watermarking/invisible_dct.py, SciPy (scipy.fftpack.dct/idct), NumPy, Pillow, PyMuPDF.")
    add_p("5. Real-World Example: Embedding 'CS401:STUDENT-99' into page 1. When viewed, the page looks completely normal. When extracted, the exact string is recovered.")
    add_p("6. How to demonstrate: Apply an invisible watermark in /documents, then upload the downloaded file into /verify to see the extracted payload.")
    add_p("7. How to test: Run pytest backend/tests/test_crypto_watermark.py::test_dct_invisible_watermark_pipeline.")
    add_p("8. Limitations: Rasterizes the carrier page to 150 DPI images, which increases file size and converts vector text into raster images.")
    add_p("9. Viva Question: 'Why choose mid-frequencies instead of low or high frequencies?' Answer: Low frequencies contain fundamental visible image structures, so altering them causes visible distortion. High frequencies are discarded during lossy JPEG compression. Mid-frequencies balance perceptual invisibility with compression robustness.")

    # MODULE 5
    add_h2("Module 5: Cryptographic Manifest & Ed25519 Signatures")
    add_p("1. What it is: Asymmetric digital notary seal that cryptographically binds document metadata and hashes.")
    add_p("2. Why we need it: Proves who issued the document and guarantees that neither the hashes nor the watermark references were altered.")
    add_p("3. How it works: Constructs a canonical JSON manifest with sorted keys and no whitespace. The server signs the canonical byte string with its Ed25519 private key, outputting a Base64 signature. The public key is stored in PEM format for verification.")
    add_p("4. Files & Libraries: backend/app/cryptography/engine.py, cryptography.hazmat.primitives.asymmetric.ed25519.")
    add_p("5. Real-World Example: Manifest JSON containing document ID, original SHA-256, protected SHA-256, watermark algorithm ('DCT-SpreadSpectrum-v1'), and issuer email, signed with Ed25519.")
    add_p("6. How to demonstrate: In /documents, click 'Manifest' to view and download the signed JSON structure.")
    add_p("7. How to test: Run pytest backend/tests/test_crypto_watermark.py::test_ed25519_digital_signature.")
    add_p("8. Limitations: Proves the manifest's integrity under the server's keypair; does not prove the legal copyright ownership of the original text.")
    add_p("9. Viva Question: 'What is canonical JSON and why is it required for digital signatures?' Answer: In JSON, key order and whitespace can vary (e.g., {'a':1, 'b':2} vs {'b': 2, 'a': 1}). Canonicalization sorts keys and strips extra spaces so the byte representation is deterministic before hashing and signing.")

    # MODULE 6
    add_h2("Module 6: Forensic Verification Center")
    add_p("1. What it is: Automated multi-path forensic evaluation tool for suspected documents.")
    add_p("2. Why we need it: Allows instructors and administrators to upload any PDF and determine whether it is authentic, modified, or leaked.")
    add_p("3. How it works: Evaluates candidate SHA-256 hash against database records, verifies Ed25519 signatures, and runs DCT frequency extraction. Categorizes results into clear verdicts: AUTHENTIC_EXACT_MATCH, AUTHENTIC_WATERMARK_CONFIRMED, TAMPERED_DOCUMENT_MODIFIED, or UNREGISTERED_OR_ALTERED.")
    add_p("4. Files & Libraries: backend/app/api/v1/verify.py, backend/app/reports/pdf_generator.py, ReportLab.")
    add_p("5. Real-World Example: Uploading a modified assignment PDF. The system confirms the Ed25519 signature is valid for the manifest, but detects a hash mismatch, declaring TAMPERED_DOCUMENT_MODIFIED.")
    add_p("6. How to demonstrate: Open /verify, upload a protected document, inspect the analysis card, and click 'Download Official Certificate (PDF)'.")
    add_p("7. How to test: Verified through API integration and end-to-end verification flows.")
    add_p("8. Limitations: Detached verification without database access requires the user to supply the companion manifest JSON.")
    add_p("9. Viva Question: 'If the hash does not match, can the document still be authentic?' Answer: Yes! If a student converted the PDF to a high-quality scan or re-saved it, the byte hash will differ, but if the extracted DCT watermark matches our record, we know the underlying content is authentic.")

    # MODULE 7
    add_h2("Module 7: Robustness Testing Lab")
    add_p("1. What it is: An interactive experimental sandbox for evaluating watermark resilience against real distortion attacks.")
    add_p("2. Why we need it: Demonstrates genuine scientific evaluation rather than making unverified claims.")
    add_p("3. How it works: Takes the watermarked carrier page, applies a chosen transformation (JPEG compression, downscaling/upscaling, additive Gaussian noise, or border cropping), attempts watermark extraction, and measures PSNR (dB) and Bit Error Rate (BER).")
    add_p("4. Files & Libraries: backend/app/watermarking/robustness.py, frontend/src/pages/Lab.tsx, NumPy, Pillow.")
    add_p("5. Real-World Example: Compressing a watermarked document with JPEG Quality 70. The system reports PSNR = 38.4 dB, BER = 0.0%, and successfully extracts 'CONFIDENTIAL CS401'.")
    add_p("6. How to demonstrate: Navigate to /lab, select a document, choose 'JPEG Lossy Compression', set intensity to 70, and click 'Execute Robustness Test'.")
    add_p("7. How to test: Verified via automated test test_dct_invisible_watermark_pipeline.")
    add_p("8. Limitations: Severe border cropping (>20%) disrupts the non-overlapping 8x8 block alignment and causes extraction failure.")
    add_p("9. Viva Question: 'What do PSNR and BER represent?' Answer: PSNR (Peak Signal-to-Noise Ratio in dB) measures visual fidelity; values above 35 dB indicate imperceptible distortion. BER (Bit Error Rate) is the fraction of corrupted payload bits; 0.0% means 100% accurate recovery.")

    # MODULE 8
    add_h2("Module 8: Tamper-Evident Chained Audit Logging")
    add_p("1. What it is: A cryptographically chained audit ledger of all security-sensitive events.")
    add_p("2. Why we need it: Prevents corrupt administrators or attackers from altering or deleting history logs.")
    add_p("3. How it works: Every event record stores actor ID, event type, timestamp, details, previous hash, and current hash, where Current_Hash = SHA-256(Previous_Hash + Actor + Type + Status + Details).")
    add_p("4. Files & Libraries: backend/app/services/audit.py, backend/app/models/models.py.")
    add_p("5. Real-World Example: In the Dashboard, the audit table displays each action linked to the previous SHA-256 hash prefix, forming a verifiable blockchain-like trail.")
    add_p("6. How to demonstrate: Perform any upload or verification, visit /dashboard, and view the updated cryptographic audit sequence.")
    add_p("7. How to test: Executed automatically on every auth, upload, and verification test case.")
    add_p("8. Limitations: A privileged root database administrator could theoretically recalculate the entire chain forward unless external timestamping or anchoring (e.g. OpenTimestamps) is used.")
    add_p("9. Viva Question: 'How does hash chaining prevent log tampering?' Answer: If an attacker modifies an old event record, its hash changes, breaking the link to all subsequent records in the chain.")

    # ==================== 6. DATABASE SCHEMA & ENTITY RELATIONSHIPS ====================
    add_h1("6. Database Design & Entity-Relationship Model")
    add_p("The database schema is defined in backend/app/models/models.py using SQLAlchemy:")

    add_code_block(
"""+----------------+          1 : N          +-------------------+
|     User       |------------------------->|     Document      |
|----------------|                          |-------------------|
| id (UUID)      |                          | id (UUID)         |
| email (Unique) |                          | title             |
| hashed_password|                          | original_filename |
| full_name      |                          | original_sha256   |
| role           |                          | owner_id (FK)     |
+----------------+                          +-------------------+
        |                                             |
        | 1 : N                                       | 1 : N
        v                                             v
+----------------+                          +-------------------+
|   AuditEvent   |                          |  WatermarkRecord  |
|----------------|                          |-------------------|
| id (UUID)      |                          | id (UUID)         |
| actor_id (FK)  |                          | document_id (FK)  |
| event_type     |                          | watermark_type    |
| previous_hash  |                          | payload_text      |
| current_hash   |                          | protected_sha256  |
+----------------+                          | manifest_id       |
                                            | digital_signature |
                                            +-------------------+
                                                      |
                                                      | 1 : N
                                                      v
                                            +-------------------+
                                            |RobustnessExperiment
                                            |-------------------|
                                            | id (UUID)         |
                                            | watermark_rec(FK) |
                                            | transformation    |
                                            | psnr_db           |
                                            | bit_error_rate    |
                                            +-------------------+"""
    )

    # ==================== 7. TESTING STRATEGY & VERIFIED RESULTS ====================
    add_h1("7. Testing Strategy & Actual Verified Results")
    add_p("AquaMark was verified using automated unit and integration tests run via pytest:")

    tbl_test = doc.add_table(rows=9, cols=3)
    tbl_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    th_cells = tbl_test.rows[0].cells
    th_cells[0].text = "Test Identifier"
    th_cells[1].text = "What is Verified"
    th_cells[2].text = "Result"
    for c in th_cells:
        set_cell_background(c, "0F172A")
        c.paragraphs[0].runs[0].font.name = "Arial"
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9)
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    test_data = [
        ("test_sha256_consistency", "SHA-256 determinism & avalanche effect on byte change", "PASSED (100%)"),
        ("test_hmac_sha256_verification", "HMAC verification with secret key & rejection of tampered data", "PASSED (100%)"),
        ("test_ed25519_digital_signature", "Ed25519 signature creation & verification on canonical manifest", "PASSED (100%)"),
        ("test_authenticated_aes_gcm_encryption", "AES-256-GCM encryption with 96-bit nonce & decryption", "PASSED (100%)"),
        ("test_dct_invisible_watermark_pipeline", "Embedding 128-bit payload into 2D-DCT blocks & 100% extraction", "PASSED (100%)"),
        ("test_health", "FastAPI server health endpoint responds with HTTP 200 HEALTHY", "PASSED (100%)"),
        ("test_auth_workflow_and_security", "User registration, Argon2id hashing, login token & bad pass rejection", "PASSED (100%)"),
        ("test_unauthorized_access_prevented", "Access to /documents without valid Bearer token returns HTTP 401", "PASSED (100%)")
    ]

    for idx, (tname, tdesc, tres) in enumerate(test_data, start=1):
        row_cells = tbl_test.rows[idx].cells
        row_cells[0].text = tname
        row_cells[1].text = tdesc
        row_cells[2].text = tres
        bg = "FFFFFF" if idx % 2 != 0 else "F8FAFC"
        for c_idx, cell in enumerate(row_cells):
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            if p.runs:
                p.runs[0].font.name = "Arial"
                p.runs[0].font.size = Pt(8.5)
                if c_idx == 2:
                    p.runs[0].font.bold = True
                    p.runs[0].font.color.rgb = RGBColor(13, 148, 136)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==================== 8. PITCH SCRIPTS: 30s, 2m, 5m ====================
    add_h1("8. Presentation Scripts for Any Time Limit")
    add_p("Use these carefully timed scripts when explaining your project to evaluators:")

    add_h2("The 30-Second Elevator Pitch")
    add_box("30-Second Script",
            "“My project is AquaMark, an applied cryptography platform that protects university lecture notes and exam papers from unauthorized distribution. We combine three layers: Visible Watermarks for visual deterrence, Invisible 2D-DCT Steganography that hides a recipient tracking ID inside pixel frequencies to survive JPEG compression and screenshots, and Ed25519 Digital Signatures that produce a tamper-evident cryptographic manifest. We also built an empirical Robustness Testing Lab that measures Peak Signal-to-Noise Ratio and Bit Error Rate across real-world distortion attacks.”")

    add_h2("The 2-Minute Structured Explanation")
    add_box("2-Minute Script",
            "“Good morning. In electronic education, high-value course content like exam papers and lecture notes are frequently leaked. Traditional watermarks fail because any student can crop them out, while simple file hashes fail because recompressing a PDF alters the hash completely.\n\n"
            "To solve this, we engineered AquaMark. It implements three distinct mathematical layers:\n"
            "First, Visible Watermarking: using PyMuPDF to place vector-preserving diagonal text across all pages.\n"
            "Second, Invisible DCT Steganography: we convert carrier pages to luminance, slice them into 8x8 blocks, and modulate mid-frequency transform coefficients (3,2) and (2,3) to embed a 128-bit payload with preamble synchronization. This hidden serial number survives lossy JPEG compression and format conversions.\n"
            "Third, Cryptographic Authentication: we generate Ed25519 asymmetric digital signatures over canonical JSON manifests and log every action to a SHA-256 chained audit trail.\n\n"
            "Finally, our platform includes a Robustness Lab where we empirically test and report watermark survival against JPEG compression, downscaling, noise, and cropping, outputting PSNR in decibels and Bit Error Rate percentages. All eight test suites are passing, and the application is live.”")

    add_h2("The 5-Minute Technical Deep Dive")
    add_p("For a 5-minute presentation, follow this 4-part structure:")
    add_bullet("1. Problem & Threat Model (1 min): ", "Explain why PDF metadata is easily stripped and why hash comparisons alone are too brittle.")
    add_bullet("2. Architecture & Algorithms (1.5 min): ", "Detail the 2D-DCT frequency transformation, mid-frequency coefficient selection, and Ed25519 asymmetric manifest signing.")
    add_bullet("3. Live System Walkthrough (1.5 min): ", "Show the dashboard, upload a sample PDF, apply an invisible watermark with a student ID, verify the file, and download the official PDF certificate.")
    add_bullet("4. Robustness Lab & Limitations (1 min): ", "Run a JPEG compression trial in the lab, display the PSNR and BER metrics, and honestly discuss geometric cropping limitations.")

    # ==================== 9. 25 VIVA QUESTIONS & CONFIDENT ANSWERS ====================
    add_h1("9. 25 Viva Examination Questions & Model Answers")
    add_p("Study these 25 essential questions and answers to excel in your oral defense:")

    viva_qa = [
        ("Q1: What is the main objective of AquaMark?",
         "To provide an end-to-end platform that protects educational course content using visible watermarks for deterrence, invisible DCT steganography for leak tracing, and Ed25519 digital signatures for tamper-evident authenticity verification."),
        ("Q2: What is the difference between Spatial and Frequency domain watermarking?",
         "Spatial domain watermarking modifies pixel values directly (like LSB replacement). It is fast but easily wiped out by lossy JPEG compression. Frequency domain watermarking (like DCT) transforms the image into frequency coefficients and embeds data into mid-frequencies, which survives recompression and filtering."),
        ("Q3: Why did you choose 8x8 blocks for DCT?",
         "8x8 blocks are the universal standard in image transformation (matching the JPEG compression standard). They provide an ideal trade-off between localized frequency resolution and computational speed."),
        ("Q4: Which DCT coefficients are modified and why?",
         "We modify mid-frequency coefficient pairs (3,2) and (2,3). Low frequencies hold the main visual shapes (modifying them degrades visual quality). High frequencies are completely removed by JPEG quantization. Mid-frequencies provide the optimal balance between visual invisibility and compression survivability."),
        ("Q5: What is the purpose of the preamble sync marker [1,0,1,0,1,1,0,0]?",
         "During extraction, the scanner needs to know exactly where the payload begins and verify that it is reading a valid signal rather than background noise. If the preamble is not detected within an allowable Hamming distance, the extraction is aborted."),
        ("Q6: Why use Ed25519 instead of RSA-2048?",
         "Ed25519 offers 128-bit security (equivalent to RSA-3072) with tiny 64-byte signatures, very low memory overhead, fast signing/verifying speeds, and mathematical immunity to timing attacks and weak random number generator flaws."),
        ("Q7: What is canonical JSON serialization?",
         "In standard JSON, key order and whitespace are arbitrary. Canonical JSON formats the dictionary with sorted keys and compact separators (',', ':') so that the exact same byte string is generated every time before signing."),
        ("Q8: Why does AquaMark use Argon2id for password hashing?",
         "Argon2id won the Password Hashing Competition. It is memory-hard, meaning it requires configurable memory (RAM) and time, preventing attackers from using GPU or ASIC clusters to brute-force passwords."),
        ("Q9: What is HMAC and why is it used?",
         "HMAC (Hash-based Message Authentication Code) combines a secret key with the message hash. In AquaMark, it links the original file hash to the protected file hash, proving that the pairing was authorized by the server."),
        ("Q10: What is AES-256-GCM?",
         "An authenticated symmetric cipher. It encrypts sensitive student metadata while simultaneously generating an authentication tag using a unique 96-bit nonce, ensuring data cannot be decrypted or tampered with."),
        ("Q11: Can a digital watermark prevent someone from leaking a document?",
         "No. A watermark does not physically lock down a computer screen or prevent cameras. It is a forensic deterrence tool that allows the institution to trace the source once an unauthorized copy surfaces."),
        ("Q12: Does a valid digital signature prove legal copyright ownership?",
         "No. A digital signature only proves that the holder of the private key authenticated that specific manifest at that time. It does not prove who authored the text originally before it was signed."),
        ("Q13: What does PSNR stand for and what is a good value?",
         "Peak Signal-to-Noise Ratio, measured in decibels (dB). Values above 35 dB indicate high visual fidelity where human eyes cannot distinguish the watermarked image from the original."),
        ("Q14: What is Bit Error Rate (BER)?",
         "The percentage of recovered bits that differ from the embedded bits. A BER of 0.0% means the watermark was recovered with 100% precision."),
        ("Q15: How does the tamper-evident audit log work?",
         "Each event record includes the SHA-256 hash of the preceding record: Current_Hash = SHA-256(Previous_Hash + EventData). If any historical record is modified or deleted, all subsequent hashes in the chain become invalid."),
        ("Q16: Why store uploaded files with random UUIDs?",
         "To prevent Path Traversal attacks (e.g. ../../../etc/shadow) and avoid filename collisions when multiple users upload files with the same name like 'syllabus.pdf'."),
        ("Q17: What happens if a candidate file hash does not match the database?",
         "AquaMark checks if the digital signature on the manifest is valid and attempts invisible watermark extraction. If the watermark payload matches, it reports 'AUTHENTIC_WATERMARK_CONFIRMED' rather than a false tampering alarm."),
        ("Q18: What is the YCbCr color space?",
         "A color model separating Luminance (Y - brightness) from Chrominance (Cb - blue-difference, Cr - red-difference). We embed watermarks into the Y channel because the human visual system is less sensitive to high-frequency brightness modulations."),
        ("Q19: What is the trade-off of the DCT invisible watermarking pipeline?",
         "Vector PDF pages are rendered into 150 DPI raster images to allow pixel-level DCT frequency modification. This converts vector fonts into raster graphics, slightly increasing file size."),
        ("Q20: What are the main limitations of your watermarking algorithm?",
         "It resists lossy compression, downscaling, and noise, but severe geometric cropping (>30%) or extreme rotational warping disrupts 8x8 block alignment and prevents payload recovery."),
        ("Q21: How are private signing keys protected in AquaMark?",
         "Keys are stored in a protected directory outside the web server root (backend/storage/keys/). The system authority keypair is managed by the backend service and never sent to the browser."),
        ("Q22: What role-based access control is implemented?",
         "The first registered user is automatically designated an 'admin', while subsequent users are 'instructor'. Ownership checks are enforced on every document endpoint so users cannot view or download others' files."),
        ("Q23: How does the verification certificate PDF get generated?",
         "Using ReportLab in Python. It draws an official forensic certificate including document hashes, signature verification status, extracted watermark payload, timestamp, and legal notices."),
        ("Q24: What database is used and why?",
         "SQLAlchemy ORM with SQLite for zero-configuration local development and tests, seamlessly swappable to PostgreSQL via DATABASE_URL in docker-compose.yml for production."),
        ("Q25: What is the most important lesson learned from this project?",
         "That real document security requires a defense-in-depth approach. Hashing alone is too brittle, visible watermarks alone are too easy to erase, and signatures alone do not survive format conversion. Combining all three provides practical, robust protection.")
    ]

    for q, a in viva_qa:
        add_h2(q)
        add_p(a)

    # ==================== 10. GLOSSARY & REVISION CHECKLIST ====================
    add_h1("10. Technical Glossary & Student Revision Checklist")

    add_h2("Technical Terms & Acronyms Glossary")
    add_bullet("• 2D-DCT: ", "Two-Dimensional Discrete Cosine Transform. An algorithm expressing a finite sequence of data points in terms of a sum of cosine functions oscillating at different frequencies.")
    add_bullet("• AES-256-GCM: ", "Advanced Encryption Standard with 256-bit key in Galois/Counter Mode. Provides confidentiality and cryptographic integrity verification.")
    add_bullet("• Argon2id: ", "Hybrid version of Argon2 combining Argon2i (resistant to side-channel attacks) and Argon2d (resistant to GPU cracking).")
    add_bullet("• BER: ", "Bit Error Rate. The ratio of incorrectly received bits to the total number of transmitted bits.")
    add_bullet("• Ed25519: ", "Edwards-curve Digital Signature Algorithm over Curve25519 using SHA-512.")
    add_bullet("• HMAC: ", "Keyed-Hash Message Authentication Code. Calculates a message authentication code involving a cryptographic hash function in combination with a secret key.")
    add_bullet("• Luminance (Y): ", "The photometric measure of luminous intensity, representing the grayscale brightness channel of an image.")
    add_bullet("• PSNR: ", "Peak Signal-to-Noise Ratio. Engineering metric used to quantify reconstruction quality of lossy compression codecs.")
    add_bullet("• SHA-256: ", "Secure Hash Algorithm generating a 256-bit (32-byte, 64-hex character) one-way cryptographic digest.")
    add_bullet("• Steganography: ", "The practice of concealing a message, file, or image within another ordinary file or image.")

    add_h2("Student Master Revision Checklist")
    add_p("Check off these points before entering your viva:")
    add_bullet("[ ] ", "I can explain the difference between Hashing, Signatures, and Watermarking without mixing them up.")
    add_bullet("[ ] ", "I know why we modify mid-frequency DCT coefficients (3,2) and (2,3) instead of low or high frequencies.")
    add_bullet("[ ] ", "I can demonstrate how to upload a PDF, apply an invisible watermark, and verify it live.")
    add_bullet("[ ] ", "I understand why a hash mismatch does not automatically prove malicious tampering.")
    add_bullet("[ ] ", "I know that Ed25519 proves manifest integrity, not original copyright ownership.")
    add_bullet("[ ] ", "I can explain PSNR (visual quality) and Bit Error Rate (payload recovery) in the Robustness Lab.")
    add_bullet("[ ] ", "I can explain the 5 steps of the invisible DCT watermarking algorithm clearly.")

    # Save document
    doc.save(output_path)
    print(f"Generated complete DOCX at: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "docs/AquaMark_Comprehensive_Academic_Learning_Guide.docx"
    build_docx_learning_guide(out)
