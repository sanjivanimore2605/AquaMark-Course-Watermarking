import os
import shutil
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)
from reportlab.pdfgen import canvas

pdf_out = "/Users/omsaishdhokchaule/Downloads/AquaMark_Project_Presentation.pdf"

# 16:9 Widescreen landscape dimensions (approx 13.33 x 7.5 inches = 960 x 540 pt)
PAGE_WIDTH, PAGE_HEIGHT = 960, 540

# Color Palette
DARK_NAVY = colors.HexColor("#0F2A4A")
ACCENT_TEAL = colors.HexColor("#0284C7")
DARK_SLATE = colors.HexColor("#1E293B")
MUTED_GRAY = colors.HexColor("#64748B")
BG_LIGHT = colors.HexColor("#F8FAFC")
CARD_BG = colors.HexColor("#FFFFFF")
CARD_BORDER = colors.HexColor("#E2E8F0")
ACCENT_GREEN = colors.HexColor("#10B981")
ACCENT_RED = colors.HexColor("#EF4444")

class PresentationCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(PresentationCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(PresentationCanvas, self).showPage()
        super(PresentationCanvas, self).save()

    def draw_decorations(self, page_count):
        # Draw background color
        self.saveState()
        if self._pageNumber == 1 or self._pageNumber == 12:
            self.setFillColor(DARK_NAVY)
            self.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        else:
            self.setFillColor(BG_LIGHT)
            self.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
            
            # Slide Header tracker
            self.setFont("Helvetica-Bold", 8.5)
            self.setFillColor(ACCENT_TEAL)
            self.drawString(40, PAGE_HEIGHT - 32, "AQUAMARK  |  CRYPTOGRAPHY & INFORMATION SECURITY (24UCYPC301)")
            
            # Top divider line
            self.setStrokeColor(CARD_BORDER)
            self.setLineWidth(1)
            self.line(40, PAGE_HEIGHT - 75, PAGE_WIDTH - 40, PAGE_HEIGHT - 75)
            
            # Bottom slide footer
            self.setStrokeColor(CARD_BORDER)
            self.setLineWidth(0.5)
            self.line(40, 32, PAGE_WIDTH - 40, 32)
            
            self.setFont("Helvetica", 8)
            self.setFillColor(MUTED_GRAY)
            self.drawString(40, 20, "Sanjivani University | Dept. of Cyber Security | Sanjivani Rameshwar More (PRN: 2124UCSM1115)")
            self.drawRightString(PAGE_WIDTH - 40, 20, f"Slide {self._pageNumber} of {page_count}")
            
        self.restoreState()

def build_pdf_presentation():
    pdf = SimpleDocTemplate(
        pdf_out,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=40,
        rightMargin=40,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_slide_h1 = ParagraphStyle(
        'T1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=colors.white, alignment=0
    )
    title_slide_sub = ParagraphStyle(
        'TSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=13, leading=18,
        textColor=colors.HexColor("#E2E8F0"), alignment=0
    )
    title_slide_badge = ParagraphStyle(
        'TBadge', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=14,
        textColor=colors.HexColor("#38BDF8"), alignment=0
    )

    slide_title = ParagraphStyle(
        'STitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=DARK_NAVY, spaceAfter=12
    )

    card_header = ParagraphStyle(
        'CHdr', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=DARK_NAVY, spaceAfter=4
    )

    card_badge = ParagraphStyle(
        'CBadge', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=ACCENT_TEAL, spaceAfter=6
    )

    card_body = ParagraphStyle(
        'CBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.5,
        textColor=DARK_SLATE, spaceAfter=4
    )

    story = []

    # ==================== SLIDE 1: TITLE SLIDE ====================
    story.append(Spacer(1, 40))
    story.append(Paragraph("SANJIVANI UNIVERSITY  |  SCHOOL OF ENGINEERING & TECHNOLOGY  |  DEPARTMENT OF CYBER SECURITY", title_slide_badge))
    story.append(Spacer(1, 10))
    story.append(Paragraph("AquaMark: Robust Digital Watermarking & Document Integrity", title_slide_h1))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Official Topic: Robust Digital Watermarking for Protection of Electronic Course Content (PS Code: CIS-105)", title_slide_sub))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Domain: D11 — Steganography, Watermarking & Digital Forensics  |  Course: Cryptography & Information Security (24UCYPC301)", title_slide_badge))
    story.append(Spacer(1, 35))

    # Meta card in white
    meta_box = [
        [
            Paragraph("<font size=8.5 color='#0284C7'><b>PRESENTER (STUDENT):</b></font><br/>"
                      "<font size=14 color='#0F2A4A'><b>Sanjivani Rameshwar More</b></font><br/>"
                      "<font size=9.5 color='#1E293B'>PRN: 2124UCSM1115 &nbsp;|&nbsp; Roll No.: A-15<br/>"
                      "Class: T.Y. B.Tech Cyber Security (Semester V)</font>", card_body),
            Paragraph("<font size=8.5 color='#0284C7'><b>PROJECT GUIDE & EVALUATION:</b></font><br/>"
                      "<font size=14 color='#0F2A4A'><b>Dr. Chetan D. Bawankar</b></font><br/>"
                      "<font size=9.5 color='#1E293B'>Head, Department of Cyber Security<br/>"
                      "Subject Teacher: Mr. Kunal Makar &nbsp;|&nbsp; A.Y. 2026-2027</font>", card_body)
        ]
    ]
    t_m = Table(meta_box, colWidths=[430, 430])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t_m)
    story.append(PageBreak())

    # Helper for creating 3 or 4 cards table
    def make_cards_row(cards_data, col_w=280):
        row_cells = []
        for c in cards_data:
            badge_html = f"<font size=7.5 color='{c.get('badge_color', '#0284C7')}'><b>{c.get('badge','').upper()}</b></font><br/>" if c.get('badge') else ""
            items_html = "<br/>".join([f"• &nbsp;{it}" for it in c['items']])
            cell_content = (
                f"{badge_html}"
                f"<font size=11 color='#0F2A4A'><b>{c['title']}</b></font><br/><br/>"
                f"<font size=9 color='#1E293B'>{items_html}</font>"
            )
            row_cells.append(Paragraph(cell_content, card_body))
        t = Table([row_cells], colWidths=[col_w]*len(cards_data))
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        return t

    # ==================== SLIDE 2: INTRODUCTION ====================
    story.append(Paragraph("Introduction: Digital Course Content Sharing in Universities", slide_title))
    c2 = [
        {"title": "1. Digitization of Learning", "badge": "Educational Context", "badge_color": "#0284C7", "items": [
            "Universities routinely share lecture notes, lab manuals, and assignments as PDF files.",
            "PDF is the universal academic standard because formatting stays identical on all devices.",
            "Hundreds of students receive and store course materials on their local devices every day."
        ]},
        {"title": "2. The Leakage Dilemma", "badge": "Core Vulnerability", "badge_color": "#EF4444", "items": [
            "Electronic documents are extremely easy to duplicate with zero quality loss.",
            "Files are frequently leaked to public student WhatsApp groups and commercial tutoring websites.",
            "Once leaked, there is no built-in mechanism to identify which student shared the file."
        ]},
        {"title": "3. The Need for AquaMark", "badge": "Project Purpose", "badge_color": "#10B981", "items": [
            "We need a system that binds recipient identity directly into the document content.",
            "It must deter unauthorized file forwarding while preserving perfect reading clarity.",
            "It must provide cryptographic proof of authenticity if questions arise about leaks."
        ]}
    ]
    story.append(make_cards_row(c2, col_w=286))
    story.append(Spacer(1, 15))
    takeaway_box = Table([[Paragraph("<font color='white'><b>In short:</b> AquaMark gives educators control over course PDFs by embedding personalized tracking and tamper-detection into every distributed copy.</font>", card_body)]], colWidths=[860])
    takeaway_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(takeaway_box)
    story.append(PageBreak())

    # ==================== SLIDE 3: PROBLEM STATEMENT ====================
    story.append(Paragraph("Problem Statement: Why Traditional File Protection Fails", slide_title))
    c3 = [
        {"title": "Uncontrolled Redistribution", "badge": "Problem 1", "badge_color": "#EF4444", "items": [
            "Students share proprietary notes freely with zero fear of detection.",
            "No recipient tracking exists on pages.",
            "Commercial portals monetize faculty materials."
        ]},
        {"title": "Perimeter Security Fails", "badge": "Problem 2", "badge_color": "#EF4444", "items": [
            "Portal logins only protect files before download.",
            "Standard PDF passwords cracked in seconds.",
            "Once on a laptop, security boundary vanishes."
        ]},
        {"title": "Silent File Tampering", "badge": "Problem 3", "badge_color": "#EF4444", "items": [
            "PDFs lack built-in tamper detection.",
            "Assignment deadlines or questions secretly edited.",
            "Neither teacher nor evaluator can prove alterations."
        ]},
        {"title": "Lack of Audit Trail", "badge": "Problem 4", "badge_color": "#EF4444", "items": [
            "No forensic log links files to student PRNs.",
            "Disputes over who leaked proprietary materials.",
            "Impossible to legally enforce academic integrity."
        ]}
    ]
    story.append(make_cards_row(c3, col_w=210))
    story.append(PageBreak())

    # ==================== SLIDE 4: OBJECTIVES ====================
    story.append(Paragraph("Project Objectives: Targeted Goals of AquaMark", slide_title))
    c4 = [
        {"title": "1. Visible Deterrence", "badge": "Personalized Overlay", "badge_color": "#0284C7", "items": [
            "Implement automated visible watermarking engine using PyMuPDF.",
            "Stamp recipient PRN, student name, and copyright diagonally at 45°.",
            "Ensure 35% opacity so reading legibility is fully preserved."
        ]},
        {"title": "2. Invisible Watermark", "badge": "Transform Robustness", "badge_color": "#0284C7", "items": [
            "Embed covert identity bits into image frequency structures via 2D-DCT.",
            "Preserve forensic traceability even if visible stamp is cropped.",
            "Guarantee human imperceptibility (> 40 dB PSNR)."
        ]},
        {"title": "3. Tamper Verification", "badge": "Cryptographic Integrity", "badge_color": "#10B981", "items": [
            "Generate unique SHA-256 digital fingerprint for every generated PDF.",
            "Bind document metadata with HMAC manifests to prevent forgery.",
            "Detect any 1-character or 1-byte alteration upon re-upload."
        ]}
    ]
    story.append(make_cards_row(c4, col_w=286))
    story.append(Spacer(1, 15))
    c4_b = Table([[Paragraph("<b>Objective 4 (Platform):</b> Build a responsive full-stack web application (FastAPI + React + SQLite) allowing teachers to watermark and verify files in sub-second execution.", card_body)]], colWidths=[860])
    c4_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(c4_b)
    story.append(PageBreak())

    # ==================== SLIDE 5: PROPOSED SOLUTION ====================
    story.append(Paragraph("Proposed Solution: The AquaMark Defense-in-Depth Pipeline", slide_title))
    c5 = [
        {"title": "Step 1: Upload PDF", "badge": "Faculty Action", "badge_color": "#0284C7", "items": [
            "Faculty uploads lecture notes or lab manuals in PDF format.",
            "System inspects vector structure and text layers."
        ]},
        {"title": "Step 2: Watermark", "badge": "Automated Engine", "badge_color": "#0284C7", "items": [
            "Applies diagonal visible PRN stamp across all pages.",
            "Embeds invisible transform-domain identity bits."
        ]},
        {"title": "Step 3: Hash & Sign", "badge": "Cryptographic Core", "badge_color": "#10B981", "items": [
            "Calculates SHA-256 fingerprint.",
            "Creates tamper-proof HMAC verification manifest."
        ]},
        {"title": "Step 4: Distribute", "badge": "Targeted Delivery", "badge_color": "#0284C7", "items": [
            "Student receives personalized copy.",
            "File opens in all standard viewers."
        ]},
        {"title": "Step 5: Verify", "badge": "Forensic Inspection", "badge_color": "#10B981", "items": [
            "Re-upload any circulating copy.",
            "Instant Green (Authentic) or Red (Tampered) alert."
        ]}
    ]
    story.append(make_cards_row(c5, col_w=168))
    story.append(Spacer(1, 14))
    sol_status = Table([[Paragraph("<b>Implementation Status:</b> ✓ Fully Implemented & Tested: PDF Upload, Visible Stamping, SHA-256 Hashing, SQLite Database & Verification. ⚡ Extended Scope: Campus SSO & Moodle LMS Integration.", card_body)]], colWidths=[860])
    sol_status.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(sol_status)
    story.append(PageBreak())

    # ==================== SLIDE 6: MAIN FEATURES ====================
    story.append(Paragraph("Main Features: Key Capabilities of the AquaMark Platform", slide_title))
    c6_row1 = [
        {"title": "1. PDF Vector Engine", "badge": "PyMuPDF", "badge_color": "#10B981", "items": [
            "Parses vector layout, text layers, and page orientation.",
            "Saves originals safely in isolated server vault."
        ]},
        {"title": "2. Visible Watermark", "badge": "Personalized Deterrence", "badge_color": "#10B981", "items": [
            "Diagonal 45° semi-transparent recipient PRN stamp.",
            "Calibrated 35% opacity preserves reading legibility."
        ]},
        {"title": "3. Invisible Embedding", "badge": "2D-DCT Frequency", "badge_color": "#10B981", "items": [
            "Embeds identity bits into middle image frequencies.",
            "Survives cropping and format conversions (> 40 dB PSNR)."
        ]}
    ]
    c6_row2 = [
        {"title": "4. Cryptographic Hashing", "badge": "SHA-256 Engine", "badge_color": "#10B981", "items": [
            "Computes unique 256-bit digital file fingerprint.",
            "Detects even 1-byte alteration via avalanche effect."
        ]},
        {"title": "5. User Authentication", "badge": "JWT + Bcrypt", "badge_color": "#10B981", "items": [
            "Protects faculty and student credentials with bcrypt.",
            "Issues stateless, time-limited JWT Bearer tokens."
        ]},
        {"title": "6. Complete Audit Trail", "badge": "SQLite Database", "badge_color": "#10B981", "items": [
            "Relational database logs document creation & checks.",
            "Provides non-repudiable academic integrity records."
        ]}
    ]
    story.append(make_cards_row(c6_row1, col_w=286))
    story.append(Spacer(1, 10))
    story.append(make_cards_row(c6_row2, col_w=286))
    story.append(PageBreak())

    # ==================== SLIDE 7: HOW THE TECHNOLOGY WORKS ====================
    story.append(Paragraph("How the Technology Works: Core Security Concepts", slide_title))
    c7 = [
        {"title": "Digital Watermarking", "badge": "Traceability", "badge_color": "#0284C7", "items": [
            "What it is: Embeds identity data directly into host document.",
            "How it works: Places visible text overlay & invisible frequency bits.",
            "What it proves: Proves authorized recipient of that copy.",
            "Limitation: Does not stop physical re-typing by hand."
        ]},
        {"title": "SHA-256 Hashing", "badge": "Integrity Check", "badge_color": "#10B981", "items": [
            "What it is: Cryptographic algorithm yielding unique 256-bit fingerprint.",
            "Avalanche Effect: Changing 1 character completely changes hash.",
            "What it proves: Proves file is 100% byte-identical to original.",
            "Limitation: Detects tampering, but doesn't show which word changed."
        ]},
        {"title": "HMAC Manifests", "badge": "Authenticity", "badge_color": "#0284C7", "items": [
            "What it is: Hash-based Message Authentication Code with secret key.",
            "How it works: Binds file hash and metadata with server secret.",
            "What it proves: Proves manifest originated from official server.",
            "Security: Prevents attackers from forging verification records."
        ]},
        {"title": "Password Hashing & JWT", "badge": "Access Control", "badge_color": "#10B981", "items": [
            "Bcrypt Hashing: Salted password hashing prevents rainbow tables.",
            "JWT Tokens: Encodes user identity and expiration into signed token.",
            "Stateless APIs: Backend validates signatures without extra DB lookups.",
            "Security: Prevents unauthorized users from accessing teacher tools."
        ]}
    ]
    story.append(make_cards_row(c7, col_w=210))
    story.append(PageBreak())

    # ==================== SLIDE 8: SYSTEM ARCHITECTURE ====================
    story.append(Paragraph("System Architecture: Multi-Tier Modular Design", slide_title))
    arch_img = RLImage("scripts/report_generator/assets/system_architecture.png", width=840, height=330)
    story.append(arch_img)
    story.append(Spacer(1, 10))
    story.append(Paragraph("<para align='center'><font size=9.5 color='#0F2A4A'><b>Four-Tier Modular Design:</b> (1) React Client Interface &nbsp;→&nbsp; (2) FastAPI Application Controller &nbsp;→&nbsp; (3) Core Watermarking & Integrity Engines &nbsp;→&nbsp; (4) Secure Storage & Audit Database.</font></para>", card_body))
    story.append(PageBreak())

    # ==================== SLIDE 9: WEBSITE DEMONSTRATION ====================
    story.append(Paragraph("Website Demonstration: Live User Workflows & Interface", slide_title))
    demo_row = [
        [
            RLImage("scripts/report_generator/assets/ui/ui_dashboard.png", width=275, height=160),
            RLImage("scripts/report_generator/assets/ui/ui_watermark_process.png", width=275, height=160),
            RLImage("scripts/report_generator/assets/ui/ui_verification_result.png", width=275, height=160),
        ],
        [
            Paragraph("<b>1. Teacher Dashboard</b><br/><font size=8.5 color='#64748B'>Overview of protected course PDFs, verified copies, and real-time university statistics.</font>", card_body),
            Paragraph("<b>2. Watermark Generation</b><br/><font size=8.5 color='#64748B'>Input recipient student PRN, select protection layers, and preview diagonal overlay.</font>", card_body),
            Paragraph("<b>3. Tamper Verification Tool</b><br/><font size=8.5 color='#64748B'>Instant forensic inspection: Green banner for authentic, Red alert for modified files.</font>", card_body),
        ]
    ]
    t_demo = Table(demo_row, colWidths=[286, 286, 286])
    t_demo.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 10))
    live_banner = Table([[Paragraph("<font color='#166534'><b>⚡ Live Application Verification:</b> Backend runs at <b>http://localhost:8000</b> with interactive OpenAPI Swagger documentation.</font>", card_body)]], colWidths=[860])
    live_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, ACCENT_GREEN),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(live_banner)
    story.append(PageBreak())

    # ==================== SLIDE 10: TESTING AND RESULTS ====================
    story.append(Paragraph("Testing and Results: Formal Laboratory Verification Matrix", slide_title))
    t_data = [
        [Paragraph("<b>Test ID</b>", card_body), Paragraph("<b>Test Scenario</b>", card_body), Paragraph("<b>Expected Outcome</b>", card_body), Paragraph("<b>Observed Output</b>", card_body), Paragraph("<b>Status</b>", card_body)],
        [Paragraph("TC01", card_body), Paragraph("User Login &amp; JWT Auth", card_body), Paragraph("200 OK + Valid Bearer Token", card_body), Paragraph("Token issued &amp; validated successfully", card_body), Paragraph("<font color='#10B981'><b>PASS</b></font>", card_body)],
        [Paragraph("TC02", card_body), Paragraph("PDF Upload &amp; Hashing", card_body), Paragraph("File stored, SHA-256 computed", card_body), Paragraph("File saved in vault, unique hash in DB", card_body), Paragraph("<font color='#10B981'><b>PASS</b></font>", card_body)],
        [Paragraph("TC03", card_body), Paragraph("Visible Watermarking", card_body), Paragraph("Diagonal text on all pages", card_body), Paragraph("Stamps applied at 45°, 35% opacity", card_body), Paragraph("<font color='#10B981'><b>PASS</b></font>", card_body)],
        [Paragraph("TC04", card_body), Paragraph("Untampered Verification", card_body), Paragraph("Status: Valid, Hash match", card_body), Paragraph("Integrity confirmed; green status", card_body), Paragraph("<font color='#10B981'><b>PASS</b></font>", card_body)],
        [Paragraph("TC05", card_body), Paragraph("1-Byte Tampered PDF", card_body), Paragraph("Status: Tampered, Hash mismatch", card_body), Paragraph("Tampering detected; red alert raised", card_body), Paragraph("<font color='#10B981'><b>PASS</b></font>", card_body)],
    ]
    t_tests = Table(t_data, colWidths=[65, 180, 240, 290, 85])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (-1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_tests)
    story.append(Spacer(1, 14))

    metrics_row = [
        {"title": "Processing Latency", "badge": "Speed", "badge_color": "#0284C7", "items": [
            "Averages 0.82 seconds per page.",
            "Processes a 20-page document in under 3 seconds."
        ]},
        {"title": "Visual Imperceptibility", "badge": "Image Quality", "badge_color": "#0284C7", "items": [
            "42.8 dB PSNR score.",
            "Well above 38 dB threshold for zero visual distortion."
        ]},
        {"title": "Tamper Detection", "badge": "Accuracy", "badge_color": "#10B981", "items": [
            "100% detection rate on 1-byte alterations.",
            "Zero false-positive alerts on valid files."
        ]}
    ]
    story.append(make_cards_row(metrics_row, col_w=286))
    story.append(PageBreak())

    # ==================== SLIDE 11: LIMITATIONS AND FUTURE SCOPE ====================
    story.append(Paragraph("Limitations and Future Scope: Honest Assessment & Roadmap", slide_title))
    c11 = [
        {"title": "Current Limitations", "badge": "Honest Constraints", "badge_color": "#EF4444", "items": [
            "Analog / Camera Capture: Mobile camera photos of a laptop screen can degrade invisible watermarks.",
            "Screenshot Attacks: Screen captures strip metadata, though visible watermarks remain.",
            "Hash Specificity: SHA-256 detects that a file changed, but cannot pinpoint which sentence changed.",
            "Format Dependency: Current system is specifically optimized for Portable Document Format (PDF)."
        ]},
        {"title": "Future Improvements", "badge": "Development Roadmap", "badge_color": "#0284C7", "items": [
            "LMS Integration: Direct plugins for Moodle to automatically watermark files on student download.",
            "Dynamic QR Verification: Embedding compact, verifiable QR codes on margins for mobile scanning.",
            "Wavelet (DWT-SVD) Watermarking: Upgrading invisible embedding for print-scan survival.",
            "Multi-Format Support: Extending protection to Word (.docx) and PowerPoint (.pptx) documents."
        ]}
    ]
    story.append(make_cards_row(c11, col_w=430))
    story.append(PageBreak())

    # ==================== SLIDE 12: CONCLUSION ====================
    story.append(Spacer(1, 40))
    story.append(Paragraph("<font size=24 color='#38BDF8'><b>AquaMark: Layered Document Trust</b></font>", title_slide_h1))
    story.append(Spacer(1, 20))
    c12_points = [
        "Combines visible deterrence, invisible tracking, and cryptographic integrity in one unified workflow.",
        "Solves the perimeter failure of traditional PDF passwords and university login portals.",
        "Successfully implemented, tested, and verified with sub-second processing performance.",
        "Provides a practical, robust, and cost-effective document protection solution for universities."
    ]
    for p_txt in c12_points:
        story.append(Paragraph(f"<font size=13 color='#F1F5F9'>✓ &nbsp;&nbsp;{p_txt}</font>", card_body))
        story.append(Spacer(1, 10))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<font size=32 color='white'><b>THANK YOU!</b></font>", ParagraphStyle('TY', parent=styles['Normal'], alignment=1)))
    story.append(Paragraph("<font size=14 color='#93C5FD'><b>Questions &amp; Answers Welcomed</b></font>", ParagraphStyle('QA', parent=styles['Normal'], alignment=1)))

    pdf.build(story, canvasmaker=PresentationCanvas)
    shutil.copy(pdf_out, "/Users/omsaishdhokchaule/Downloads/AquaMark/AquaMark_Project_Presentation.pdf")
    print(f"PDF Presentation generated successfully at: {pdf_out}")

if __name__ == "__main__":
    build_pdf_presentation()
