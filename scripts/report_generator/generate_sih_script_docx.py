import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os
import shutil

doc = docx.Document()

# Page Margins
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.25)
    s.right_margin = Inches(1.0)
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)

COLOR_NAVY = RGBColor(15, 42, 74)
COLOR_ORANGE = RGBColor(249, 115, 22)
COLOR_DARK = RGBColor(30, 41, 59)
COLOR_MUTED = RGBColor(100, 116, 139)

def add_header():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run("SANJIVANI UNIVERSITY, KOPARGAON\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(13)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY

    r2 = p.add_run("DEPARTMENT OF CYBER SECURITY | SCHOOL OF ENGINEERING AND TECHNOLOGY\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_ORANGE

    r3 = p.add_run("Course: Cryptography & Information Security (24UCYPC301) | A.Y. 2026-2027\n")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = COLOR_MUTED

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(14)
    rt = p_title.add_run("AQUAMARK SIH-STYLE 6-SLIDE PRESENTATION SPEAKING SCRIPT & VIVA DEFENSE GUIDE\n")
    rt.font.name = "Times New Roman"
    rt.font.size = Pt(15)
    rt.font.bold = True
    rt.font.color.rgb = COLOR_NAVY

    r_meta = p_title.add_run("Presenter: Sanjivani Rameshwar More (PRN: 2124UCSM1115, Roll No. A-15)\nGuide: Dr. Chetan D. Bawankar (HOD, Dept. of Cyber Security) | PS Code: CIS-105")
    r_meta.font.name = "Times New Roman"
    r_meta.font.size = Pt(10.5)
    r_meta.font.italic = True
    r_meta.font.color.rgb = COLOR_DARK

add_header()

p_intro = doc.add_paragraph()
p_intro.paragraph_format.line_spacing = 1.35
p_intro.paragraph_format.space_after = Pt(14)
r_in = p_intro.add_run(
    "Guide Overview: This document provides the complete, natural speaking notes for your 6-slide SIH-style presentation "
    "('AquaMark_SIH_Style_Presentation.pptx'). Each slide is designed for 45 to 60 seconds of speaking time, allowing you to "
    "confidently complete your classroom evaluation in approximately 5 to 6 minutes, followed by viva question defense."
)
r_in.font.name = "Times New Roman"
r_in.font.size = Pt(11)

slides_data = [
    {
        "slide_num": 1,
        "title": "Slide 1: Project Cover",
        "objective": "Introduce yourself, the official problem statement CIS-105, department, and project guide with professional presence.",
        "script": "Respected Dr. Chetan Bawankar sir, Mr. Kunal Makar sir, and dear classmates. My name is Sanjivani Rameshwar More, studying in Third Year Cyber Security. Today, I am presenting our project under the Smart India Hackathon prototype framework: AquaMark — Secure Digital Watermarking and Document Integrity Platform. This project is submitted for Problem Statement CIS-105 under the domain of Steganography, Watermarking, and Digital Forensics.",
        "tip": "Speak with confident posture. Point toward the QR code and mention that it links directly to our verified GitHub repository.",
        "viva_q": "Why is the problem statement titled 'Robust Digital Watermarking for Electronic Course Content'?",
        "viva_a": "Because in modern universities, lecture notes and lab manuals are shared as PDFs, which are easily leaked or modified without permission. This project builds a robust watermarking and tamper-detection platform specifically tailored for academic content."
    },
    {
        "slide_num": 2,
        "title": "Slide 2: Proposed Solution & Project Overview",
        "objective": "Present the 5 core capabilities on the left and the 3-step security workflow on the right.",
        "script": "Sir, on this slide you can see our proposed solution. On the left are our five key capabilities: PDF Watermarking, Document Traceability, File Integrity Checking, Secure Access Control, and Document Management. On the right is our core security workflow in three simple steps: first, the faculty uploads a course PDF; second, AquaMark applies a diagonal visible PRN stamp and computes a cryptographic SHA-256 hash; and third, any circulating document can be re-uploaded to instantly verify authenticity and detect modifications.",
        "tip": "Explain that every feature shown is already fully implemented and runs in sub-1.2 seconds.",
        "viva_q": "What happens if a student shares their watermarked document on a public forum?",
        "viva_a": "The visible watermark displaying their PRN immediately identifies who originally downloaded the file, creating strong psychological deterrence."
    },
    {
        "slide_num": 3,
        "title": "Slide 3: Technical Approach & Architecture",
        "objective": "Detail the technical stack (React, FastAPI, PyMuPDF, SQLite) and system architecture diagram.",
        "script": "This slide outlines our technical architecture and technology stack. On the left are our implementation tools: React and Tailwind for a responsive web interface, FastAPI and Python for high-performance asynchronous APIs, PyMuPDF for vector PDF manipulation, and hashlib for SHA-256 cryptographic hashing. On the right is our system architecture diagram showing how requests travel securely from the user interface down to our SQLite vault. Below are our live FastAPI backend at port 8000 and our verified GitHub repository.",
        "tip": "Emphasize that the system uses real, standard Python libraries and follows clean REST API principles.",
        "viva_q": "Why is FastAPI used instead of traditional Flask?",
        "viva_a": "FastAPI is natively asynchronous, provides automatic Swagger API documentation, and delivers the high throughput needed to handle multi-page PDF operations rapidly."
    },
    {
        "slide_num": 4,
        "title": "Slide 4: Feasibility and Viability Analysis",
        "objective": "Demonstrate the feasibility, zero licensing cost, campus adoption, and layered security model.",
        "script": "Sir, this slide addresses the feasibility and viability of AquaMark. In the left panel, we highlight our Academic Security Guarantee: sub-second execution, zero licensing costs, and standard PDF compatibility across all devices. On the right, we break this down into four pillars: Technical Feasibility using stable tools; Low Cost by leveraging open-source software; Practical Campus Adoption with zero new hardware required; and our Layered Security Model combining visible deterrence with cryptographic hash verification.",
        "tip": "Highlight that colleges can adopt AquaMark immediately on their existing computers without buying expensive commercial tools.",
        "viva_q": "Does AquaMark require installing custom viewer software on student phones?",
        "viva_a": "No, sir. The protected files remain standard PDFs that open in any browser, Adobe Acrobat, or mobile reader without requiring plugins."
    },
    {
        "slide_num": 5,
        "title": "Slide 5: Impact and Institutional Benefits",
        "objective": "Explain the 5 institutional benefits and conclude with the unified mission banner.",
        "script": "Here we highlight the institutional impact of AquaMark across five key benefits: Benefit 1 is Source Identification through recipient PRNs; Benefit 2 is Integrity Checking using SHA-256; Benefit 3 is Document Traceability with an auditable history; Benefit 4 is an Organized Workflow replacing informal file sharing; and Benefit 5 is Educational Security protecting faculty intellectual property. As our bottom banner states: AquaMark supports safer sharing and better traceability of educational documents.",
        "tip": "Read the bottom banner clearly and emphasize that the system encourages safe academic sharing rather than restricting learning.",
        "viva_q": "Does a digital watermark completely prevent a student from copying text?",
        "viva_a": "No security tool can prevent someone from manually re-typing words. What watermarking achieves is source traceability and deterrence against mass unauthorized redistribution."
    },
    {
        "slide_num": 6,
        "title": "Slide 6: Research and Technical References",
        "objective": "Cite the authentic academic publications and international standards supporting the project.",
        "script": "Finally, this slide cites the foundational research and global standards supporting AquaMark. We referenced Cox and Miller's textbook for digital watermarking theory, ISO 32000-1 for PDF vector specifications, William Stallings for cryptographic network security, Ahmed's 1974 IEEE paper for Discrete Cosine Transform, Hsu's research for frequency-domain robustness, and NIST FIPS 180-4 for SHA-256 secure hashing. Thank you very much, respected teachers. I am now open to your questions.",
        "tip": "Smile, maintain eye contact, and invite viva questions from the panel.",
        "viva_q": "What is the role of NIST FIPS 180-4 in your project?",
        "viva_a": "It is the official federal standard defining the Secure Hash Algorithm (SHA-256), ensuring our integrity verification follows globally standardized cryptographic rules."
    }
]

for s in slides_data:
    p_s_hdr = doc.add_paragraph()
    p_s_hdr.paragraph_format.space_before = Pt(14)
    p_s_hdr.paragraph_format.space_after = Pt(4)
    r_sh = p_s_hdr.add_run(f"SLIDE {s['slide_num']}: {s['title'].upper()}")
    r_sh.font.name = "Times New Roman"
    r_sh.font.size = Pt(13)
    r_sh.font.bold = True
    r_sh.font.color.rgb = COLOR_NAVY

    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(4.7)

    labels = [
        ("Slide Objective", s['objective']),
        ("Speaking Script (45-60s)", f"\"{s['script']}\""),
        ("Speaking Tips", s['tip']),
        ("Expected Viva Question", s['viva_q']),
        ("Recommended Viva Answer", s['viva_a'])
    ]

    for idx, (lbl, val) in enumerate(labels):
        row = table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(lbl)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY if idx != 1 else COLOR_ORANGE

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.line_spacing = 1.2
        r1 = p1.add_run(val)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10)
        if idx == 1:
            r1.font.bold = True
            r1.font.color.rgb = COLOR_DARK
        elif idx == 4:
            r1.font.color.rgb = RGBColor(22, 101, 52)
        else:
            r1.font.color.rgb = COLOR_DARK

        for cell in [c0, c1]:
            tcPr = cell._element.get_or_add_tcPr()
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{"F8FAFC" if idx % 2 == 0 else "FFFFFF"}"/>')
            tcPr.append(shd)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

docx_out = "/Users/omsaishdhokchaule/Downloads/AquaMark_Presentation_Script.docx"
doc.save(docx_out)
print(f"Presentation script saved successfully at: {docx_out}")

shutil.copy(docx_out, "/Users/omsaishdhokchaule/Downloads/AquaMark/AquaMark_Presentation_Script.docx")
