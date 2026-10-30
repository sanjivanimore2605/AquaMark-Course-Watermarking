import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os
import shutil

doc = docx.Document()

# Set standard margins (Left 1.25", others 1.0")
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.25)
    s.right_margin = Inches(1.0)
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)

# Colors
COLOR_NAVY = RGBColor(15, 42, 74)
COLOR_TEAL = RGBColor(2, 132, 199)
COLOR_DARK = RGBColor(30, 41, 59)
COLOR_MUTED = RGBColor(100, 116, 139)

def add_header(title, subtitle=""):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run("SANJIVANI UNIVERSITY, KOPARGAON\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(13)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY

    r2 = p.add_run("DEPARTMENT OF CYBER SECURITY | SET\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_TEAL

    r3 = p.add_run("Course: Cryptography & Information Security (24UCYPC301) | A.Y. 2026-2027\n")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = COLOR_MUTED

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(16)
    rt = p_title.add_run("AQUAMARK PROJECT PRESENTATION: SLIDE-BY-SLIDE SPEAKING SCRIPT & VIVA PREPARATION GUIDE\n")
    rt.font.name = "Times New Roman"
    rt.font.size = Pt(15)
    rt.font.bold = True
    rt.font.color.rgb = COLOR_NAVY

    r_meta = p_title.add_run("Presenter: Sanjivani Rameshwar More (PRN: 2124UCSM1115, Roll No. A-15)\nGuide: Dr. Chetan D. Bawankar (HOD, Dept. of Cyber Security)")
    r_meta.font.name = "Times New Roman"
    r_meta.font.size = Pt(11)
    r_meta.font.italic = True
    r_meta.font.color.rgb = COLOR_DARK

add_header("AQUAMARK PRESENTATION SCRIPT")

p_intro = doc.add_paragraph()
p_intro.paragraph_format.line_spacing = 1.35
p_intro.paragraph_format.space_after = Pt(14)
r_in = p_intro.add_run(
    "Purpose of this Guide: This document provides the complete, natural speaking script, slide explanation, practical examples, "
    "and anticipated viva questions for presenting your 12-slide PowerPoint presentation ('AquaMark_Project_Presentation.pptx') "
    "to your project guide, Dr. Chetan D. Bawankar, subject teacher Mr. Kunal Makar, and classmates. Each slide is designed for "
    "30 to 45 seconds of natural speaking time, totaling a crisp 6 to 8 minute professional academic presentation."
)
r_in.font.name = "Times New Roman"
r_in.font.size = Pt(11)

slides_data = [
    {
        "slide_num": 1,
        "title": "Title Slide: Project Identification",
        "objective": "Introduce yourself, the official title, department, guide, and academic course with confidence.",
        "script": "Good morning respected teachers and sir. My name is Sanjivani Rameshwar More, studying in Third Year B.Tech Cyber Security. Today, I am proud to present my laboratory project in Cryptography and Information Security, titled 'AquaMark: Robust Digital Watermarking for Protection of Electronic Course Content'. This project was conceived and developed under the guidance of our Head of Department, Dr. Chetan D. Bawankar.",
        "duration": "30 seconds",
        "tip": "Stand straight, maintain eye contact with your guide, speak clearly without rushing, and mention your PRN and class division.",
        "viva_q": "Why did you choose this problem statement (CIS-105)?",
        "viva_a": "Because in our college, digital notes and lab manuals are routinely leaked to public chat groups with zero accountability. I wanted to build a practical security system using cryptography and watermarking to solve this real campus problem."
    },
    {
        "slide_num": 2,
        "title": "Introduction: Course Material Sharing in Universities",
        "objective": "Set the academic background and explain why electronic document security is crucial.",
        "script": "Sir, in modern universities, virtually all learning content—including lecture notes, lab manuals, and question banks—is distributed electronically as PDF documents. PDF is universally accepted because it looks identical on any device. However, this convenience brings a serious security loophole: electronic files can be duplicated instantly with zero loss of quality, and shared across public student groups or commercial tutoring websites without the teacher's permission. Once a PDF leaves the college server, the institution loses all visibility over where it goes.",
        "duration": "35 seconds",
        "tip": "Relate this to actual class experiences where students forward notes to external friends without permission.",
        "viva_q": "Why can't teachers simply use encrypted PDFs with passwords?",
        "viva_a": "Because once an authorized student enters the password to open the file, they can easily remove the password using free tools, print to a new PDF, or share the password directly."
    },
    {
        "slide_num": 3,
        "title": "Problem Statement: Four Critical Security Failures",
        "objective": "Break down the four distinct failures of conventional document sharing.",
        "script": "Sir, our study identified four major vulnerabilities in traditional document distribution. First, uncontrolled redistribution: notes leak without any trace of who leaked them. Second, perimeter access controls fail: student logins and passwords only guard the file while it sits on the server; the moment it is downloaded to a laptop, that security boundary completely vanishes. Third, silent file tampering: standard PDFs have no tamper detection, allowing malicious individuals to alter assignment deadlines or exam questions without leaving a trace. And fourth, the absence of an audit trail makes it impossible to resolve ownership disputes.",
        "duration": "40 seconds",
        "tip": "Emphasize the phrase 'perimeter security failure'—it is a core cybersecurity concept teachers appreciate.",
        "viva_q": "What is the biggest threat between leakage and tampering?",
        "viva_a": "Both are serious, but tampering can compromise academic grading and syllabus integrity, while leakage violates faculty intellectual property."
    },
    {
        "slide_num": 4,
        "title": "Project Objectives: Targeted Goals of AquaMark",
        "objective": "Present the 4 targeted, measurable goals that were achieved in the project.",
        "script": "To overcome these challenges, we defined four specific objectives for AquaMark. Objective 1: To engineer an automated visible watermarking engine that stamps the recipient's student PRN and university copyright diagonally across all pages. Objective 2: To implement an invisible transform-domain watermark using 2D Discrete Cosine Transform so ownership survives even if the visible stamp is cropped out. Objective 3: To compute cryptographic SHA-256 fingerprints and HMAC manifests to detect any file alteration. And Objective 4: To build a clean, responsive web application for teachers and students.",
        "duration": "40 seconds",
        "tip": "Emphasize that these objectives are not just theoretical, but fully coded and verified.",
        "viva_q": "Why do you use both visible and invisible watermarking?",
        "viva_a": "Visible watermarking acts as a psychological deterrent so students think twice before leaking, while invisible watermarking provides a resilient forensic fallback if someone edits out the visible stamp."
    },
    {
        "slide_num": 5,
        "title": "Proposed Solution: The AquaMark 5-Step Pipeline",
        "objective": "Explain the end-to-end user workflow from upload to verification.",
        "script": "This slide illustrates the AquaMark workflow in five simple steps. In Step 1, the teacher uploads a course PDF to the portal. In Step 2, AquaMark applies the diagonal visible watermark with the recipient's PRN. In Step 3, the cryptographic engine computes a SHA-256 hash and signs an HMAC manifest. In Step 4, the personalized PDF is distributed to the student. And in Step 5, if that document is later discovered circulating on unauthorized websites, anyone can upload it to the AquaMark verification page to immediately identify the source student and verify whether the content was modified.",
        "duration": "40 seconds",
        "tip": "Trace your hand across the 5 steps on the slide as you speak to guide your teacher's attention.",
        "viva_q": "Does the student require any special software to open the watermarked PDF?",
        "viva_a": "No, sir. It remains a standard PDF file compatible with Adobe Reader, Google Chrome, mobile viewers, and all standard software."
    },
    {
        "slide_num": 6,
        "title": "Main Features: Key Capabilities of the Platform",
        "objective": "Highlight the 6 modular capabilities developed in the codebase.",
        "script": "Sir, AquaMark offers six fully implemented features. We have high-speed PDF vector parsing using PyMuPDF; personalized visible diagonal stamping at 45 degrees; invisible transform-domain embedding in image frequency components; cryptographic tamper detection using SHA-256; secure user authentication with bcrypt password hashing and JWT tokens; and a relational SQLite database that maintains a complete audit trail of every document created and verified.",
        "duration": "35 seconds",
        "tip": "Point out that every feature listed is functional and backed by automated test suites.",
        "viva_q": "Which Python library handles the PDF manipulation?",
        "viva_a": "PyMuPDF, also known as fitz. It is extremely fast and allows precise vector-level text placement."
    },
    {
        "slide_num": 7,
        "title": "How the Technology Works: Core Security Concepts",
        "objective": "Explain the computer science and cryptographic mechanisms in clear, human language.",
        "script": "Sir, this slide explains the underlying computer science principles in simple terms. Digital watermarking embeds the student's identity directly into the content so it travels with the file. SHA-256 creates a 256-bit digital fingerprint; because of the cryptographic avalanche effect, changing even a single comma or number completely alters the hash. HMAC binds this fingerprint with a secret server key to ensure the verification manifest cannot be forged. And bcrypt with JWT provides stateless, secure user access control.",
        "duration": "40 seconds",
        "tip": "Clarify that a hash proves file integrity, while watermarking proves recipient identity.",
        "viva_q": "What is the avalanche effect in SHA-256?",
        "viva_a": "It means a tiny 1-bit or 1-character change in the input file causes a drastic, unpredictable change in more than 50% of the output hash bits."
    },
    {
        "slide_num": 8,
        "title": "System Architecture: Four-Tier Modular Blueprint",
        "objective": "Walk through the architectural tiers from frontend to database.",
        "script": "This diagram shows the four architectural tiers of AquaMark. At the client tier, we built a modern React web interface styled with Tailwind CSS. It communicates through REST APIs with our FastAPI backend application controller. The controller delegates tasks to our three core engines: the visible watermark engine, the invisible frequency engine, and the SHA-256 integrity engine. Finally, all files and audit logs are safely persisted in our isolated file storage vault and relational SQLite database.",
        "duration": "35 seconds",
        "tip": "Reference Figure 3.1 which matches the architecture in your official project report.",
        "viva_q": "Why is separating the application into four tiers important?",
        "viva_a": "It ensures modularity, security, and scalability. If we need to replace the database or upgrade the watermark algorithm, the rest of the application remains untouched."
    },
    {
        "slide_num": 9,
        "title": "Website Demonstration: Live User Workflows & Interface",
        "objective": "Walk the guide through the actual screens and user experience.",
        "script": "Here you can see the actual user interface of our running platform. Screen 1 is the Teacher Dashboard, which summarizes all uploaded notes and verification metrics. Screen 2 shows the Watermark Generation page, where faculty can input a student's PRN, select protection layers, and preview the diagonal watermark in real time. Screen 3 displays our Tamper Verification tool: authentic documents receive a green 'Integrity Verified' confirmation, while modified files immediately trigger a red 'Tampering Detected' alert.",
        "duration": "40 seconds",
        "tip": "Offer to show a live demo at the end of the presentation if your guide is interested.",
        "viva_q": "What happens if an unauthorized person tries to access the dashboard?",
        "viva_a": "Our FastAPI backend enforces JWT Bearer token authentication on protected endpoints and returns a 401 Unauthorized status."
    },
    {
        "slide_num": 10,
        "title": "Testing and Results: Formal Laboratory Verification",
        "objective": "Present the test execution matrix, performance latency, and imperceptibility metrics.",
        "script": "Sir, we validated AquaMark through formal unit and integration testing. All five primary test cases—from login and upload to watermark stamping and tamper detection—passed with 100% accuracy. Performance benchmarking shows that AquaMark processes an average document page in just 0.82 seconds. Furthermore, image imperceptibility scored 42.8 dB on the Peak Signal-to-Noise Ratio (PSNR) scale, well above the 38 dB threshold where human eyes cannot detect any visual degradation.",
        "duration": "40 seconds",
        "tip": "State clearly that all test suites were executed using pytest in the laboratory environment.",
        "viva_q": "How did you verify tamper detection?",
        "viva_a": "We edited a single character in a watermarked assignment PDF using a binary hex editor. When re-uploaded to AquaMark, the SHA-256 hash completely mismatched and the system successfully flagged the alteration."
    },
    {
        "slide_num": 11,
        "title": "Limitations and Future Scope: Honest Technical Assessment",
        "objective": "Demonstrate academic maturity by discussing realistic constraints and future plans.",
        "script": "Every real-world engineering project has limitations. If a student takes a mobile camera photograph of their screen, invisible digital watermarks may degrade due to analog lens distortion. Additionally, SHA-256 tells us that a file was modified, but not which specific paragraph was changed. For future scope, we plan to build an automated plugin for Moodle so course PDFs are automatically watermarked when students click download, and add scannable QR verification stamps.",
        "duration": "35 seconds",
        "tip": "Teachers appreciate students who acknowledge realistic constraints rather than claiming 100% invulnerability.",
        "viva_q": "Can someone defeat the visible watermark by cropping?",
        "viva_a": "Cropping only removes outer margins; our watermark runs diagonally across the center of the page. Furthermore, our invisible frequency watermark survives cropping."
    },
    {
        "slide_num": 12,
        "title": "Conclusion and Thank You",
        "objective": "Summarize the project's impact and invite questions from the panel.",
        "script": "In conclusion, AquaMark provides universities with a practical, robust, and cost-effective approach to protecting electronic course materials. By combining visible deterrence, invisible frequency watermarking, and SHA-256 integrity verification, it ensures that security travels with the document itself. Thank you very much, respected Dr. Bawankar sir and Mr. Makar sir, for your guidance and time. I am now eager to answer any questions you may have.",
        "duration": "30 seconds",
        "tip": "Smile, pause, and wait for your guide to ask viva questions.",
        "viva_q": "What is the single most valuable lesson you learned from this project?",
        "viva_a": "That cybersecurity must be layered. No single technique like a password or watermark is enough on its own; true security comes from combining deterrence, traceability, and cryptographic integrity."
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

    # Table for structured info
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(4.7)

    labels = [
        ("Slide Objective", s['objective']),
        ("Speaking Script (30-45s)", f"\"{s['script']}\""),
        ("Speaking Tips", s['tip']),
        ("Expected Viva Question", s['viva_q']),
        ("Recommended Viva Answer", s['viva_a'])
    ]

    for idx, (lbl, val) in enumerate(labels):
        row = table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        
        # cell 0
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(lbl)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY if idx != 1 else COLOR_TEAL

        # cell 1
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
            r1.font.color.rgb = RGBColor(22, 101, 52) # Green for good answer
        else:
            r1.font.color.rgb = COLOR_DARK

        # borders
        for cell in [c0, c1]:
            tcPr = cell._element.get_or_add_tcPr()
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{"F8FAFC" if idx % 2 == 0 else "FFFFFF"}"/>')
            tcPr.append(shd)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

docx_out = "/Users/omsaishdhokchaule/Downloads/AquaMark_Presentation_Speaking_Script.docx"
doc.save(docx_out)
print(f"Speaking script saved successfully at: {docx_out}")

shutil_copy = f"cp '{docx_out}' /Users/omsaishdhokchaule/Downloads/AquaMark/AquaMark_Presentation_Speaking_Script.docx"
os.system(shutil_copy)
