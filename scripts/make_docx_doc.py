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

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_docx(output_path):
    doc = Document()

    # Set page margins (0.8 inch)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles helper
    primary_color = RGBColor(15, 23, 42)    # Deep Navy Slate
    accent_color = RGBColor(13, 148, 136)   # Teal 600
    subtext_color = RGBColor(71, 85, 105)  # Slate 600

    # Title & Header
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("AquaMark: Complete Project Guide & Technical Documentary")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = primary_color

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(18)
    run_sub = sub_p.add_run("Robust Digital Watermarking for Protection of Electronic Course Content\nComplete Plain-Language Explanation, Architecture, Defense Viva, & Code Breakdown")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = accent_color

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = primary_color
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = accent_color
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(bold_prefix)
        r1.font.name = "Arial"
        r1.font.size = Pt(10.5)
        r1.font.bold = True
        r1.font.color.rgb = primary_color
        r2 = p.add_run(text)
        r2.font.name = "Arial"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, 120, 120, 180, 180)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"★ {title}\n")
        r_title.font.name = "Arial"
        r_title.font.size = Pt(11)
        r_title.font.bold = True
        r_title.font.color.rgb = accent_color
        r_body = p.add_run(text)
        r_body.font.name = "Arial"
        r_body.font.size = Pt(10)
        r_body.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # SECTION 1: WHAT IS AQUAMARK IN SIMPLE WORDS?
    # -------------------------------------------------------------
    add_h1("1. What is AquaMark? (The 2-Minute Elevator Pitch)")
    add_body(
        "Imagine you are a professor or university teacher. You spend weeks writing high-value lecture notes, "
        "graded assignments, and question banks. You distribute PDFs to your students. A week later, you discover "
        "your course material uploaded anonymously to public websites (like Chegg, Reddit, or CourseHero) with your name deleted. "
        "How do you prove that this document was originally yours? And how do you find out which student leaked it?"
    )
    add_body(
        "AquaMark is an end-to-end cybersecurity and cryptography web application engineered to solve this exact crisis. "
        "Instead of just putting a cosmetic stamp on a PDF that any student can crop out, AquaMark applies three layers of mathematical security:"
    )
    add_bullet("Layer 1: Visible Watermarks: ", "Diagonal security notices and page headers that remind readers the file is copyright-protected.")
    add_bullet("Layer 2: Invisible DCT Steganography: ", "Secret digital identifiers embedded into the mathematical frequencies of the document's pages. The human eye cannot see it, but our forensic scanner can pull it out—even if the student converts it to an image or compresses it as a JPEG.")
    add_bullet("Layer 3: Cryptographic Integrity (Ed25519 & SHA-256): ", "An asymmetric digital signature manifest and hash ledger that acts like a tamper-proof notary seal. If anyone alters a single character or comma in the file, AquaMark's verification scanner instantly flags it as TAMPERED.")

    add_callout(
        "Simple Analogy to Remember",
        "Think of AquaMark like a modern passport: It has a visible photo (Visible Watermark), an invisible biometric RFID microchip embedded in the paper (DCT Invisible Watermark), and an official government cryptographic digital seal (Ed25519 Signature + SHA-256). You can't forge it, and you can always trace who it was issued to."
    )

    # -------------------------------------------------------------
    # SECTION 2: THE 3 CORE CONCEPTS YOU MUST DISTINGUISH
    # -------------------------------------------------------------
    add_h1("2. The Three Cryptographic Pillars (Viva Defense Foundation)")
    add_body(
        "In university viva evaluations, examiners often test whether you truly understand the mathematical difference "
        "between Hashing, Digital Signatures, and Digital Watermarking. AquaMark treats each of these as distinct tools:"
    )

    # Comparison Table
    tbl = doc.add_table(rows=4, cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Concept", "What It Does", "Strength", "Limitation / Vulnerability"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        set_cell_background(cell, "0F172A")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = "Arial"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("SHA-256 Hash", "Creates a 64-character mathematical fingerprint of the exact bytes.", "Extremely sensitive: changing even 1 bit changes the entire hash completely.", "Brittle: If someone converts PDF to JPG or recompresses it, the hash changes even if content is unchanged."),
        ("Ed25519 Signature", "Uses asymmetric public/private keys to sign a document manifest.", "Mathematically proves who issued the document and guarantees non-repudiation.", "Only verifies the signed metadata manifest; doesn't survive if the binary wrapper is stripped."),
        ("DCT Watermarking", "Embeds imperceptible bits directly into the image frequencies.", "Robust: Survives image resizing, JPEG compression, and format changes.", "Does not prove legal ownership alone; it provides forensic traceability.")
    ]

    for row_idx, row_data in enumerate(data, start=1):
        bg = "FFFFFF" if row_idx % 2 != 0 else "F8FAFC"
        for col_idx, text in enumerate(row_data):
            cell = tbl.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = primary_color
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # SECTION 3: HOW THE INVISIBLE WATERMARK ACTUALLY WORKS (DCT)
    # -------------------------------------------------------------
    add_h1("3. How Does the Invisible Watermark Work? (Under the Hood)")
    add_body(
        "Many basic student projects simply hide text in PDF metadata (which can be deleted in 2 seconds with any free tool). "
        "AquaMark implements genuine frequency-domain steganography using Discrete Cosine Transform (DCT):"
    )
    add_bullet("Step 1: Color Space Conversion (YCbCr): ", "The PDF page is converted into an image and split into Luminance (Y - brightness) and Chrominance (Cb, Cr - color). Humans are less sensitive to subtle changes in luminance frequency.")
    add_bullet("Step 2: 8x8 Block Transformation: ", "The entire luminance page is sliced into small 8x8 pixel squares. Each 8x8 block undergoes a 2D Discrete Cosine Transform (DCT). This changes pixel brightness values into frequency coefficients.")
    add_bullet("Step 3: Mid-Frequency Modulation: ", "Why mid-frequencies? Low frequencies contain the primary visible content (modifying them ruins image clarity). High frequencies are completely discarded by JPEG compression. Mid-frequency pairs (3,2) and (2,3) are the 'sweet spot'.")
    add_bullet("Step 4: Embedding the Bit: ", "To embed a binary bit '1', the system adjusts the DCT math so Coefficient(3,2) > Coefficient(2,3). To embed a binary bit '0', it forces Coefficient(2,3) > Coefficient(3,2).")
    add_bullet("Step 5: Inverse DCT: ", "The blocks are converted back into standard pixels via Inverse DCT (IDCT). To human eyes, the page looks completely normal, but the digital signal is permanently woven into the math of the image.")

    # -------------------------------------------------------------
    # SECTION 4: STEP-BY-STEP USER WORKFLOW
    # -------------------------------------------------------------
    add_h1("4. Step-by-Step System Walkthrough")
    add_body("When you demo the project to evaluators, follow this exact 5-step flow:")

    add_h2("Step 1: Registration & Secure Login")
    add_body("Create an account with email and master password. Passwords are never stored in plaintext—they are hashed using Argon2id (the winner of the Password Hashing Competition), making them impervious to GPU brute-force attacks.")

    add_h2("Step 2: Upload Course PDF")
    add_body("Drag and drop any lecture note, syllabus, or exam PDF. The system extracts page count, calculates original SHA-256 hash, and saves it in isolated storage using random UUIDs to prevent directory traversal attacks.")

    add_h2("Step 3: Apply Protection & Watermarking")
    add_body(
        "Select your document and choose whether you want Visible Overlay or Invisible DCT Watermarking. "
        "Enter a custom label (e.g. 'CONFIDENTIAL CS401') and an optional Student ID (e.g. 'STUDENT-2026-904'). "
        "The system embeds the payload, signs a canonical JSON manifest with the server's Ed25519 private key, "
        "and logs the action to a tamper-evident hash chain."
    )

    add_h2("Step 4: Forensic Verification")
    add_body(
        "Go to the 'Verify Document' page. Upload any PDF suspected of being altered or leaked. "
        "AquaMark performs automated forensic analysis: checks if the hash matches the original, verifies the Ed25519 digital signature, "
        "and runs an extraction scan for invisible watermarks. You can download an official cryptographic PDF certificate on the spot."
    )

    add_h2("Step 5: The Robustness Testing Lab")
    add_body(
        "This is the star feature of the project! Go to the 'Robustness Lab' tab. "
        "You can subject the watermarked file to simulated real-world attacks: JPEG compression, geometric downscaling, "
        "Gaussian noise, and border cropping. The system runs the attack, attempts extraction, and reports real mathematical metrics: "
        "PSNR (Peak Signal-to-Noise Ratio in dB) and Bit Error Rate (BER)."
    )

    # -------------------------------------------------------------
    # SECTION 5: PROJECT ARCHITECTURE & CODE MAP
    # -------------------------------------------------------------
    add_h1("5. Technical Architecture & File Directory Guide")
    add_body("The project is cleanly decoupled into a FastAPI backend and a React/TypeScript frontend:")

    add_bullet("backend/app/cryptography/engine.py: ", "Contains Ed25519 keypair generation, canonical JSON signing, SHA-256 calculation, HMAC-SHA-256 validation, and AES-256-GCM encryption.")
    add_bullet("backend/app/watermarking/visible.py: ", "Handles PyMuPDF (fitz) vector text injection with custom angles, alpha transparency, and header security banners.")
    add_bullet("backend/app/watermarking/invisible_dct.py: ", "Contains 2D-DCT block transformation, sync preamble detection, mid-frequency modulation, and extraction routines.")
    add_bullet("backend/app/watermarking/robustness.py: ", "Executes simulated image attacks (JPEG, resize, noise, crop) and measures PSNR and Bit Error Rate.")
    add_bullet("backend/app/services/audit.py: ", "Tamper-evident audit trail linking each event to the previous SHA-256 hash.")
    add_bullet("backend/app/reports/pdf_generator.py: ", "Uses ReportLab to generate official forensic certificates in PDF format.")
    add_bullet("frontend/src/pages/: ", "React pages for Home, Login, Register, Dashboard, Documents, Verify, Lab, and About.")

    # -------------------------------------------------------------
    # SECTION 6: VIVA QUESTIONS & HOW TO ANSWER THEM
    # -------------------------------------------------------------
    add_h1("6. Top Viva Questions & Confident Answers")
    add_body("Review these questions before your presentation or academic viva:")

    qa_list = [
        ("Q1: What is the difference between Spatial domain and Frequency domain watermarking?",
         "Answer: Spatial domain watermarking directly changes pixel color values (like adding a subtle watermark or changing the least significant bit LSB). It is simple but easily destroyed by JPEG compression or resizing. Frequency domain watermarking (like AquaMark's DCT) transforms the image into frequency coefficients first and modifies mid-frequencies. It is much more robust against lossy compression and image operations."),
        
        ("Q2: Why did you choose Ed25519 over older algorithms like RSA-2048?",
         "Answer: Ed25519 is based on Edwards-curve Digital Signature Algorithm (EdDSA). It provides 128-bit security level equivalent to RSA-3072, but produces tiny 64-byte signatures, requires very low CPU overhead, and has mathematical immunity against timing attacks and weak random number generator vulnerabilities."),
        
        ("Q3: Why use Argon2id for password hashing instead of SHA-256 or MD5?",
         "Answer: SHA-256 is an extremely fast general-purpose hashing algorithm, meaning attackers with GPUs can compute billions of guesses per second. Argon2id is a memory-hard password hashing algorithm designed specifically to resist GPU and ASIC brute-force attacks by requiring configurable RAM and time costs."),
        
        ("Q4: Can a digital watermark prevent someone from copying a document?",
         "Answer: No. Digital watermarks are deterrence and forensics tools, not access control walls. Once a student can view a document on their screen, they can take a screenshot or retype it. Watermarking ensures that when an unauthorized copy surfaces, the university can prove origin and trace which student leaked it."),
        
        ("Q5: What is PSNR and Bit Error Rate (BER) in your Robustness Lab?",
         "Answer: PSNR (Peak Signal-to-Noise Ratio) measures visual quality in decibels (dB); higher PSNR (>35 dB) means the watermarked image looks virtually identical to the original. BER (Bit Error Rate) measures the percentage of corrupted bits in the recovered payload; 0% BER means perfect recovery.")
    ]

    for q, a in qa_list:
        add_h2(q)
        add_body(a)

    # -------------------------------------------------------------
    # SECTION 7: HONEST RESEARCH BOUNDARIES & LIMITATIONS
    # -------------------------------------------------------------
    add_h1("7. Limitations & Honest Academic Boundaries")
    add_body(
        "Academic evaluators respect honesty about engineering trade-offs. You should clearly state these known boundaries:"
    )
    add_bullet("1. Severe Geometric Cropping: ", "If someone crops out more than 30% of the page or warps it trapezoidally, block synchronization can fail without advanced projective mesh rectification.")
    add_bullet("2. Rasterization Trade-off: ", "To embed DCT watermarks into page pixels, vector PDF pages are rasterized at 150 DPI. While visually sharp, this converts vector fonts into raster images, slightly increasing file size.")
    add_bullet("3. Digital Signatures vs Legal Proof: ", "A digital signature proves that the holder of the private key authenticated the manifest on that date; it does not legally prove who wrote the underlying original text before it was signed.")

    doc.save(output_path)
    print(f"Successfully generated DOCX at {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "AquaMark_Complete_Project_Documentary.docx"
    generate_docx(out)
