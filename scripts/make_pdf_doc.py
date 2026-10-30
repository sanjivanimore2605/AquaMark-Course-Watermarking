import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top banner for subsequent pages
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0d9488")) # Teal
            self.drawString(54, letter[1] - 36, "AQUAMARK")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(110, letter[1] - 36, "| Complete Project Guide & Technical Documentary")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#94a3b8"))
        self.drawString(54, 34, "AquaMark — Robust Digital Watermarking & Document Integrity Platform")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)
        self.restoreState()

def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary = colors.HexColor("#0f172a") # Slate 900
    teal = colors.HexColor("#0d9488")    # Teal 600
    dark_gray = colors.HexColor("#1e293b")
    body_gray = colors.HexColor("#334155")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=teal,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=teal,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body_gray,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body_gray,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'DocCallout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_gray
    )

    table_header_style = ParagraphStyle(
        'DocTH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'DocTD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=body_gray
    )

    table_cell_bold = ParagraphStyle(
        'DocTDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=primary
    )

    story = []

    # Title & Subtitle Banner
    story.append(Paragraph("AquaMark: Complete Project Guide & Technical Documentary", title_style))
    story.append(Paragraph("Robust Digital Watermarking for Protection of Electronic Course Content<br/><i>Complete Plain-Language Explanation, Architecture, Defense Viva, & Code Breakdown</i>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=teal, spaceBefore=0, spaceAfter=12))

    # SECTION 1
    story.append(Paragraph("1. What is AquaMark? (The 2-Minute Elevator Pitch)", h1_style))
    story.append(Paragraph(
        "Imagine you are a professor or university teacher. You spend weeks writing high-value lecture notes, "
        "graded assignments, and question banks. You distribute PDFs to your students. A week later, you discover "
        "your course material uploaded anonymously to public websites (like Chegg, Reddit, or CourseHero) with your name deleted. "
        "How do you prove that this document was originally yours? And how do you find out which student leaked it?",
        body_style
    ))
    story.append(Paragraph(
        "<b>AquaMark</b> is an end-to-end cybersecurity and cryptography web application engineered to solve this exact crisis. "
        "Instead of just putting a cosmetic stamp on a PDF that any student can crop out, AquaMark applies three layers of mathematical security:",
        body_style
    ))
    story.append(Paragraph("• <b>Layer 1: Visible Watermarks:</b> Diagonal security notices and page headers that remind readers the file is copyright-protected.", bullet_style))
    story.append(Paragraph("• <b>Layer 2: Invisible DCT Steganography:</b> Secret digital identifiers embedded into the mathematical frequencies of the document's pages. The human eye cannot see it, but our forensic scanner can pull it out—even if the student converts it to an image or compresses it as a JPEG.", bullet_style))
    story.append(Paragraph("• <b>Layer 3: Cryptographic Integrity (Ed25519 & SHA-256):</b> An asymmetric digital signature manifest and hash ledger that acts like a tamper-proof notary seal. If anyone alters a single character or comma in the file, AquaMark's verification scanner instantly flags it as TAMPERED.", bullet_style))

    # Callout Box
    callout_text = (
        "<b>★ Simple Analogy to Remember:</b><br/>"
        "Think of AquaMark like a modern passport: It has a visible photo (Visible Watermark), an invisible biometric RFID microchip embedded in the paper (DCT Invisible Watermark), and an official government cryptographic digital seal (Ed25519 Signature + SHA-256). You can't forge it, and you can always trace who it was issued to."
    )
    callout_table = Table([[Paragraph(callout_text, callout_style)]], colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINELEFT', (0,0), (0,0), 3, teal),
    ]))
    story.append(Spacer(1, 4))
    story.append(callout_table)
    story.append(Spacer(1, 8))

    # SECTION 2
    story.append(Paragraph("2. The Three Cryptographic Pillars (Viva Defense Foundation)", h1_style))
    story.append(Paragraph(
        "In university viva evaluations, examiners often test whether you truly understand the mathematical difference "
        "between Hashing, Digital Signatures, and Digital Watermarking. AquaMark treats each of these as distinct tools:",
        body_style
    ))

    # Comparison Table
    table_data = [
        [Paragraph("Concept", table_header_style), Paragraph("What It Does", table_header_style), Paragraph("Strength", table_header_style), Paragraph("Limitation / Vulnerability", table_header_style)],
        [Paragraph("SHA-256 Hash", table_cell_bold), Paragraph("Creates a 64-char fingerprint of exact file bytes.", table_cell_style), Paragraph("Extremely sensitive: 1 altered bit flips the entire hash.", table_cell_style), Paragraph("Brittle: recompressing or converting to image invalidates hash.", table_cell_style)],
        [Paragraph("Ed25519 Signature", table_cell_bold), Paragraph("Asymmetric keys sign canonical document manifest.", table_cell_style), Paragraph("Guarantees non-repudiation and author authenticity.", table_cell_style), Paragraph("Only protects signed manifest metadata, not physical prints.", table_cell_style)],
        [Paragraph("DCT Watermarking", table_cell_bold), Paragraph("Embeds imperceptible bits in luminance frequency coefficients.", table_cell_style), Paragraph("Robust against JPEG compression, resizing, and screenshots.", table_cell_style), Paragraph("Provides leak tracing; does not replace legal copyright claims.", table_cell_style)],
    ]
    t = Table(table_data, colWidths=[84, 140, 140, 140])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # SECTION 3
    story.append(Paragraph("3. How Does the Invisible Watermark Work? (Under the Hood)", h1_style))
    story.append(Paragraph(
        "Many basic student projects simply hide text in PDF metadata (which can be deleted in 2 seconds with any free tool). "
        "AquaMark implements genuine frequency-domain steganography using Discrete Cosine Transform (DCT):",
        body_style
    ))
    story.append(Paragraph("• <b>Step 1: Color Space Conversion (YCbCr):</b> The PDF page is converted into an image and split into Luminance (Y - brightness) and Chrominance (Cb, Cr - color). Humans are less sensitive to subtle changes in luminance frequency.", bullet_style))
    story.append(Paragraph("• <b>Step 2: 8x8 Block Transformation:</b> The entire luminance page is sliced into small 8x8 pixel squares. Each 8x8 block undergoes a 2D Discrete Cosine Transform (DCT). This changes pixel brightness values into frequency coefficients.", bullet_style))
    story.append(Paragraph("• <b>Step 3: Mid-Frequency Modulation:</b> Why mid-frequencies? Low frequencies contain primary visual energy (modifying them ruins image clarity). High frequencies are completely discarded by JPEG compression. Mid-frequency pairs (3,2) and (2,3) are the 'sweet spot'.", bullet_style))
    story.append(Paragraph("• <b>Step 4: Embedding the Bit:</b> To embed a binary bit '1', the system adjusts the DCT math so Coefficient(3,2) > Coefficient(2,3). To embed a binary bit '0', it forces Coefficient(2,3) > Coefficient(3,2).", bullet_style))
    story.append(Paragraph("• <b>Step 5: Inverse DCT:</b> The blocks are converted back into standard pixels via Inverse DCT (IDCT). To human eyes, the page looks completely normal, but the digital signal is permanently woven into the math of the image.", bullet_style))

    # SECTION 4
    story.append(Paragraph("4. Step-by-Step System Walkthrough (Demo Guide)", h1_style))
    story.append(Paragraph("<b>Step 1: Registration & Secure Login:</b> Create an account with email and master password. Passwords are never stored in plaintext—they are hashed using Argon2id, making them impervious to GPU brute-force attacks.", body_style))
    story.append(Paragraph("<b>Step 2: Upload Course PDF:</b> Drag and drop any lecture note, syllabus, or exam PDF. The system extracts page count, calculates original SHA-256 hash, and saves it in isolated storage using random UUIDs.", body_style))
    story.append(Paragraph("<b>Step 3: Apply Protection & Watermarking:</b> Choose Visible Overlay or Invisible DCT Watermarking. Enter custom label (e.g. 'CONFIDENTIAL CS401') and an optional Student ID (e.g. 'STUDENT-2026-904'). The system signs a canonical JSON manifest with the server's Ed25519 private key and logs the action to a tamper-evident hash chain.", body_style))
    story.append(Paragraph("<b>Step 4: Forensic Verification:</b> Go to the 'Verify Document' page. Upload any PDF suspected of being altered or leaked. AquaMark checks hash match, verifies the Ed25519 digital signature, and runs an extraction scan for invisible watermarks. You can download an official cryptographic PDF certificate.", body_style))
    story.append(Paragraph("<b>Step 5: The Robustness Testing Lab:</b> Subject the watermarked file to simulated real-world attacks: JPEG compression, geometric downscaling, Gaussian noise, and border cropping. The system runs the attack, attempts extraction, and reports real mathematical metrics: PSNR (in dB) and Bit Error Rate (BER).", body_style))

    # SECTION 5
    story.append(Paragraph("5. Technical Architecture & File Directory Guide", h1_style))
    story.append(Paragraph("• <b>backend/app/cryptography/engine.py:</b> Ed25519 keypair generation, canonical JSON signing, SHA-256 calculation, HMAC-SHA-256 validation, and AES-256-GCM encryption.", bullet_style))
    story.append(Paragraph("• <b>backend/app/watermarking/visible.py:</b> PyMuPDF (fitz) vector text injection with custom angles, alpha transparency, and header security banners.", bullet_style))
    story.append(Paragraph("• <b>backend/app/watermarking/invisible_dct.py:</b> 2D-DCT block transformation, sync preamble detection, mid-frequency modulation, and extraction routines.", bullet_style))
    story.append(Paragraph("• <b>backend/app/watermarking/robustness.py:</b> Executes simulated image attacks (JPEG, resize, noise, crop) and measures PSNR and Bit Error Rate.", bullet_style))
    story.append(Paragraph("• <b>backend/app/services/audit.py:</b> Tamper-evident audit trail linking each event to the previous SHA-256 hash.", bullet_style))
    story.append(Paragraph("• <b>backend/app/reports/pdf_generator.py:</b> Uses ReportLab to generate official forensic certificates in PDF format.", bullet_style))
    story.append(Paragraph("• <b>frontend/src/pages/:</b> React pages for Home, Login, Register, Dashboard, Documents, Verify, Lab, and About.", bullet_style))

    # SECTION 6
    story.append(Paragraph("6. Top Viva Questions & Confident Answers", h1_style))
    qas = [
        ("Q1: What is the difference between Spatial domain and Frequency domain watermarking?",
         "Answer: Spatial domain watermarking directly changes pixel color values (like adding a subtle watermark or changing LSB). It is easily destroyed by JPEG compression. Frequency domain watermarking (like AquaMark's DCT) transforms the image into frequency coefficients first and modifies mid-frequencies, making it far more robust."),
        ("Q2: Why did you choose Ed25519 over older algorithms like RSA-2048?",
         "Answer: Ed25519 provides 128-bit security level equivalent to RSA-3072, but produces tiny 64-byte signatures, requires very low CPU overhead, and has mathematical immunity against timing attacks."),
        ("Q3: Why use Argon2id for password hashing instead of SHA-256?",
         "Answer: SHA-256 is fast, allowing attackers with GPUs to compute billions of guesses per second. Argon2id is a memory-hard algorithm designed specifically to resist GPU/ASIC brute-force attacks by requiring configurable RAM and time costs."),
        ("Q4: Can a digital watermark prevent someone from copying a document?",
         "Answer: No. Digital watermarks are deterrence and forensics tools, not access control walls. Once a student can view a document, they can screenshot it. Watermarking ensures that when an unauthorized copy surfaces, the university can prove origin and trace the leaker."),
        ("Q5: What is PSNR and Bit Error Rate (BER) in your Robustness Lab?",
         "Answer: PSNR (Peak Signal-to-Noise Ratio) measures visual fidelity in dB (>35 dB means virtually identical to original). BER (Bit Error Rate) measures percentage of corrupted bits in recovered payload (0% BER = perfect extraction).")
    ]
    for q, a in qas:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))

    # SECTION 7
    story.append(Paragraph("7. Limitations & Honest Academic Boundaries", h1_style))
    story.append(Paragraph("• <b>Severe Geometric Cropping:</b> Cropping out >30% of the page or severe trapezoidal warping impairs block synchronization.", bullet_style))
    story.append(Paragraph("• <b>Rasterization Trade-off:</b> Embedding DCT watermarks into page pixels requires rasterizing vector PDF pages at 150 DPI, slightly increasing file size.", bullet_style))
    story.append(Paragraph("• <b>Digital Signatures vs Legal Proof:</b> An Ed25519 signature proves who authenticated the manifest on that date; it does not replace legal copyright arbitration.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "AquaMark_Complete_Project_Documentary.pdf"
    build_pdf(out)
