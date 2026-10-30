import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

class AcademicNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(AcademicNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(AcademicNumberedCanvas, self).showPage()
        super(AcademicNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Header on pages 2+
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0d9488")) # Teal
            self.drawString(54, letter[1] - 36, "AQUAMARK")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(110, letter[1] - 36, "| Comprehensive Academic & Technical Learning Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer on all pages
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#94a3b8"))
        self.drawString(54, 34, "AquaMark — Robust Digital Watermarking & Document Integrity Platform")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)
        self.restoreState()

def build_pdf_learning_guide(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    primary = colors.HexColor("#0f172a") # Slate 900
    teal = colors.HexColor("#0d9488")    # Teal 600
    dark_gray = colors.HexColor("#1e293b")
    body_gray = colors.HexColor("#334155")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=teal,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=teal,
        spaceBefore=9,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body_gray,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body_gray,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'DocCallout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=dark_gray
    )

    table_header_style = ParagraphStyle(
        'DocTH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'DocTD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=body_gray
    )

    table_cell_bold = ParagraphStyle(
        'DocTDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=primary
    )

    code_style = ParagraphStyle(
        'DocCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#e2e8f0")
    )

    story = []

    # Title & Banner
    story.append(Paragraph("AquaMark — Comprehensive Academic & Technical Learning Guide", title_style))
    story.append(Paragraph("Official Academic Title: Robust Digital Watermarking for Protection of Electronic Course Content<br/><i>Student Learning Handbook, Code Audit, Implementation Breakdown, and Viva Preparation Guide</i>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=teal, spaceBefore=0, spaceAfter=10))

    # Intro Callout
    intro_box = (
        "<b>★ How to Use This Handbook:</b><br/>"
        "This guide is written especially for you as a student. It starts from fundamental concepts, explains every single technical term when introduced, walks through the exact implemented Python and React code, clarifies honest security limits, and provides complete viva answers so you can defend your project with absolute confidence."
    )
    t_box = Table([[Paragraph(intro_box, callout_style)]], colWidths=[504])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LINELEFT', (0,0), (0,0), 3, teal),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 8))

    # SECTION 1: IMPLEMENTATION AUDIT
    story.append(Paragraph("1. Honest Implementation Audit (What is Built vs What is Planned)", h1_style))
    story.append(Paragraph("In any senior or capstone engineering evaluation, academic integrity is paramount. Never claim a feature exists if it was only a design proposal. Below is the audited status of the AquaMark codebase:", body_style))

    story.append(Paragraph("A. Features Fully Implemented and Verified in Working Code", h2_style))
    story.append(Paragraph("• <b>1. Visible Vector Watermark Engine:</b> Implemented in backend/app/watermarking/visible.py using PyMuPDF (fitz). Preserves PDF page geometry, injects diagonal text overlays with adjustable opacity/angles, and embeds top security header banners.", bullet_style))
    story.append(Paragraph("• <b>2. 2D-DCT Invisible Watermark Pipeline:</b> Implemented in backend/app/watermarking/invisible_dct.py. Converts PDF page to Luminance (Y), divides into 8x8 blocks, embeds 128-bit payload with preamble sync marker [1,0,1,0,1,1,0,0] into mid-frequency coefficients (3,2) and (2,3), and performs inverse DCT.", bullet_style))
    story.append(Paragraph("• <b>3. Ed25519 Asymmetric Digital Signatures:</b> Implemented in backend/app/cryptography/engine.py using cryptography library. Generates Ed25519 keypairs, serializes canonical JSON manifests, and verifies digital signatures.", bullet_style))
    story.append(Paragraph("• <b>4. File Integrity & HMAC:</b> SHA-256 block-based hashing for original and protected files; HMAC-SHA-256 binding original hash to protected hash.", bullet_style))
    story.append(Paragraph("• <b>5. Authenticated Symmetric Encryption:</b> AES-256-GCM encryption with unique 96-bit random nonces for sensitive metadata.", bullet_style))
    story.append(Paragraph("• <b>6. Tamper-Evident Audit Hash Chain:</b> Implemented in backend/app/services/audit.py. Each event's SHA-256 hash chains to the previous event's hash, forming an append-only cryptographic sequence.", bullet_style))
    story.append(Paragraph("• <b>7. Robustness Testing Lab:</b> Implemented in backend/app/watermarking/robustness.py & frontend/src/pages/Lab.tsx. Evaluates watermark recovery under JPEG compression, geometric scaling, Gaussian noise, and cropping, calculating PSNR (dB) and Bit Error Rate (BER).", bullet_style))
    story.append(Paragraph("• <b>8. Complete Full-Stack REST API & React Frontend:</b> FastAPI endpoints under /api/v1 (auth, documents, watermarks, verify, experiments, dashboard); React 19 + TypeScript + Tailwind CSS UI.", bullet_style))
    story.append(Paragraph("• <b>9. Automated Test Suite:</b> 8 automated test cases in backend/tests/ passing at 100% (SHA-256, HMAC, Ed25519, AES-GCM, DCT pipeline, health, auth, access prevention).", bullet_style))

    story.append(Paragraph("B. Features Implemented But Not Separately Unit Tested", h2_style))
    story.append(Paragraph("• <b>1. Multi-page Batch Invisible Watermarking:</b> Embedding payload into carrier page 1 is tested; multi-page distributed spreading is supported in code but unit tests target page 1 carrier.", bullet_style))
    story.append(Paragraph("• <b>2. Contrast Adjustment Transformation:</b> Backend supports contrast_adjust in run_single_experiment; the four primary tested vectors in the frontend UI are JPEG, resize, noise, and crop.", bullet_style))

    story.append(Paragraph("C. Features Planned as Future Work (Not Implemented)", h2_style))
    story.append(Paragraph("• <b>1. Hardware Token / HSM Integration:</b> Storing private Ed25519 keys on physical YubiKeys or cloud HSMs (AWS KMS / GCP Cloud KMS). Currently, keys are stored on the server filesystem.", bullet_style))
    story.append(Paragraph("• <b>2. Automatic Projective Mesh Rectification:</b> Self-healing detection of severe trapezoidal phone camera photos taken of computer screens.", bullet_style))
    story.append(Paragraph("• <b>3. Outbound Email Delivery:</b> SMTP / SendGrid email verification. Currently, user accounts activate directly upon registration.", bullet_style))

    story.append(Paragraph("D. Security Non-Claims (Honest Academic Boundaries)", h2_style))
    story.append(Paragraph("• <b>No 'Copy-Proof' Claim:</b> Digital watermarking does NOT physically lock down computer displays. If a student can read the document, they can take a screenshot or retype it. Watermarking is for provenance and leak tracing.", bullet_style))
    story.append(Paragraph("• <b>No 'Proof of Legal Ownership' Claim:</b> An Ed25519 signature proves that a specific private key signed the manifest on that date; it does NOT legally prove who first created the underlying intellectual content.", bullet_style))
    story.append(Paragraph("• <b>No Universal Robustness:</b> Extreme cropping (>30% of page area) or severe geometric rotation disrupts 8x8 block alignment and prevents payload recovery.", bullet_style))

    # SECTION 2: REAL WORLD STORY
    story.append(Paragraph("2. Project Overview & The Real-World Story", h1_style))
    story.append(Paragraph("<b>Scenario: Dr. Katherine's Leaked Midterm:</b><br/>"
                           "Dr. Katherine teaches Advanced Cryptography (CS401) to 60 university students. On Monday, she uploads the upcoming Midterm Exam Assignment to the university portal. On Tuesday morning, a teaching assistant notices that the exact assignment is posted on Chegg and a public Telegram group.<br/>"
                           "Dr. Katherine faces three questions: (1) Is this file actually her authentic exam paper, or a modified version where someone altered Question 4? (2) Can she prove to the Department Chair that she published this document first, without exposing her master private keys? (3) Which of her 60 students downloaded this specific copy and leaked it?<br/>"
                           "Traditional tools fail: cosmetic watermarks are cropped in seconds, and SHA-256 breaks if the student saves as a JPEG. AquaMark solves this by combining visible watermarks, invisible frequency steganography, and Ed25519 digital signatures.", body_style))

    # SECTION 3: BASIC CONCEPTS
    story.append(Paragraph("3. Basic Concepts Explained from Scratch (No Jargon)", h1_style))
    story.append(Paragraph("• <b>SHA-256 Hash:</b> A mathematical fingerprint. Fixed 64 hex characters. Deterministic (same file = same hash) and has the Avalanche Effect (change 1 comma = completely different hash).", bullet_style))
    story.append(Paragraph("• <b>HMAC (Hash-based Message Authentication Code):</b> A hash mixed with a secret key. Proves that data was not altered AND was approved by the secret key holder.", bullet_style))
    story.append(Paragraph("• <b>Asymmetric Digital Signature (Ed25519):</b> A keypair system. Private key stays on server to sign manifests; public key is shared to verify signatures without anyone being able to forge them.", bullet_style))
    story.append(Paragraph("• <b>Digital Watermark:</b> Information embedded directly into the carrier media pixels. Visible watermarks deter casual leaks; invisible DCT watermarks survive compression and formatting.", bullet_style))
    story.append(Paragraph("• <b>Hash Mismatch vs Malicious Tampering:</b> A hash mismatch proves binary bytes changed, but does NOT prove malice (e.g. re-saving in a different PDF reader alters metadata). AquaMark verifies if the underlying DCT watermark payload is still intact.", bullet_style))

    # SECTION 4: ARCHITECTURE
    story.append(Paragraph("4. System Architecture & Technology Stack", h1_style))
    arch_ascii = (
        "+-----------------------------------------------------------------------+\n"
        "|                         AquaMark Web Frontend                         |\n"
        "|      (React 19, TypeScript, Vite, Tailwind CSS v4, Lucide Icons)       |\n"
        "+-----------------------------------+-----------------------------------+\n"
        "                                    | REST API Calls (Axios / JSON)\n"
        "                                    v\n"
        "+-----------------------------------------------------------------------+\n"
        "|                          FastAPI Backend                              |\n"
        "|   /auth      /documents      /watermarks     /verify    /experiments  |\n"
        "+---------+--------------+--------------+----------+--------------------+\n"
        "          |              |              |          |\n"
        "          v              v              v          v\n"
        "   +--------------+ +------------+ +----------+ +-----------------------+\n"
        "   | Security &   | | PyMuPDF    | | 2D-DCT   | | Cryptography Engine   |\n"
        "   | Argon2id     | | Vector     | | Stegano  | | Ed25519, SHA-256,     |\n"
        "   | Auth Tokens  | | Engine     | | Pipeline | | HMAC, AES-256-GCM     |\n"
        "   +--------------+ +------------+ +----------+ +-----------------------+\n"
        "          |              |              |          |\n"
        "          +--------------+-------+------+----------+\n"
        "                                 |\n"
        "                                 v\n"
        "   +-----------------------------+--------------------------------------+\n"
        "   | Storage Vault & Persistence Layer                                  |\n"
        "   | - SQLite / PostgreSQL (Relational metadata & audit hash chain)     |\n"
        "   | - Isolated File Storage (UUID paths outside public web root)       |\n"
        "   +--------------------------------------------------------------------+"
    )
    t_code = Table([[Paragraph(arch_ascii.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code)
    story.append(Spacer(1, 8))

    # SECTION 5: DEEP DIVE MODULES (9-point breakdown)
    story.append(Paragraph("5. Detailed Breakdown of Every Implemented Module", h1_style))

    modules = [
        ("Module 1: Authentication & Account Security",
         "Genuine registration, login, and JWT session authentication. Passwords hashed using Argon2id with memory-hard parameters. First user is 'admin', others 'instructor'. Files: backend/app/api/v1/auth.py, passlib[argon2], pyjwt. Limitation: No outbound SMTP confirmation emails. Viva Tip: Argon2id prevents GPU brute-forcing."),
        
        ("Module 2: Secure PDF Ingestion & Vault Storage",
         "Validates PDF extension, limits page count (1-100) and size (25MB) using PyMuPDF. Generates random UUIDs for storage outside web root to prevent path traversal. Calculates original SHA-256 hash. Files: backend/app/api/v1/documents.py. Limitation: No ClamAV antivirus daemon in local dev. Viva Tip: UUID naming prevents directory traversal attacks."),
        
        ("Module 3: Visible Digital Watermarking",
         "PyMuPDF vector overlay applying 45-degree diagonal text with 35% alpha transparency and top security banner. Preserves existing page dimensions and underlying text searchability. Files: backend/app/watermarking/visible.py. Limitation: Can be cropped if margins are cut. Viva Tip: Preserves vector text without raster flattening."),
        
        ("Module 4: Invisible 2D-DCT Steganography Pipeline",
         "Converts page to Luminance (Y) channel, splits into 8x8 blocks, and applies 2D-DCT. Embeds 128-bit payload with preamble [1,0,1,0,1,1,0,0] into mid-frequency coefficients (3,2) and (2,3) using relative coefficient modulation. Files: backend/app/watermarking/invisible_dct.py, SciPy, NumPy. Limitation: Carrier page is rasterized at 150 DPI. Viva Tip: Mid-frequencies balance visual invisibility with compression resilience."),
        
        ("Module 5: Cryptographic Manifest & Ed25519 Signatures",
         "Constructs canonical JSON manifest (sorted keys, compact separators) with original/protected hashes and watermark metadata. Signed using Ed25519 private key. Public key stored in PEM. Files: backend/app/cryptography/engine.py. Limitation: Proves manifest integrity, not legal ownership of original text. Viva Tip: Canonicalization ensures identical byte strings before hashing."),
        
        ("Module 6: Forensic Verification Center",
         "Multi-path forensic inspection: tests candidate SHA-256 against DB, validates Ed25519 signature on manifest, and extracts DCT frequency watermark. Issues official PDF certificates via ReportLab. Files: backend/app/api/v1/verify.py, pdf_generator.py. Limitation: Detached verification requires companion manifest JSON. Viva Tip: Distinguishes exact hash matches from transformed authentic files."),
        
        ("Module 7: Robustness Testing Lab",
         "Interactive sandbox testing watermark survival against JPEG compression (Q10-Q95), downscaling/upscaling, additive Gaussian noise, and border cropping. Computes PSNR in dB and Bit Error Rate (BER). Files: backend/app/watermarking/robustness.py, frontend/src/pages/Lab.tsx. Limitation: Severe cropping (>20%) disrupts 8x8 block sync. Viva Tip: PSNR >35 dB indicates imperceptible distortion; 0% BER means perfect recovery."),
        
        ("Module 8: Tamper-Evident Chained Audit Logging",
         "Chained ledger where each event's hash = SHA-256(Previous_Hash + Actor + Type + Status + Details). Displayed in real-time on dashboard. Files: backend/app/services/audit.py. Limitation: Root DB admin could recalculate chain without external public anchoring. Viva Tip: Hash chaining makes historical record deletion immediately detectable.")
    ]

    for mtitle, mdesc in modules:
        story.append(Paragraph(f"<b>{mtitle}</b>", h2_style))
        story.append(Paragraph(mdesc, body_style))

    # SECTION 6: TESTING & VERIFIED RESULTS
    story.append(Paragraph("6. Testing Strategy & Actual Verified Results", h1_style))
    story.append(Paragraph("All 8 automated test suites were executed using pytest and verified at 100% success:", body_style))

    table_data = [
        [Paragraph("Test Identifier", table_header_style), Paragraph("What It Verifies", table_header_style), Paragraph("Result", table_header_style)],
        [Paragraph("test_sha256_consistency", table_cell_bold), Paragraph("Determinism and avalanche effect on single byte alteration", table_cell_style), Paragraph("PASSED (100%)", table_cell_bold)],
        [Paragraph("test_hmac_sha256_verification", table_cell_bold), Paragraph("HMAC verification with secret key & rejection of tampered data", table_cell_style), Paragraph("PASSED (100%)", table_cell_bold)],
        [Paragraph("test_ed25519_digital_signature", table_cell_bold), Paragraph("Ed25519 signature creation & verification on canonical manifest", table_cell_style), Paragraph("PASSED (100%)", table_cell_bold)],
        [Paragraph("test_authenticated_aes_gcm_encryption", table_cell_bold), Paragraph("AES-256-GCM encryption with 96-bit nonce & decryption", table_cell_style), Paragraph("PASSED (100%)", table_cell_bold)],
        [Paragraph("test_dct_invisible_watermark_pipeline", table_cell_bold), Paragraph("Embedding 128-bit payload into 2D-DCT blocks & 100% extraction", table_cell_style), Paragraph("PASSED (100%)", table_cell_bold)],
        [Paragraph("test_health", table_cell_bold), Paragraph("FastAPI server health endpoint responds with HTTP 200 HEALTHY", table_cell_style), Paragraph("PASSED (100%)", table_cell_bold)],
        [Paragraph("test_auth_workflow_and_security", table_cell_bold), Paragraph("User registration, Argon2id hashing, login token & bad pass rejection", table_cell_style), Paragraph("PASSED (100%)", table_cell_bold)],
        [Paragraph("test_unauthorized_access_prevented", table_cell_bold), Paragraph("Access to /documents without valid Bearer token returns HTTP 401", table_cell_style), Paragraph("PASSED (100%)", table_cell_bold)],
    ]
    t_test = Table(table_data, colWidths=[140, 274, 90])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 8))

    # SECTION 7: PITCH SCRIPTS
    story.append(Paragraph("7. Presentation Scripts for Any Time Limit", h1_style))
    story.append(Paragraph("<b>30-Second Elevator Pitch:</b><br/>"
                           "“My project is AquaMark, an applied cryptography platform that protects university lecture notes and exam papers from unauthorized distribution. We combine three layers: Visible Watermarks for visual deterrence, Invisible 2D-DCT Steganography that hides a recipient tracking ID inside pixel frequencies to survive JPEG compression and screenshots, and Ed25519 Digital Signatures that produce a tamper-evident cryptographic manifest. We also built an empirical Robustness Testing Lab that measures Peak Signal-to-Noise Ratio and Bit Error Rate across real-world distortion attacks.”", body_style))

    story.append(Paragraph("<b>2-Minute Structured Explanation:</b><br/>"
                           "“In electronic education, high-value course content is frequently leaked. Traditional watermarks fail because any student can crop them out, while simple file hashes fail because recompressing a PDF alters the hash completely.<br/>"
                           "AquaMark implements three distinct mathematical layers: First, Visible Watermarking using PyMuPDF to place vector-preserving diagonal text across all pages. Second, Invisible DCT Steganography: we convert carrier pages to luminance, slice them into 8x8 blocks, and modulate mid-frequency transform coefficients (3,2) and (2,3) to embed a 128-bit payload with preamble synchronization. This hidden serial number survives lossy JPEG compression and format conversions. Third, Cryptographic Authentication: we generate Ed25519 asymmetric digital signatures over canonical JSON manifests and log every action to a SHA-256 chained audit trail.<br/>"
                           "Finally, our platform includes a Robustness Lab where we empirically test and report watermark survival against JPEG compression, downscaling, noise, and cropping, outputting PSNR in decibels and Bit Error Rate percentages. All eight test suites are passing, and the application is live.”", body_style))

    # SECTION 8: 25 VIVA QUESTIONS
    story.append(Paragraph("8. 25 Viva Examination Questions & Model Answers", h1_style))
    viva_list = [
        ("Q1: What is the main objective of AquaMark?", "To protect course content using visible watermarks for deterrence, invisible DCT steganography for leak tracing, and Ed25519 signatures for tamper-evident verification."),
        ("Q2: Spatial vs Frequency domain watermarking?", "Spatial directly alters pixels (e.g. LSB), easily destroyed by JPEG. Frequency transforms image to coefficients (DCT) and embeds in mid-frequencies, surviving recompression."),
        ("Q3: Why 8x8 blocks for DCT?", "Standard in JPEG compression, providing an ideal trade-off between localized frequency resolution and computation speed."),
        ("Q4: Which DCT coefficients are modified?", "Mid-frequency pairs (3,2) and (2,3). Low frequencies contain visible shapes; high frequencies are discarded by JPEG. Mid-frequencies balance invisibility and robustness."),
        ("Q5: What is the preamble sync marker?", "An 8-bit pattern [1,0,1,0,1,1,0,0] allowing the extractor to locate the payload start and verify signal presence before reading data."),
        ("Q6: Why Ed25519 instead of RSA-2048?", "Provides 128-bit security with tiny 64-byte signatures, fast signing/verifying speeds, and immunity to timing attacks."),
        ("Q7: What is canonical JSON serialization?", "Sorting keys and removing whitespace so the exact same byte string is generated every time before hashing and signing."),
        ("Q8: Why Argon2id for password hashing?", "Memory-hard algorithm requiring configurable RAM and time, neutralizing GPU and ASIC brute-force attacks."),
        ("Q9: What is HMAC and why is it used?", "Hash-based Message Authentication Code combining a secret key with file hashes, proving the pairing was authorized by the server."),
        ("Q10: What is AES-256-GCM?", "Authenticated symmetric cipher encrypting sensitive metadata while generating an authentication tag with a 96-bit nonce."),
        ("Q11: Can a watermark prevent copying?", "No. It is a forensic deterrence tool that allows tracing leakers after an unauthorized copy surfaces."),
        ("Q12: Does a signature prove legal copyright?", "No. It proves the private key signed that manifest on that date; it does not prove original authorship."),
        ("Q13: What does PSNR stand for?", "Peak Signal-to-Noise Ratio in dB. Values >35 dB indicate high visual fidelity indistinguishable from the original."),
        ("Q14: What is Bit Error Rate (BER)?", "The fraction of recovered bits that differ from embedded bits; 0.0% means 100% accurate recovery."),
        ("Q15: How does the tamper-evident audit log work?", "Each event hash = SHA-256(Previous_Hash + EventData). Altering any record invalidates all subsequent hashes."),
        ("Q16: Why store files with random UUIDs?", "Prevents Path Traversal attacks and avoids filename collisions from identical uploads."),
        ("Q17: What if candidate hash doesn't match DB?", "AquaMark tests the Ed25519 signature and extracts the DCT watermark. If the payload matches, it confirms authentic content."),
        ("Q18: What is YCbCr color space?", "Separates Luminance (Y - brightness) from Chrominance (Cb, Cr - color). We embed into Y because human eyes are less sensitive to brightness modulations."),
        ("Q19: What is the trade-off of DCT watermarking?", "Carrier pages are rendered to 150 DPI raster images to allow pixel DCT modification, slightly increasing file size."),
        ("Q20: What are your watermark's limitations?", "Severe cropping (>30%) or extreme rotational warping disrupts 8x8 block alignment and prevents recovery."),
        ("Q21: How are private signing keys protected?", "Stored outside the web server root in backend/storage/keys/ and never exposed to the frontend browser."),
        ("Q22: What role-based access is implemented?", "First registered user is 'admin', subsequent are 'instructor'. Ownership checks are enforced on every document endpoint."),
        ("Q23: How are PDF verification certificates made?", "Generated on-the-fly using Python's ReportLab library with full cryptographic hashes and verification verdicts."),
        ("Q24: What database is used?", "SQLAlchemy ORM with SQLite for zero-config development/tests, swappable to PostgreSQL via DATABASE_URL in docker-compose.yml."),
        ("Q25: What is the key takeaway of this project?", "Real document security requires defense-in-depth: combining visible watermarks, invisible frequency steganography, and cryptographic signatures.")
    ]

    for q, a in viva_list:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))

    # SECTION 9: GLOSSARY & CHECKLIST
    story.append(Paragraph("9. Technical Glossary & Student Revision Checklist", h1_style))
    story.append(Paragraph("• <b>2D-DCT:</b> Two-Dimensional Discrete Cosine Transform. Converts spatial pixel brightness into frequency coefficients.<br/>"
                           "• <b>AES-256-GCM:</b> Advanced Encryption Standard with 256-bit key in Galois/Counter Mode providing confidentiality and integrity.<br/>"
                           "• <b>Argon2id:</b> Hybrid memory-hard password hashing algorithm resistant to GPU cracking.<br/>"
                           "• <b>BER:</b> Bit Error Rate. Percentage of corrupted bits in the extracted payload.<br/>"
                           "• <b>Ed25519:</b> Edwards-curve Digital Signature Algorithm providing 128-bit security with 64-byte signatures.<br/>"
                           "• <b>PSNR:</b> Peak Signal-to-Noise Ratio in dB measuring reconstructed image visual quality.<br/>"
                           "• <b>Steganography:</b> The practice of concealing a secret message within an ordinary carrier file.", body_style))

    story.append(Paragraph("<b>Student Master Revision Checklist:</b><br/>"
                           "[ ] I can explain the difference between Hashing, Signatures, and Watermarking without mixing them up.<br/>"
                           "[ ] I know why we modify mid-frequency DCT coefficients (3,2) and (2,3).<br/>"
                           "[ ] I can demonstrate uploading a PDF, applying an invisible watermark, and verifying it live.<br/>"
                           "[ ] I understand why a hash mismatch does not automatically prove malicious tampering.<br/>"
                           "[ ] I know that Ed25519 proves manifest integrity, not original legal copyright ownership.<br/>"
                           "[ ] I can explain PSNR (visual quality) and Bit Error Rate (payload recovery) in the Robustness Lab.", body_style))

    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"Generated complete PDF at: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "docs/AquaMark_Comprehensive_Academic_Learning_Guide.pdf"
    build_pdf_learning_guide(out)
