# Complete Academic Project Report PDF Generator for AquaMark
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

from report_data_front import FRONT_MATTER, ABSTRACT_TEXT
import report_data_ch1_4 as ch1_4
import report_data_ch5_8 as ch5_8
import report_data_ch9_13 as ch9_13
import report_data_appendices as appx

class FormalNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(FormalNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(FormalNumberedCanvas, self).showPage()
        super(FormalNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Cover page (page 1) has no header or footer
        if self._pageNumber > 1:
            # Header
            self.setFont("Times-Bold", 8)
            self.setFillColor(colors.HexColor("#0d9488")) # Teal
            self.drawString(54, letter[1] - 36, "AQUAMARK")
            self.setFont("Times-Roman", 8)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(110, letter[1] - 36, "| Robust Digital Watermarking for Protection of Electronic Course Content")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

            # Footer
            self.setFont("Times-Roman", 8.5)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(54, 34, f"{FRONT_MATTER['department']}, {FRONT_MATTER['college_name']}")
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 54, 34, page_str)
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 46, letter[0] - 54, 46)

        self.restoreState()

def generate_academic_report_pdf(output_path):
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
    body_gray = colors.HexColor("#1e293b")

    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        textColor=primary,
        alignment=1, # Center
        spaceAfter=6
    )

    cover_topic_style = ParagraphStyle(
        'CoverTopic',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=12,
        leading=16,
        textColor=teal,
        alignment=1,
        spaceAfter=24
    )

    cover_meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        textColor=body_gray,
        alignment=1,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=13.5,
        leading=17,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        textColor=teal,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=13,
        textColor=body_gray,
        alignment=4, # Justify
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=13,
        textColor=body_gray,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'DocCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#e2e8f0")
    )

    table_header_style = ParagraphStyle(
        'DocTH',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'DocTD',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7,
        leading=9,
        textColor=body_gray
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>{FRONT_MATTER['college_name'].upper()}</b>", cover_meta_style))
    story.append(Paragraph(f"<b>{FRONT_MATTER['department'].upper()}</b>", cover_meta_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("A PROJECT REPORT ON", cover_meta_style))
    story.append(Paragraph(FRONT_MATTER["project_title"].upper(), cover_title_style))
    story.append(Paragraph(f"Topic: {FRONT_MATTER['official_topic']}", cover_topic_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Submitted in partial fulfillment of the requirements for the award of the degree of<br/>"
                           "<b>BACHELOR OF TECHNOLOGY</b><br/>"
                           "IN<br/>"
                           "<b>COMPUTER SCIENCE AND ENGINEERING (CYBER SECURITY)</b>", cover_meta_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>Submitted by:</b><br/>{FRONT_MATTER['student_name']}<br/>PRN: {FRONT_MATTER['roll_number']}<br/>{FRONT_MATTER['year_semester']}", cover_meta_style))
    story.append(Paragraph(f"<b>Under the Guidance of:</b><br/>{FRONT_MATTER['guide_name']}", cover_meta_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>{FRONT_MATTER['university_name']}</b><br/>Academic Year {FRONT_MATTER['academic_year']}", cover_meta_style))
    story.append(PageBreak())

    # ==================== CERTIFICATE ====================
    story.append(Paragraph(f"<b>{FRONT_MATTER['college_name'].upper()}</b>", cover_meta_style))
    story.append(Paragraph(f"<b>{FRONT_MATTER['department']}</b>", cover_meta_style))
    story.append(Paragraph("<b>BONAFIDE CERTIFICATE</b>", cover_title_style))
    story.append(Spacer(1, 15))

    cert_text = (
        f"This is to certify that this project report entitled \"<b>{FRONT_MATTER['project_title']}</b>\" is the bonafide work "
        f"carried out by <b>{FRONT_MATTER['student_name']}</b> (PRN: {FRONT_MATTER['roll_number']}) in partial fulfillment "
        f"of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering "
        f"(Cyber Security) of {FRONT_MATTER['university_name']} during the academic year {FRONT_MATTER['academic_year']}.<br/><br/>"
        "The project work has been carried out under my supervision and guidance. The contents of this report have not been "
        "submitted to any other University or Institute for the award of any degree or diploma."
    )
    story.append(Paragraph(cert_text, body_style))
    story.append(Spacer(1, 40))

    # Formatted signatories with Dr. Chetan D. Bawankar as HOD
    hod_lines = FRONT_MATTER['head_of_department'].replace("\n", "<br/>")
    sig_data = [
        [Paragraph(f"_________________________<br/><b>Internal Guide:</b><br/>{FRONT_MATTER['guide_name']}<br/>{FRONT_MATTER['department']}", body_style),
         Paragraph(f"_________________________<br/><b>Head of Department:</b><br/><b>{hod_lines}</b>", body_style)]
    ]
    t_sig = Table(sig_data, colWidths=[250, 254])
    t_sig.setStyle(TableStyle([('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
    story.append(t_sig)
    story.append(Spacer(1, 30))

    story.append(Paragraph("Submitted for the University Project Examination held on: ___________________", body_style))
    story.append(Spacer(1, 30))

    exam_data = [
        [Paragraph("_________________________<br/><b>Internal Examiner</b><br/>Signature & Date", body_style),
         Paragraph("_________________________<br/><b>External Examiner</b><br/>Signature & Date", body_style)]
    ]
    t_exam = Table(exam_data, colWidths=[250, 254])
    story.append(t_exam)
    story.append(PageBreak())

    # ==================== DECLARATION ====================
    story.append(Paragraph("<b>DECLARATION</b>", cover_title_style))
    story.append(Spacer(1, 15))
    decl_text = (
        f"I, <b>{FRONT_MATTER['student_name']}</b>, hereby declare that the project report entitled \"<b>{FRONT_MATTER['project_title']}</b>\", "
        f"submitted to the {FRONT_MATTER['department']}, {FRONT_MATTER['college_name']}, "
        "is an authentic record of original work carried out by me under the guidance of "
        f"<b>{FRONT_MATTER['guide_name']}</b>.<br/><br/>"
        "I further declare that this work is original and that all external sources, algorithms, software libraries, and research papers "
        "have been duly cited and acknowledged. This report has not previously formed the basis for the award of any degree, diploma, "
        "associateship, or fellowship at this or any other university or institution."
    )
    story.append(Paragraph(decl_text, body_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Place: Kopargaon<br/>Date:  ___________________", body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>(Signature of the Student)</b><br/>{FRONT_MATTER['student_name']}<br/>PRN: {FRONT_MATTER['roll_number']}", ParagraphStyle('RightSig', parent=body_style, alignment=2)))
    story.append(PageBreak())

    # ==================== ACKNOWLEDGMENT ====================
    story.append(Paragraph("<b>ACKNOWLEDGMENT</b>", cover_title_style))
    story.append(Spacer(1, 15))
    ack_text = (
        "I express my deepest gratitude and sincere appreciation to my esteemed project guide, "
        f"<b>{FRONT_MATTER['guide_name']}</b>, for their invaluable mentorship, insightful technical guidance, and constructive "
        "critiques throughout the conceptualization, design, implementation, and evaluation of this project.<br/><br/>"
        "I extend my sincere thanks to <b>Dr. Chetan D. Bawankar</b>, Head, Department of Cyber Security, School of Engineering and Technology (SET), "
        "Sanjivani University, Kopargaon, as well as faculty members and laboratory staff for providing excellent computational facilities and academic encouragement.<br/><br/>"
        "Finally, I am profoundly grateful to my family, colleagues, and peers for their unwavering moral support, encouragement, "
        "and patience throughout this endeavor."
    )
    story.append(Paragraph(ack_text, body_style))
    story.append(Spacer(1, 25))
    story.append(Paragraph(f"<b>{FRONT_MATTER['student_name']}</b><br/>PRN: {FRONT_MATTER['roll_number']}", ParagraphStyle('RightSig2', parent=body_style, alignment=2)))
    story.append(PageBreak())

    # ==================== ABSTRACT ====================
    story.append(Paragraph("<b>ABSTRACT</b>", cover_title_style))
    story.append(Spacer(1, 10))
    for p_text in ABSTRACT_TEXT.split("\n\n"):
        story.append(Paragraph(p_text, body_style))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ==================== TOC ====================
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", cover_title_style))
    story.append(Spacer(1, 10))
    toc_data = [
        ("Certificate", "iii"), ("Declaration", "iv"), ("Acknowledgment", "v"), ("Abstract", "vi"),
        ("List of Tables", "viii"), ("List of Abbreviations", "ix"),
        ("Chapter 1: Introduction", "1"), ("Chapter 2: Problem Statement and Objectives", "4"),
        ("Chapter 3: Literature Review and Existing Approaches", "6"),
        ("Chapter 4: Proposed System and Research Contribution", "9"),
        ("Chapter 5: System Requirements and Feasibility Study", "11"),
        ("Chapter 6: System Architecture and Detailed Design", "13"),
        ("Chapter 7: Methodology and Mathematical Algorithms", "16"),
        ("Chapter 8: Implementation Details and Module Breakdown", "18"),
        ("Chapter 9: Security Analysis and Threat Model", "21"),
        ("Chapter 10: Testing and Evaluation", "23"),
        ("Chapter 11: Results and Discussion", "25"),
        ("Chapter 12: Limitations and Future Scope", "27"),
        ("Chapter 13: Conclusion", "28"),
        ("References", "29"),
        ("Appendix A: Key Terms and Definitions", "31"),
        ("Appendix B: Core Algorithms Pseudocode", "32"),
        ("Appendix C: Test Case Execution Log", "34"),
        ("Appendix D: User Manual and Operational Walkthrough", "35"),
        ("Appendix E: Installation and Execution Guide", "36")
    ]
    t_toc_rows = []
    for item, pg in toc_data:
        t_toc_rows.append([
            Paragraph(f"<b>{item}</b>" if "Chapter" in item or "References" in item or "Appendix" in item else item, body_style),
            Paragraph(pg, ParagraphStyle('R', parent=body_style, alignment=2))
        ])
    t_toc = Table(t_toc_rows, colWidths=[450, 54])
    t_toc.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor("#f1f5f9"))
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==================== LIST OF TABLES & ABBREVIATIONS ====================
    story.append(Paragraph("<b>LIST OF TABLES</b>", h1_style))
    lot = [
        "Table 3.1: Comparison Matrix of Existing Document Protection Paradigms ........... 7",
        "Table 5.1: System Runtime Dependencies and Verified Library Versions ............... 12",
        "Table 6.1: Database Entities and Relational Schema Specifications .................... 15",
        "Table 9.1: Threat Model and Mitigation Matrix Under Defined Adversary Capabilities ... 22",
        "Table 10.1: Automated Pytest Suite Execution Specifications and Verified Outcomes ..... 23",
        "Table 10.2: Empirical Robustness Laboratory Measurements Under Controlled Image Attacks 24"
    ]
    for l in lot:
        story.append(Paragraph(l, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>LIST OF ABBREVIATIONS</b>", h1_style))
    abbrevs = [
        "<b>2D-DCT:</b> Two-Dimensional Discrete Cosine Transform",
        "<b>AES-GCM:</b> Advanced Encryption Standard in Galois/Counter Mode",
        "<b>API:</b> Application Programming Interface",
        "<b>BER:</b> Bit Error Rate",
        "<b>DFD:</b> Data Flow Diagram",
        "<b>DPI:</b> Dots Per Inch",
        "<b>EdDSA:</b> Edwards-curve Digital Signature Algorithm (Ed25519)",
        "<b>HMAC:</b> Keyed-Hash Message Authentication Code",
        "<b>JWT:</b> JSON Web Token",
        "<b>PDF:</b> Portable Document Format (ISO 32000-1)",
        "<b>PSNR:</b> Peak Signal-to-Noise Ratio (in dB)",
        "<b>SHA-256:</b> Secure Hash Algorithm (256-bit Digest)",
        "<b>UUID:</b> Universally Unique Identifier (v4)"
    ]
    for ab in abbrevs:
        story.append(Paragraph(ab, body_style))
    story.append(PageBreak())

    # ==================== CHAPTERS HELPER ====================
    def emit_chapter_pdf(ch_title, ch_text):
        story.append(Paragraph(f"<b>{ch_title}</b>", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=teal, spaceBefore=2, spaceAfter=8))
        paragraphs = ch_text.strip().split("\n\n")
        for p in paragraphs:
            lines = p.strip().split("\n")
            first = lines[0]
            if len(lines) == 1 and (first.startswith("1.") or first.startswith("2.") or first.startswith("3.") or first.startswith("4.") or first.startswith("5.") or first.startswith("6.") or first.startswith("7.") or first.startswith("8.") or first.startswith("9.") or first.startswith("10.") or first.startswith("11.") or first.startswith("12.") or first.startswith("13.")):
                story.append(Paragraph(f"<b>{first}</b>", h2_style))
            elif first.startswith("Level ") or first.startswith("Summary ") or first.startswith("Test Case ") or first.startswith("Where "):
                story.append(Paragraph(f"<b>{first}</b>", h2_style))
            elif first.startswith("+--") and lines[-1].startswith("+--"):
                # Table block
                raw_rows = [l for l in lines if not l.startswith("+--")]
                if raw_rows:
                    h_cols = [c.strip() for c in raw_rows[0].split("|")[1:-1]]
                    t_rows = [[Paragraph(f"<b>{h}</b>", table_header_style) for h in h_cols]]
                    for r in raw_rows[1:]:
                        r_vals = [c.strip() for c in r.split("|")[1:-1]]
                        t_rows.append([Paragraph(v, table_cell_style) for v in r_vals])
                    
                    col_w = 504.0 / len(h_cols)
                    t_rendered = Table(t_rows, colWidths=[col_w] * len(h_cols))
                    t_rendered.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), primary),
                        ('TOPPADDING', (0,0), (-1,-1), 3),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                        ('LEFTPADDING', (0,0), (-1,-1), 4),
                        ('RIGHTPADDING', (0,0), (-1,-1), 4),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
                    ]))
                    story.append(t_rendered)
                    story.append(Spacer(1, 6))
            elif first.startswith("+-") or first.startswith("  * ") or first.startswith("1: ") or first.startswith("="):
                # Code / Diagram block
                clean_str = "<br/>".join(lines).replace(" ", "&nbsp;")
                t_code = Table([[Paragraph(clean_str, code_style)]], colWidths=[504])
                t_code.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                    ('RIGHTPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 5),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ]))
                story.append(t_code)
                story.append(Spacer(1, 6))
            else:
                for line in lines:
                    if line.startswith("- ") or line.startswith("• ") or line.startswith("* "):
                        story.append(Paragraph(f"• {line[2:]}", bullet_style))
                    elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or line.startswith("4. ") or line.startswith("5. ") or line.startswith("6. "):
                        story.append(Paragraph(line, bullet_style))
                    else:
                        story.append(Paragraph(line, body_style))
        story.append(PageBreak())

    emit_chapter_pdf(ch1_4.CHAPTER_1_TITLE, ch1_4.CHAPTER_1_TEXT)
    emit_chapter_pdf(ch1_4.CHAPTER_2_TITLE, ch1_4.CHAPTER_2_TEXT)
    emit_chapter_pdf(ch1_4.CHAPTER_3_TITLE, ch1_4.CHAPTER_3_TEXT)
    emit_chapter_pdf(ch1_4.CHAPTER_4_TITLE, ch1_4.CHAPTER_4_TEXT)
    emit_chapter_pdf(ch5_8.CHAPTER_5_TITLE, ch5_8.CHAPTER_5_TEXT)
    emit_chapter_pdf(ch5_8.CHAPTER_6_TITLE, ch5_8.CHAPTER_6_TEXT)
    emit_chapter_pdf(ch5_8.CHAPTER_7_TITLE, ch5_8.CHAPTER_7_TEXT)
    emit_chapter_pdf(ch5_8.CHAPTER_8_TITLE, ch5_8.CHAPTER_8_TEXT)
    emit_chapter_pdf(ch9_13.CHAPTER_9_TITLE, ch9_13.CHAPTER_9_TEXT)
    emit_chapter_pdf(ch9_13.CHAPTER_10_TITLE, ch9_13.CHAPTER_10_TEXT)
    emit_chapter_pdf(ch9_13.CHAPTER_11_TITLE, ch9_13.CHAPTER_11_TEXT)
    emit_chapter_pdf(ch9_13.CHAPTER_12_TITLE, ch9_13.CHAPTER_12_TEXT)
    emit_chapter_pdf(ch9_13.CHAPTER_13_TITLE, ch9_13.CHAPTER_13_TEXT)

    # REFERENCES
    story.append(Paragraph("<b>References</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=teal, spaceBefore=2, spaceAfter=8))
    for ref in ch9_13.REFERENCES_TEXT.strip().split("\n"):
        story.append(Paragraph(ref, body_style))
        story.append(Spacer(1, 2))
    story.append(PageBreak())

    # APPENDICES
    emit_chapter_pdf(appx.APPENDIX_A_TITLE, appx.APPENDIX_A_TEXT)
    emit_chapter_pdf(appx.APPENDIX_B_TITLE, appx.APPENDIX_B_TEXT)
    emit_chapter_pdf(appx.APPENDIX_C_TITLE, appx.APPENDIX_C_TEXT)
    emit_chapter_pdf(appx.APPENDIX_D_TITLE, appx.APPENDIX_D_TEXT)
    emit_chapter_pdf(appx.APPENDIX_E_TITLE, appx.APPENDIX_E_TEXT)

    doc.build(story, canvasmaker=FormalNumberedCanvas)
    print(f"Successfully generated academic report PDF at: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "AquaMark_Full_Project_Report.pdf"
    generate_academic_report_pdf(out)
