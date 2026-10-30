import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# 1. Initialize Presentation with 16:9 widescreen dimensions (13.333 x 7.5 in)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# SIH Reference Color Palette
DARK_NAVY = RGBColor(15, 42, 74)       # #0F2A4A - Primary Text & Navy Panels
ACCENT_ORANGE = RGBColor(249, 115, 22) # #F97316 - SIH Orange Accent / Badges
ACCENT_BLUE = RGBColor(2, 132, 199)    # #0284C7 - SIH Blue Links / Icons
ACCENT_GREEN = RGBColor(16, 185, 129)  # #10B981 - Small Green Accents
BG_WHITE = RGBColor(255, 255, 255)     # #FFFFFF - Clean White Background
CARD_BG = RGBColor(255, 255, 255)      # #FFFFFF - White Card
CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 - Subtle Gray Border
TEXT_DARK = RGBColor(30, 41, 59)       # #1E293B - Charcoal Body Text
TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B - Gray Metadata
FOOTER_LINE = RGBColor(186, 230, 253)  # #BAE6FD - Thin Blue Footer Line

# Standard Footer Helper (Matches SIH Reference)
def add_sih_footer(slide, slide_num, total_slides=6):
    # Thin horizontal line above footer
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = FOOTER_LINE
    line.line.color.rgb = FOOTER_LINE

    # Left footer: Project tracking
    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(6.0), Inches(0.35))
    tf_l = tb_left.text_frame
    p_l = tf_l.paragraphs[0]
    p_l.text = "AquaMark | Robust Digital Watermarking for Protection of Electronic Course Content"
    p_l.font.name = "Arial"
    p_l.font.size = Pt(8.5)
    p_l.font.color.rgb = TEXT_MUTED

    # Right footer: Page / Template tracking
    tb_right = slide.shapes.add_textbox(Inches(8.5), Inches(6.98), Inches(4.033), Inches(0.35))
    tf_r = tb_right.text_frame
    p_r = tf_r.paragraphs[0]
    p_r.text = f"@SIH Idea submission- Template  |  {slide_num} / {total_slides}"
    p_r.font.name = "Arial"
    p_r.font.size = Pt(8.5)
    p_r.font.color.rgb = TEXT_MUTED
    p_r.alignment = PP_ALIGN.RIGHT

# Standard Slide Header (Matches SIH Center Bold Layout)
def add_sih_header(slide, title_text):
    # Top Tag
    tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.3))
    tf_tag = tb_tag.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "SMART INDIA HACKATHON 2026  |  COLLEGE LABORATORY EVALUATION"
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_ORANGE
    p_tag.alignment = PP_ALIGN.CENTER

    # Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.733), Inches(0.65))
    tf_t = tb_title.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Arial"
    p_t.font.size = Pt(25)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_NAVY
    p_t.alignment = PP_ALIGN.CENTER

# Helper for building rounded feature cards with icons
def add_feature_card(slide, left, top, width, height, icon_char, title, desc, tag=""):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1.5)

    # Icon circle / badge on left
    icon_circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.15), top + Inches(0.15), Inches(0.55), Inches(0.55))
    icon_circle.fill.solid()
    icon_circle.fill.fore_color.rgb = RGBColor(254, 243, 199) # soft amber
    icon_circle.line.color.rgb = ACCENT_ORANGE
    icon_circle.line.width = Pt(1.5)

    tf_ic = icon_circle.text_frame
    p_ic = tf_ic.paragraphs[0]
    p_ic.text = icon_char
    p_ic.font.name = "Arial"
    p_ic.font.size = Pt(14)
    p_ic.font.bold = True
    p_ic.font.color.rgb = ACCENT_ORANGE
    p_ic.alignment = PP_ALIGN.CENTER

    # Text box
    tb = slide.shapes.add_textbox(left + Inches(0.8), top + Inches(0.1), width - Inches(0.9), height - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.name = "Arial"
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_NAVY

    if tag:
        r_tag = p_t.add_run()
        r_tag.text = f"  [{tag}]"
        r_tag.font.size = Pt(9)
        r_tag.font.bold = True
        r_tag.font.color.rgb = ACCENT_ORANGE

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = "Arial"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(3)

slides_notes = {}

# ==============================================================================
# SLIDE 1 — PROJECT COVER (Matches Page 1 of Reference)
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)

# Top Orange Branding Pill
pill = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(3.2), Inches(0.35))
pill.fill.solid()
pill.fill.fore_color.rgb = ACCENT_ORANGE
pill.line.color.rgb = ACCENT_ORANGE
tf_p = pill.text_frame
p_p = tf_p.paragraphs[0]
p_p.text = "SMART INDIA HACKATHON 2026"
p_p.font.name = "Arial"
p_p.font.size = Pt(10)
p_p.font.bold = True
p_p.font.color.rgb = RGBColor(255, 255, 255)
p_p.alignment = PP_ALIGN.CENTER

# Main Title & Subtitle on Left
tb_c1 = slide1.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(7.2), Inches(1.8))
tf_c1 = tb_c1.text_frame
tf_c1.word_wrap = True

p_c1 = tf_c1.paragraphs[0]
p_c1.text = "AquaMark"
p_c1.font.name = "Arial"
p_c1.font.size = Pt(36)
p_c1.font.bold = True
p_c1.font.color.rgb = DARK_NAVY

p_sub = tf_c1.add_paragraph()
p_sub.text = "Secure Digital Watermarking and Document Integrity Platform"
p_sub.font.name = "Arial"
p_sub.font.size = Pt(16)
p_sub.font.bold = True
p_sub.font.color.rgb = ACCENT_BLUE
p_sub.space_before = Pt(4)

# 2-Column Info Grid (Matches SIH Left Table)
grid_data = [
    ("PROBLEM STATEMENT ID", "CIS-105", "PS CATEGORY", "Software (Cybersecurity)"),
    ("TECHNICAL DOMAIN", "D11 — Steganography & Digital Forensics", "TEAM ID / CLASS", "T.Y. B.Tech Div A (Roll No. A-15)"),
    ("PRESENTER (STUDENT)", "Sanjivani Rameshwar More (PRN: 2124UCSM1115)", "PROJECT GUIDE & HOD", "Dr. Chetan D. Bawankar"),
    ("INSTITUTION", "Department of Cyber Security, SET, Sanjivani University, Kopargaon", "COURSE", "Cryptography & Info Security (24UCYPC301)"),
    ("PROBLEM STATEMENT TITLE", "Robust Digital Watermarking for Protection of Electronic Course Content", "PILOT JURISDICTION", "Sanjivani University Campus")
]

table_shape = slide1.shapes.add_table(5, 4, Inches(0.8), Inches(3.0), Inches(7.5), Inches(3.7))
t_grid = table_shape.table
t_grid.columns[0].width = Inches(2.2)
t_grid.columns[1].width = Inches(2.0)
t_grid.columns[2].width = Inches(1.5)
t_grid.columns[3].width = Inches(1.8)

for r_idx, (k1, v1, k2, v2) in enumerate(grid_data):
    # Left pair
    c0 = t_grid.cell(r_idx, 0)
    c0.fill.solid()
    c0.fill.fore_color.rgb = RGBColor(248, 250, 252)
    p0 = c0.text_frame.paragraphs[0]
    p0.text = k1
    p0.font.name = "Arial"
    p0.font.size = Pt(8.5)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_ORANGE

    c1 = t_grid.cell(r_idx, 1)
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_WHITE
    p1 = c1.text_frame.paragraphs[0]
    p1.text = v1
    p1.font.name = "Arial"
    p1.font.size = Pt(8.5)
    p1.font.color.rgb = DARK_NAVY

    # Right pair
    c2 = t_grid.cell(r_idx, 2)
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(248, 250, 252)
    p2 = c2.text_frame.paragraphs[0]
    p2.text = k2
    p2.font.name = "Arial"
    p2.font.size = Pt(8.5)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_ORANGE

    c3 = t_grid.cell(r_idx, 3)
    c3.fill.solid()
    c3.fill.fore_color.rgb = BG_WHITE
    p3 = c3.text_frame.paragraphs[0]
    p3.text = v2
    p3.font.name = "Arial"
    p3.font.size = Pt(8.5)
    p3.font.color.rgb = DARK_NAVY

# Right Column on Slide 1: Security Graphic & Verified Demo QR
slide1.shapes.add_picture("scripts/report_generator/assets/sih/security_illustration.png", Inches(8.8), Inches(1.0), Inches(3.8), Inches(3.8))

# QR Card
qr_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(4.9), Inches(3.0), Inches(1.8))
qr_card.fill.solid()
qr_card.fill.fore_color.rgb = CARD_BG
qr_card.line.color.rgb = ACCENT_ORANGE
qr_card.line.width = Pt(1.5)

slide1.shapes.add_picture("scripts/report_generator/assets/sih/demo_qr.png", Inches(9.35), Inches(5.05), Inches(1.5), Inches(1.5))

tb_qr = slide1.shapes.add_textbox(Inches(10.9), Inches(5.15), Inches(1.2), Inches(1.3))
tf_qr = tb_qr.text_frame
tf_qr.word_wrap = True
p_q1 = tf_qr.paragraphs[0]
p_q1.text = "SCAN FOR REPO"
p_q1.font.name = "Arial"
p_q1.font.size = Pt(9)
p_q1.font.bold = True
p_q1.font.color.rgb = ACCENT_ORANGE

p_q2 = tf_qr.add_paragraph()
p_q2.text = "AquaMark Source Code\n& Verified Tests"
p_q2.font.size = Pt(8)
p_q2.font.color.rgb = TEXT_MUTED
p_q2.space_before = Pt(4)

add_sih_footer(slide1, 1)

slides_notes[1] = {
    "summary": "Project Cover introducing student credentials, guide, university, and problem statement CIS-105.",
    "script": "Respected guide Dr. Chetan Bawankar sir, teacher Mr. Kunal Makar sir, and dear classmates. My name is Sanjivani Rameshwar More from Third Year Cyber Security. Today I am presenting our project: AquaMark — Secure Digital Watermarking and Document Integrity Platform, for Problem Statement CIS-105 under the domain of Steganography, Watermarking, and Digital Forensics.",
    "viva_q": "What is the primary problem statement of CIS-105?",
    "viva_a": "To protect digital educational course materials such as PDF notes from unauthorized redistribution and detect if any circulating copy has been tampered with."
}

# ==============================================================================
# SLIDE 2 — PROJECT OVERVIEW (Matches Page 2 of Reference)
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
add_sih_header(slide2, "Proposed Solution & Project Overview")

# 5 Feature Cards on Left
card_w = Inches(7.6)
card_h = Inches(0.92)
gap = Inches(0.12)
top_s = Inches(1.4)

c2_features = [
    ("1", "PDF Watermarking", "Applies diagonal semi-transparent recipient PRN and institutional stamps across all pages.", "Implemented"),
    ("2", "Document Traceability", "Forensically binds recipient identity so leaked materials trace directly back to the downloader.", "Implemented"),
    ("3", "File Integrity Check", "Computes unique SHA-256 fingerprints to detect any unauthorized 1-byte alteration.", "Implemented"),
    ("4", "Secure User Access", "Enforces role-based access for faculty and students using salted bcrypt and JWT tokens.", "Implemented"),
    ("5", "Document Management", "Relational SQLite database organizes course documents, watermarks, and verification logs.", "Implemented")
]

for idx, (num, title, desc, tag) in enumerate(c2_features):
    c_y = top_s + idx * (card_h + gap)
    add_feature_card(slide2, Inches(0.8), c_y, card_w, card_h, num, title, desc, tag)

# Prominent Dark Navy Panel on Right (Matches SIH Style)
navy_panel = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.4), Inches(3.933), Inches(5.15))
navy_panel.fill.solid()
navy_panel.fill.fore_color.rgb = DARK_NAVY
navy_panel.line.color.rgb = DARK_NAVY

# Content inside Navy Panel
tb_np = slide2.shapes.add_textbox(Inches(8.8), Inches(1.6), Inches(3.533), Inches(4.7))
tf_np = tb_np.text_frame
tf_np.word_wrap = True

p_np_t = tf_np.paragraphs[0]
p_np_t.text = "CORE SECURITY WORKFLOW"
p_np_t.font.name = "Arial"
p_np_t.font.size = Pt(13)
p_np_t.font.bold = True
p_np_t.font.color.rgb = ACCENT_ORANGE
p_np_t.alignment = PP_ALIGN.CENTER

# 3-step visual pills inside navy panel
steps_pills = [
    ("1. UPLOAD PDF", "Faculty uploads course materials in standard PDF format. System verifies vector layout and pages."),
    ("2. PROTECT & STAMP", "Engine applies diagonal visible PRN watermark and computes unique SHA-256 hash."),
    ("3. VERIFY & AUDIT", "Upload any circulating copy to instantly confirm authenticity and detect any file tampering.")
]

for s_title, s_desc in steps_pills:
    p_st = tf_np.add_paragraph()
    p_st.text = f"▶  {s_title}"
    p_st.font.name = "Arial"
    p_st.font.size = Pt(11)
    p_st.font.bold = True
    p_st.font.color.rgb = RGBColor(255, 255, 255)
    p_st.space_before = Pt(14)

    p_sd = tf_np.add_paragraph()
    p_sd.text = s_desc
    p_sd.font.name = "Arial"
    p_sd.font.size = Pt(9.5)
    p_sd.font.color.rgb = RGBColor(203, 213, 225)
    p_sd.space_before = Pt(2)

# Small highlight at bottom of navy panel
p_hl = tf_np.add_paragraph()
p_hl.text = "Sub-1.2s Processing  •  Zero Distortion  •  100% Tamper Catch"
p_hl.font.name = "Arial"
p_hl.font.size = Pt(9)
p_hl.font.bold = True
p_hl.font.color.rgb = RGBColor(56, 189, 248)
p_hl.alignment = PP_ALIGN.CENTER
p_hl.space_before = Pt(20)

add_sih_footer(slide2, 2)

slides_notes[2] = {
    "summary": "Project Overview matching SIH slide 2: five feature cards on the left and a prominent dark navy workflow panel on the right.",
    "script": "Sir, this slide presents the core overview of AquaMark. On the left, you can see our five main capabilities: PDF Watermarking, Document Traceability, File Integrity Checking, Secure Access Control, and Document Management. On the right is our three-step workflow: Upload, Protect, and Verify. Everything is fully functional and operates in under 1.2 seconds.",
    "viva_q": "How does AquaMark achieve traceability?",
    "viva_a": "By dynamically embedding the recipient's student PRN and timestamp directly into the document structure upon generation."
}

# ==============================================================================
# SLIDE 3 — TECHNICAL APPROACH (Matches Page 3 of Reference)
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
add_sih_header(slide3, "Technical Approach & Architecture")

# 5 Component Cards on Left
tech_cards = [
    ("A", "Frontend Interface", "React 18 + TypeScript + Vite + Tailwind CSS\nResponsive UI, client-side validation, live preview", "Client Tier"),
    ("B", "Backend Controller", "Python 3.12 + FastAPI + Uvicorn ASGI\nAsync REST APIs, JWT token security, role access", "API Tier"),
    ("C", "PDF Processing Engine", "PyMuPDF (fitz) + SciPy Frequency Library\nVector layout parsing, 45° visible stamp, 2D-DCT", "Processing"),
    ("D", "Cryptographic Core", "hashlib (SHA-256) + hmac + passlib (bcrypt)\nUnique 256-bit fingerprinting, tamper manifests", "Security"),
    ("E", "Data & Vault Storage", "SQLite Relational DB + Isolated Server Vault\nMaintains user, watermark, and audit records", "Persistence")
]

for idx, (icon_c, title, desc, tag) in enumerate(tech_cards):
    c_y = top_s + idx * (card_h + gap)
    add_feature_card(slide3, Inches(0.8), c_y, card_w, card_h, icon_c, title, desc, tag)

# Architecture Diagram Image on Right (Matches SIH Right Diagram Box)
slide3.shapes.add_picture("scripts/report_generator/assets/system_architecture.png", Inches(8.6), Inches(1.4), Inches(3.933), Inches(3.6))

# Bottom Two Panels on Slide 3 (Matches SIH Live Prototype & Source Code Box)
b_panel_left = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(5.15), Inches(1.9), Inches(1.4))
b_panel_left.fill.solid()
b_panel_left.fill.fore_color.rgb = CARD_BG
b_panel_left.line.color.rgb = ACCENT_ORANGE
b_panel_left.line.width = Pt(1.5)
tf_bpl = b_panel_left.text_frame
tf_bpl.word_wrap = True
p_bpl0 = tf_bpl.paragraphs[0]
p_bpl0.text = "LIVE BACKEND"
p_bpl0.font.name = "Arial"
p_bpl0.font.size = Pt(9.5)
p_bpl0.font.bold = True
p_bpl0.font.color.rgb = ACCENT_ORANGE
p_bpl1 = tf_bpl.add_paragraph()
p_bpl1.text = "FastAPI Swagger\nhttp://localhost:8000\nActive on Campus"
p_bpl1.font.size = Pt(8.5)
p_bpl1.font.color.rgb = TEXT_DARK
p_bpl1.space_before = Pt(4)

b_panel_right = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.633), Inches(5.15), Inches(1.9), Inches(1.4))
b_panel_right.fill.solid()
b_panel_right.fill.fore_color.rgb = CARD_BG
b_panel_right.line.color.rgb = ACCENT_BLUE
b_panel_right.line.width = Pt(1.5)
tf_bpr = b_panel_right.text_frame
tf_bpr.word_wrap = True
p_bpr0 = tf_bpr.paragraphs[0]
p_bpr0.text = "SOURCE CODE"
p_bpr0.font.name = "Arial"
p_bpr0.font.size = Pt(9.5)
p_bpr0.font.bold = True
p_bpr0.font.color.rgb = ACCENT_BLUE
p_bpr1 = tf_bpr.add_paragraph()
p_bpr1.text = "GitHub Repository\nsanjivani-more /\nAquaMark-Course"
p_bpr1.font.size = Pt(8.5)
p_bpr1.font.color.rgb = TEXT_DARK
p_bpr1.space_before = Pt(4)

add_sih_footer(slide3, 3)

slides_notes[3] = {
    "summary": "Technical Approach slide matching SIH layout: five technology cards on the left, architecture diagram on the right, and live demo/repo boxes at the bottom.",
    "script": "Sir, this slide details our technical implementation. On the left are the real libraries used: React and Tailwind for frontend, FastAPI and Python for backend, PyMuPDF for vector PDF manipulation, and hashlib for SHA-256 integrity. On the right is our system architecture diagram showing how data flows cleanly from the user to the storage vault. Below are our live Swagger API endpoint and GitHub repository.",
    "viva_q": "Why is PyMuPDF preferred over PyPDF2 or ReportLab for this task?",
    "viva_a": "PyMuPDF uses the high-performance MuPDF rendering engine, allowing fast vector parsing and modification without breaking complex PDF layouts or font tables."
}

# ==============================================================================
# SLIDE 4 — FEASIBILITY AND VIABILITY (Matches Page 4 of Reference)
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
add_sih_header(slide4, "Feasibility and Viability Analysis")

# Large Dark Navy Feature Panel on Left (Matches SIH Left Hero Box)
navy_hero = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(4.5), Inches(5.15))
navy_hero.fill.solid()
navy_hero.fill.fore_color.rgb = DARK_NAVY
navy_hero.line.color.rgb = DARK_NAVY

# Illustration inside Left Navy Panel
slide4.shapes.add_picture("scripts/report_generator/assets/sih/shield_icon.png", Inches(1.85), Inches(1.7), Inches(2.4), Inches(2.4))

tb_nh = slide4.shapes.add_textbox(Inches(1.0), Inches(4.3), Inches(4.1), Inches(2.0))
tf_nh = tb_nh.text_frame
tf_nh.word_wrap = True
p_nh0 = tf_nh.paragraphs[0]
p_nh0.text = "ACADEMIC SECURITY GUARANTEE"
p_nh0.font.name = "Arial"
p_nh0.font.size = Pt(13)
p_nh0.font.bold = True
p_nh0.font.color.rgb = ACCENT_ORANGE
p_nh0.alignment = PP_ALIGN.CENTER

p_nh1 = tf_nh.add_paragraph()
p_nh1.text = "SUB-SECOND EXECUTION  •  ZERO LICENSING COST\nEvery document receives an immutable 256-bit SHA-256 digital fingerprint and recipient watermark record."
p_nh1.font.name = "Arial"
p_nh1.font.size = Pt(10)
p_nh1.font.color.rgb = RGBColor(226, 232, 240)
p_nh1.alignment = PP_ALIGN.CENTER
p_nh1.space_before = Pt(6)

p_nh2 = tf_nh.add_paragraph()
p_nh2.text = "Standard PDF compatibility: Works on all phones, tablets, and PCs without proprietary apps."
p_nh2.font.name = "Arial"
p_nh2.font.size = Pt(9)
p_nh2.font.color.rgb = RGBColor(147, 197, 253)
p_nh2.alignment = PP_ALIGN.CENTER
p_nh2.space_before = Pt(8)

# Four Feature Cards on Right (2x2 Grid)
right_cards = [
    ("1", "Technical Feasibility", "Built entirely using industry-proven, stable technologies (Python, FastAPI, React, PyMuPDF). Highly maintainable and lightweight.", ACCENT_ORANGE),
    ("2", "Low Cost & Open Source", "Zero proprietary software licensing fees. Built on open-source libraries, drastically reducing institutional operational overhead.", ACCENT_BLUE),
    ("3", "Practical Campus Adoption", "Designed specifically for college workflows. Teachers require no training; simple upload-and-stamp workflow handles entire batches.", ACCENT_GREEN),
    ("4", "Layered Security Model", "Visible deterrence prevents casual forwarding, while cryptographic SHA-256 hashing instantly exposes byte-level file modifications.", ACCENT_ORANGE)
]

rc_w = Inches(3.45)
rc_h = Inches(2.45)
rc_gap_x = Inches(0.25)
rc_gap_y = Inches(0.25)
rc_start_x = Inches(5.6)
rc_start_y = Inches(1.4)

for idx, (ic_num, rc_title, rc_desc, rc_clr) in enumerate(right_cards):
    r_row = idx // 2
    r_col = idx % 2
    x_pos = rc_start_x + r_col * (rc_w + rc_gap_x)
    y_pos = rc_start_y + r_row * (rc_h + rc_gap_y)

    rc_card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, y_pos, rc_w, rc_h)
    rc_card.fill.solid()
    rc_card.fill.fore_color.rgb = CARD_BG
    rc_card.line.color.rgb = CARD_BORDER
    rc_card.line.width = Pt(1.5)

    # Accent top strip
    strip = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, y_pos, rc_w, Inches(0.08))
    strip.fill.solid()
    strip.fill.fore_color.rgb = rc_clr
    strip.line.color.rgb = rc_clr

    tb_rc = slide4.shapes.add_textbox(x_pos + Inches(0.18), y_pos + Inches(0.18), rc_w - Inches(0.36), rc_h - Inches(0.36))
    tf_rc = tb_rc.text_frame
    tf_rc.word_wrap = True

    p_rt = tf_rc.paragraphs[0]
    p_rt.text = rc_title
    p_rt.font.name = "Arial"
    p_rt.font.size = Pt(13)
    p_rt.font.bold = True
    p_rt.font.color.rgb = DARK_NAVY
    p_rt.space_after = Pt(6)

    p_rd = tf_rc.add_paragraph()
    p_rd.text = rc_desc
    p_rd.font.name = "Arial"
    p_rd.font.size = Pt(10)
    p_rd.font.color.rgb = TEXT_DARK
    p_rd.space_before = Pt(4)

add_sih_footer(slide4, 4)

slides_notes[4] = {
    "summary": "Feasibility & Viability slide matching SIH layout: large navy panel on left and four feature cards on right covering technical, financial, practical, and security viability.",
    "script": "Sir, this slide addresses the feasibility and viability of AquaMark. Technically, it is built on reliable open-source frameworks. Financially, it incurs zero software licensing costs because Python, FastAPI, and React are free. Practically, it integrates easily into university departments without requiring any special hardware. And from a security perspective, it provides defense-in-depth through watermarking and hashing.",
    "viva_q": "Does running AquaMark require expensive server infrastructure?",
    "viva_a": "No, sir. Because of FastAPI's lightweight asynchronous design, AquaMark runs comfortably on existing college department servers or affordable cloud tiers."
}

# ==============================================================================
# SLIDE 5 — IMPACT AND BENEFITS (Matches Page 5 of Reference)
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
add_sih_header(slide5, "Impact and Institutional Benefits")

# 5 Equal Vertical Cards Across the Slide (Matches SIH Style)
benefits = [
    ("Source Identification", "Visible watermark displaying student PRN immediately reveals the original source of any leaked copy.", ACCENT_ORANGE),
    ("Integrity Checking", "SHA-256 cryptographic hashing detects unauthorized modifications to deadlines, grades, or exam questions.", ACCENT_BLUE),
    ("Document Traceability", "Forensic database records maintain a clear timeline of when files were generated, issued, and verified.", ACCENT_GREEN),
    ("Organized Workflow", "Replaces disorganized file sharing with a unified web dashboard for uploading, protecting, and tracking notes.", ACCENT_ORANGE),
    ("Educational Security", "Protects faculty intellectual property while ensuring students receive authentic, untampered study materials.", ACCENT_BLUE)
]

v_card_w = Inches(2.15)
v_gap = Inches(0.24)
v_start_x = Inches(0.8)

for idx, (b_title, b_desc, b_clr) in enumerate(benefits):
    b_x = v_start_x + idx * (v_card_w + v_gap)
    b_card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b_x, Inches(1.5), v_card_w, Inches(4.3))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = CARD_BG
    b_card.line.color.rgb = CARD_BORDER
    b_card.line.width = Pt(1.5)

    # Top accent header
    b_hdr = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b_x, Inches(1.5), v_card_w, Inches(0.45))
    b_hdr.fill.solid()
    b_hdr.fill.fore_color.rgb = b_clr
    b_hdr.line.color.rgb = b_clr
    tf_bh = b_hdr.text_frame
    p_bh = tf_bh.paragraphs[0]
    p_bh.text = f"BENEFIT 0{idx+1}"
    p_bh.font.name = "Arial"
    p_bh.font.size = Pt(10)
    p_bh.font.bold = True
    p_bh.font.color.rgb = RGBColor(255, 255, 255)
    p_bh.alignment = PP_ALIGN.CENTER

    # Content
    tb_b = slide5.shapes.add_textbox(b_x + Inches(0.12), Inches(2.1), v_card_w - Inches(0.24), Inches(3.5))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    p_bt = tf_b.paragraphs[0]
    p_bt.text = b_title
    p_bt.font.name = "Arial"
    p_bt.font.size = Pt(13)
    p_bt.font.bold = True
    p_bt.font.color.rgb = DARK_NAVY
    p_bt.space_after = Pt(8)

    p_bd = tf_b.add_paragraph()
    p_bd.text = b_desc
    p_bd.font.name = "Arial"
    p_bd.font.size = Pt(10)
    p_bd.font.color.rgb = TEXT_DARK

# Bottom Dark Navy Banner (Matches SIH Style Exact Text)
bottom_banner = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.75))
bottom_banner.fill.solid()
bottom_banner.fill.fore_color.rgb = DARK_NAVY
bottom_banner.line.color.rgb = DARK_NAVY
tf_bb = bottom_banner.text_frame
p_bb = tf_bb.paragraphs[0]
p_bb.text = "“Supporting safer sharing and better traceability of educational documents.”"
p_bb.font.name = "Arial"
p_bb.font.size = Pt(13)
p_bb.font.bold = True
p_bb.font.color.rgb = RGBColor(255, 255, 255)
p_bb.alignment = PP_ALIGN.CENTER

add_sih_footer(slide5, 5)

slides_notes[5] = {
    "summary": "Impact and Benefits slide matching SIH layout: five equal vertical cards and a prominent dark navy banner across the bottom.",
    "script": "Sir, this slide outlines the positive impact AquaMark creates across an educational institution. The five key benefits are Source Identification, Integrity Checking, Document Traceability, an Organized Workflow, and Enhanced Educational Security. As stated in our banner: AquaMark supports safer sharing and better traceability of educational documents without restricting student learning.",
    "viva_q": "Does AquaMark claim to stop 100% of all copying?",
    "viva_a": "No, sir. We are honest that watermarking does not stop a student from re-typing words or taking a photo. What it provides is indisputable source identification and cryptographic proof of tampering."
}

# ==============================================================================
# SLIDE 6 — RESEARCH AND REFERENCES (Matches Page 6 of Reference)
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
add_sih_header(slide6, "Research and Technical References")

# 6 Reference Cards in a 2-Column x 3-Row Layout (Matches SIH Style)
refs_data = [
    ("1", "Digital Watermarking Fundamentals", "I. J. Cox, M. L. Miller, J. A. Bloom, J. Fridrich, and T. Kalker", "Digital Watermarking and Steganography, 2nd ed. Morgan Kaufmann", "2008", "https://doi.org/10.1016/B978-0-12-372585-1.X5001-3"),
    ("2", "PDF Architecture & Vector Standards", "Adobe Systems Incorporated / International Organization for Standardization", "ISO 32000-1:2008 — Document Management: Portable Document Format", "2008", "https://www.iso.org/standard/51502.html"),
    ("3", "Cryptographic Security & Hashing", "William Stallings", "Cryptography and Network Security: Principles and Practice, 8th ed. Pearson", "2020", "https://www.pearson.com/en-us/subject-catalog/p/cryptography-and-network-security"),
    ("4", "Discrete Cosine Transform (2D-DCT)", "N. Ahmed, T. Natarajan, and K. R. Rao", "IEEE Transactions on Computers, vol. C-23, no. 1, pp. 90-93", "1974", "https://doi.org/10.1109/T-C.1974.223784"),
    ("5", "Frequency-Domain Watermark Robustness", "C.-T. Hsu and J.-L. Wu", "IEEE Transactions on Image Processing, vol. 8, no. 1, pp. 58-68", "1999", "https://doi.org/10.1109/83.736686"),
    ("6", "Secure Hash Standard (SHA-256)", "National Institute of Standards and Technology (NIST)", "Federal Information Processing Standards Publication (FIPS PUB 180-4)", "2015", "https://doi.org/10.6028/NIST.FIPS.180-4")
]

ref_w = Inches(5.7)
ref_h = Inches(1.55)
ref_start_x = Inches(0.8)
ref_start_y = Inches(1.45)
ref_gap_x = Inches(0.333)
ref_gap_y = Inches(0.2)

for idx, (ref_num, ref_topic, ref_authors, ref_source, ref_year, ref_link) in enumerate(refs_data):
    col = idx % 2
    row = idx // 2
    r_x = ref_start_x + col * (ref_w + ref_gap_x)
    r_y = ref_start_y + row * (ref_h + ref_gap_y)

    r_card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, r_x, r_y, ref_w, ref_h)
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = CARD_BG
    r_card.line.color.rgb = CARD_BORDER
    r_card.line.width = Pt(1.5)

    # Number badge on left
    n_badge = slide6.shapes.add_shape(MSO_SHAPE.OVAL, r_x + Inches(0.15), r_y + Inches(0.18), Inches(0.42), Inches(0.42))
    n_badge.fill.solid()
    n_badge.fill.fore_color.rgb = DARK_NAVY
    n_badge.line.color.rgb = DARK_NAVY
    tf_nb = n_badge.text_frame
    p_nb = tf_nb.paragraphs[0]
    p_nb.text = ref_num
    p_nb.font.name = "Arial"
    p_nb.font.size = Pt(12)
    p_nb.font.bold = True
    p_nb.font.color.rgb = RGBColor(255, 255, 255)
    p_nb.alignment = PP_ALIGN.CENTER

    # Content
    tb_r = slide6.shapes.add_textbox(r_x + Inches(0.68), r_y + Inches(0.1), ref_w - Inches(0.78), ref_h - Inches(0.18))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_rt = tf_r.paragraphs[0]
    p_rt.text = f"{ref_topic}  ({ref_year})"
    p_rt.font.name = "Arial"
    p_rt.font.size = Pt(11)
    p_rt.font.bold = True
    p_rt.font.color.rgb = DARK_NAVY

    p_ra = tf_r.add_paragraph()
    p_ra.text = f"Authors: {ref_authors}"
    p_ra.font.name = "Arial"
    p_ra.font.size = Pt(8.5)
    p_ra.font.color.rgb = TEXT_DARK
    p_ra.space_before = Pt(2)

    p_rs = tf_r.add_paragraph()
    p_rs.text = f"Source: {ref_source}"
    p_rs.font.name = "Arial"
    p_rs.font.size = Pt(8.5)
    p_rs.font.italic = True
    p_rs.font.color.rgb = TEXT_MUTED
    p_rs.space_before = Pt(1)

    p_rl = tf_r.add_paragraph()
    p_rl.text = ref_link
    p_rl.font.name = "Arial"
    p_rl.font.size = Pt(8)
    p_rl.font.color.rgb = ACCENT_BLUE
    p_rl.space_before = Pt(2)

add_sih_footer(slide6, 6)

slides_notes[6] = {
    "summary": "Research and References slide matching SIH layout: six academic cards in 2 columns and 3 rows with real IEEE sources.",
    "script": "Finally, this slide cites our core academic and technical references. We based our watermarking principles on Cox and Hsu's foundational papers, our PDF manipulation on ISO 32000-1 standards, our cryptographic hashing on NIST FIPS 180-4, and our frequency domain analysis on Ahmed's original Discrete Cosine Transform paper. Thank you very much, sir. I am now open to your questions.",
    "viva_q": "Why is NIST FIPS 180-4 relevant to your project?",
    "viva_a": "FIPS 180-4 is the official Federal Information Processing Standard defining Secure Hash Algorithms, including SHA-256, which guarantees our cryptographic integrity implementation follows global cryptographic standards."
}

# Attach speaker notes to PPTX slides
for idx, slide in enumerate(prs.slides):
    slide_num = idx + 1
    if slide_num in slides_notes:
        note_text = (
            f"SLIDE {slide_num} SUMMARY:\n{slides_notes[slide_num]['summary']}\n\n"
            f"SPEAKING SCRIPT (30-45s):\n\"{slides_notes[slide_num]['script']}\"\n\n"
            f"POSSIBLE VIVA QUESTION & ANSWER:\n"
            f"Q: {slides_notes[slide_num]['viva_q']}\n"
            f"A: {slides_notes[slide_num]['viva_a']}"
        )
        slide.notes_slide.notes_text_frame.text = note_text

pptx_out = "/Users/omsaishdhokchaule/Downloads/AquaMark_SIH_Style_Presentation.pptx"
prs.save(pptx_out)
print(f"SIH-Style PPTX saved successfully at: {pptx_out}")

# Also copy to workspace
os.system(f"cp '{pptx_out}' /Users/omsaishdhokchaule/Downloads/AquaMark/AquaMark_SIH_Style_Presentation.pptx")
