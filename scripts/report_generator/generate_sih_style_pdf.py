import os
import shutil
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)
from reportlab.pdfgen import canvas

pdf_out = "/Users/omsaishdhokchaule/Downloads/AquaMark_SIH_Style_Presentation.pdf"

# 16:9 Widescreen dimensions (960 x 540 pt)
PAGE_WIDTH, PAGE_HEIGHT = 960, 540

DARK_NAVY = colors.HexColor("#0F2A4A")
ACCENT_ORANGE = colors.HexColor("#F97316")
ACCENT_BLUE = colors.HexColor("#0284C7")
ACCENT_GREEN = colors.HexColor("#10B981")
BG_WHITE = colors.HexColor("#FFFFFF")
CARD_BG = colors.HexColor("#FFFFFF")
CARD_BORDER = colors.HexColor("#E2E8F0")
TEXT_DARK = colors.HexColor("#1E293B")
TEXT_MUTED = colors.HexColor("#64748B")
FOOTER_LINE = colors.HexColor("#BAE6FD")

class SIHCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(SIHCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_sih_decorations(num_pages)
            super(SIHCanvas, self).showPage()
        super(SIHCanvas, self).save()

    def draw_sih_decorations(self, page_count):
        self.saveState()
        
        # White background
        self.setFillColor(BG_WHITE)
        self.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        # Bottom thin blue line
        self.setStrokeColor(FOOTER_LINE)
        self.setLineWidth(1)
        self.line(40, 32, PAGE_WIDTH - 40, 32)
        
        # Footer text
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawString(40, 20, "AquaMark | Robust Digital Watermarking for Protection of Electronic Course Content")
        self.drawRightString(PAGE_WIDTH - 40, 20, f"@SIH Idea submission- Template  |  {self._pageNumber} / {page_count}")
        
        self.restoreState()

def build_sih_pdf():
    pdf = SimpleDocTemplate(
        pdf_out,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=40,
        rightMargin=40,
        topMargin=25,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    sih_tag = ParagraphStyle(
        'SIHTag', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=ACCENT_ORANGE, alignment=1, spaceAfter=2
    )

    sih_title = ParagraphStyle(
        'SIHTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=DARK_NAVY, alignment=1, spaceAfter=14
    )

    card_t = ParagraphStyle(
        'CardT', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=13,
        textColor=DARK_NAVY
    )

    card_d = ParagraphStyle(
        'CardD', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.5,
        textColor=TEXT_DARK
    )

    story = []

    # ==================== SLIDE 1: COVER ====================
    # Top Orange Pill
    t_pill = Table([[Paragraph("<font color='white'><b>SMART INDIA HACKATHON 2026</b></font>", ParagraphStyle('P', parent=styles['Normal'], fontSize=9, alignment=1))]], colWidths=[200])
    t_pill.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_ORANGE),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_pill)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<font size=28 color='#0F2A4A'><b>AquaMark</b></font>", ParagraphStyle('H1', parent=styles['Normal'], leading=32)))
    story.append(Paragraph("<font size=14 color='#0284C7'><b>Secure Digital Watermarking and Document Integrity Platform</b></font>", ParagraphStyle('H2', parent=styles['Normal'], leading=18)))
    story.append(Spacer(1, 10))

    # Grid table + Graphic side-by-side
    grid_rows = [
        [Paragraph("<font color='#F97316'><b>PROBLEM STATEMENT ID</b></font>", card_d), Paragraph("CIS-105", card_d),
         Paragraph("<font color='#F97316'><b>PS CATEGORY</b></font>", card_d), Paragraph("Software (Cybersecurity)", card_d)],
        [Paragraph("<font color='#F97316'><b>TECHNICAL DOMAIN</b></font>", card_d), Paragraph("D11: Steganography & Forensics", card_d),
         Paragraph("<font color='#F97316'><b>TEAM / CLASS</b></font>", card_d), Paragraph("T.Y. B.Tech Cyber Security (A-15)", card_d)],
        [Paragraph("<font color='#F97316'><b>PRESENTER (STUDENT)</b></font>", card_d), Paragraph("Sanjivani Rameshwar More (PRN: 2124UCSM1115)", card_d),
         Paragraph("<font color='#F97316'><b>PROJECT GUIDE & HOD</b></font>", card_d), Paragraph("Dr. Chetan D. Bawankar", card_d)],
        [Paragraph("<font color='#F97316'><b>INSTITUTION</b></font>", card_d), Paragraph("Dept of Cyber Security, SET, Sanjivani University", card_d),
         Paragraph("<font color='#F97316'><b>COURSE</b></font>", card_d), Paragraph("Cryptography & Info Security (24UCYPC301)", card_d)],
        [Paragraph("<font color='#F97316'><b>PROBLEM TITLE</b></font>", card_d), Paragraph("Robust Digital Watermarking for Course Content", card_d),
         Paragraph("<font color='#F97316'><b>PILOT JURISDICTION</b></font>", card_d), Paragraph("Sanjivani University Campus", card_d)],
    ]
    t_grid = Table(grid_rows, colWidths=[150, 160, 130, 140])
    t_grid.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))

    # Right side graphic & QR
    t_right_cover = Table([
        [RLImage("scripts/report_generator/assets/sih/security_illustration.png", width=180, height=180)],
        [
            Table([
                [RLImage("scripts/report_generator/assets/sih/demo_qr.png", width=75, height=75),
                 Paragraph("<font size=7.5 color='#F97316'><b>SCAN FOR REPO</b></font><br/><font size=7 color='#64748B'>AquaMark Source Code<br/>&amp; Verified Tests</font>", card_d)]
            ], colWidths=[80, 130])
        ]
    ], colWidths=[240])
    t_right_cover.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    cover_layout = Table([[t_grid, t_right_cover]], colWidths=[600, 260])
    cover_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(cover_layout)
    story.append(PageBreak())

    # ==================== SLIDE 2: OVERVIEW ====================
    story.append(Paragraph("SMART INDIA HACKATHON 2026  |  COLLEGE LABORATORY EVALUATION", sih_tag))
    story.append(Paragraph("Proposed Solution &amp; Project Overview", sih_title))

    c2_cards_data = [
        ("PDF Watermarking", "Applies diagonal semi-transparent recipient PRN and institutional stamps across all pages.", "Implemented"),
        ("Document Traceability", "Forensically binds recipient identity so leaked materials trace directly back to the downloader.", "Implemented"),
        ("File Integrity Check", "Computes unique SHA-256 fingerprints to detect any unauthorized 1-byte alteration.", "Implemented"),
        ("Secure User Access", "Enforces role-based access for faculty and students using salted bcrypt and JWT tokens.", "Implemented"),
        ("Document Management", "Relational SQLite database organizes course documents, watermarks, and verification logs.", "Implemented")
    ]
    c2_table_rows = []
    for idx, (title, desc, tag) in enumerate(c2_cards_data):
        c_cell = (
            f"<font size=10 color='#0F2A4A'><b>{idx+1}. {title}</b></font> &nbsp;&nbsp;"
            f"<font size=7.5 color='#F97316'><b>[{tag.upper()}]</b></font><br/>"
            f"<font size=8.5 color='#1E293B'>{desc}</font>"
        )
        c2_table_rows.append([Paragraph(c_cell, card_d)])

    t_c2_left = Table(c2_table_rows, colWidths=[550])
    t_c2_left.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))

    # Right navy panel
    navy_content = (
        "<font size=11 color='#F97316'><b>CORE SECURITY WORKFLOW</b></font><br/><br/>"
        "<font size=9.5 color='white'><b>&gt; 1. UPLOAD PDF</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Faculty uploads course materials in standard PDF format.</font><br/><br/>"
        "<font size=9.5 color='white'><b>&gt; 2. PROTECT &amp; STAMP</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Engine overlays recipient PRN stamp &amp; computes SHA-256.</font><br/><br/>"
        "<font size=9.5 color='white'><b>&gt; 3. VERIFY &amp; AUDIT</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Instant green/red forensic check on circulating copies.</font><br/><br/>"
        "<font size=8 color='#38BDF8'><b>Sub-1.2s &nbsp;•&nbsp; 0 Distortion &nbsp;•&nbsp; 100% Catch</b></font>"
    )
    t_c2_right = Table([[Paragraph(navy_content, card_d)]], colWidths=[290])
    t_c2_right.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))

    layout_s2 = Table([[t_c2_left, t_c2_right]], colWidths=[570, 300])
    layout_s2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(layout_s2)
    story.append(PageBreak())

    # ==================== SLIDE 3: TECHNICAL APPROACH ====================
    story.append(Paragraph("SMART INDIA HACKATHON 2026  |  COLLEGE LABORATORY EVALUATION", sih_tag))
    story.append(Paragraph("Technical Approach &amp; Architecture", sih_title))

    tech_data = [
        ("A. Frontend Interface", "React 18 + TypeScript + Vite + Tailwind CSS (Responsive web portal, live preview)", "Client Tier"),
        ("B. Backend Controller", "Python 3.12 + FastAPI + Uvicorn ASGI (Async REST APIs, JWT tokens, role security)", "API Tier"),
        ("C. PDF Processing Engine", "PyMuPDF (fitz) + SciPy (Vector parsing, 45° visible watermark, 2D-DCT frequency)", "Processing"),
        ("D. Cryptographic Core", "hashlib (SHA-256) + hmac + passlib (bcrypt) (Unique fingerprints, tamper manifests)", "Security"),
        ("E. Data &amp; Vault Storage", "SQLite Relational DB + Isolated Server Vault (Stores documents, users, audit logs)", "Persistence")
    ]
    tech_rows = []
    for title, desc, tag in tech_data:
        cell_t = (
            f"<font size=10 color='#0F2A4A'><b>{title}</b></font> &nbsp;&nbsp;"
            f"<font size=7.5 color='#F97316'><b>[{tag.upper()}]</b></font><br/>"
            f"<font size=8.5 color='#1E293B'>{desc}</font>"
        )
        tech_rows.append([Paragraph(cell_t, card_d)])

    t_tech_left = Table(tech_rows, colWidths=[550])
    t_tech_left.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))

    # Right side: Architecture diagram + bottom boxes
    arch_img = RLImage("scripts/report_generator/assets/system_architecture.png", width=290, height=210)
    b_demo_cells = [
        [
            Paragraph("<font size=8.5 color='#F97316'><b>LIVE BACKEND</b></font><br/><font size=7.5 color='#1E293B'>FastAPI Swagger<br/>http://localhost:8000</font>", card_d),
            Paragraph("<font size=8.5 color='#0284C7'><b>SOURCE CODE</b></font><br/><font size=7.5 color='#1E293B'>GitHub Repository<br/>sanjivani-more/AquaMark</font>", card_d)
        ]
    ]
    t_b_demo = Table(b_demo_cells, colWidths=[140, 140])
    t_b_demo.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))

    t_tech_right = Table([[arch_img], [Spacer(1, 6)], [t_b_demo]], colWidths=[290])
    t_tech_right.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    layout_s3 = Table([[t_tech_left, t_tech_right]], colWidths=[570, 300])
    layout_s3.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(layout_s3)
    story.append(PageBreak())

    # ==================== SLIDE 4: FEASIBILITY ====================
    story.append(Paragraph("SMART INDIA HACKATHON 2026  |  COLLEGE LABORATORY EVALUATION", sih_tag))
    story.append(Paragraph("Feasibility and Viability Analysis", sih_title))

    hero_box = (
        "<font size=12 color='#F97316'><b>ACADEMIC SECURITY GUARANTEE</b></font><br/><br/>"
        "<font size=10 color='white'><b>SUB-SECOND EXECUTION &nbsp;•&nbsp; ZERO LICENSING COST</b></font><br/><br/>"
        "<font size=8.5 color='#CBD5E1'>Every document receives an immutable 256-bit SHA-256 digital fingerprint and recipient watermark record.</font><br/><br/>"
        "<font size=8.5 color='#93C5FD'>Standard PDF compatibility: Works on all phones, tablets, and PCs without proprietary apps.</font>"
    )
    t_hero = Table([
        [RLImage("scripts/report_generator/assets/sih/shield_icon.png", width=120, height=120)],
        [Paragraph(hero_box, card_d)]
    ], colWidths=[310])
    t_hero.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))

    grid_4_data = [
        [
            Paragraph("<font size=10 color='#0F2A4A'><b>1. Technical Feasibility</b></font><br/><font size=8.5 color='#1E293B'>Built entirely using industry-proven, stable technologies (Python, FastAPI, React, PyMuPDF). Highly maintainable and lightweight.</font>", card_d),
            Paragraph("<font size=10 color='#0F2A4A'><b>2. Low Cost &amp; Open Source</b></font><br/><font size=8.5 color='#1E293B'>Zero proprietary software licensing fees. Built on open-source libraries, drastically reducing institutional operational overhead.</font>", card_d)
        ],
        [
            Paragraph("<font size=10 color='#0F2A4A'><b>3. Practical Campus Adoption</b></font><br/><font size=8.5 color='#1E293B'>Designed specifically for college workflows. Teachers require no training; simple upload-and-stamp workflow handles entire batches.</font>", card_d),
            Paragraph("<font size=10 color='#0F2A4A'><b>4. Layered Security Model</b></font><br/><font size=8.5 color='#1E293B'>Visible deterrence prevents casual forwarding, while cryptographic SHA-256 hashing instantly exposes byte-level file modifications.</font>", card_d)
        ]
    ]
    t_grid_4 = Table(grid_4_data, colWidths=[260, 260])
    t_grid_4.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    layout_s4 = Table([[t_hero, t_grid_4]], colWidths=[330, 540])
    layout_s4.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(layout_s4)
    story.append(PageBreak())

    # ==================== SLIDE 5: IMPACT & BENEFITS ====================
    story.append(Paragraph("SMART INDIA HACKATHON 2026  |  COLLEGE LABORATORY EVALUATION", sih_tag))
    story.append(Paragraph("Impact and Institutional Benefits", sih_title))

    b_cards = [
        ("BENEFIT 01", "Source Identification", "Visible watermark displaying student PRN immediately reveals the original source of any leaked copy.", ACCENT_ORANGE),
        ("BENEFIT 02", "Integrity Checking", "SHA-256 cryptographic hashing detects unauthorized modifications to deadlines, grades, or exam questions.", ACCENT_BLUE),
        ("BENEFIT 03", "Document Traceability", "Forensic database records maintain a clear timeline of when files were generated, issued, and verified.", ACCENT_GREEN),
        ("BENEFIT 04", "Organized Workflow", "Replaces disorganized file sharing with a unified web dashboard for uploading, protecting, and tracking notes.", ACCENT_ORANGE),
        ("BENEFIT 05", "Educational Security", "Protects faculty intellectual property while ensuring students receive authentic, untampered study materials.", ACCENT_BLUE)
    ]
    b_cells = []
    for b_hdr, b_title, b_desc, b_clr in b_cards:
        cell_b = (
            f"<font size=8.5 color='{b_clr}'><b>{b_hdr}</b></font><br/>"
            f"<font size=10 color='#0F2A4A'><b>{b_title}</b></font><br/><br/>"
            f"<font size=8.5 color='#1E293B'>{b_desc}</font>"
        )
        b_cells.append(Paragraph(cell_b, card_d))

    t_b_row = Table([b_cells], colWidths=[172]*5)
    t_b_row.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_b_row)
    story.append(Spacer(1, 15))

    banner_p = Table([[Paragraph("<font color='white'><b>“Supporting safer sharing and better traceability of educational documents.”</b></font>", ParagraphStyle('BP', parent=styles['Normal'], alignment=1, fontSize=11))]], colWidths=[860])
    banner_p.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(banner_p)
    story.append(PageBreak())

    # ==================== SLIDE 6: REFERENCES ====================
    story.append(Paragraph("SMART INDIA HACKATHON 2026  |  COLLEGE LABORATORY EVALUATION", sih_tag))
    story.append(Paragraph("Research and Technical References", sih_title))

    ref_items = [
        ("1", "Digital Watermarking Fundamentals (2008)", "I. J. Cox, M. L. Miller, J. A. Bloom, J. Fridrich, T. Kalker", "Digital Watermarking and Steganography, 2nd ed. Morgan Kaufmann", "https://doi.org/10.1016/B978-0-12-372585-1.X5001-3"),
        ("2", "PDF Architecture & Vector Standards (2008)", "Adobe Systems Inc. / International Organization for Standardization", "ISO 32000-1:2008 — Document Management: Portable Document Format", "https://www.iso.org/standard/51502.html"),
        ("3", "Cryptographic Security & Hashing (2020)", "William Stallings", "Cryptography and Network Security: Principles and Practice, 8th ed. Pearson", "https://www.pearson.com/en-us/subject-catalog/p/cryptography-and-network-security"),
        ("4", "Discrete Cosine Transform (2D-DCT) (1974)", "N. Ahmed, T. Natarajan, and K. R. Rao", "IEEE Transactions on Computers, vol. C-23, no. 1, pp. 90-93", "https://doi.org/10.1109/T-C.1974.223784"),
        ("5", "Frequency-Domain Watermark Robustness (1999)", "C.-T. Hsu and J.-L. Wu", "IEEE Transactions on Image Processing, vol. 8, no. 1, pp. 58-68", "https://doi.org/10.1109/83.736686"),
        ("6", "Secure Hash Standard (SHA-256) (2015)", "National Institute of Standards and Technology (NIST)", "Federal Information Processing Standards Publication (FIPS PUB 180-4)", "https://doi.org/10.6028/NIST.FIPS.180-4")
    ]
    ref_grid = []
    for r_idx in range(0, len(ref_items), 2):
        row_c = []
        for c_idx in range(2):
            num, title, auth, src, lnk = ref_items[r_idx + c_idx]
            cell_txt = (
                f"<font size=9.5 color='#0F2A4A'><b>[{num}] {title}</b></font><br/>"
                f"<font size=8 color='#1E293B'>Authors: {auth}</font><br/>"
                f"<font size=7.5 color='#64748B'><i>Source: {src}</i></font><br/>"
                f"<font size=7 color='#0284C7'>{lnk}</font>"
            )
            row_c.append(Paragraph(cell_txt, card_d))
        ref_grid.append(row_c)

    t_ref_table = Table(ref_grid, colWidths=[425, 425])
    t_ref_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_ref_table)

    pdf.build(story, canvasmaker=SIHCanvas)
    shutil.copy(pdf_out, "/Users/omsaishdhokchaule/Downloads/AquaMark/AquaMark_SIH_Style_Presentation.pdf")
    print("SIH-Style PDF generated successfully!")

if __name__ == "__main__":
    build_sih_pdf()
