import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("scripts/report_generator/assets/ui", exist_ok=True)

font_regular = None
font_bold = None
font_title = None

font_candidates = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/Library/Fonts/Arial.ttf"
]
for fc in font_candidates:
    if os.path.exists(fc):
        try:
            font_title = ImageFont.truetype(fc, 32)
            font_bold = ImageFont.truetype(fc, 22)
            font_regular = ImageFont.truetype(fc, 18)
            font_small = ImageFont.truetype(fc, 14)
            break
        except Exception:
            pass

if not font_title:
    font_title = ImageFont.load_default()
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_small = ImageFont.load_default()

def create_browser_window(w, h, title, active_tab="Dashboard"):
    img = Image.new('RGB', (w, h), color='#F8FAFC')
    draw = ImageDraw.Draw(img)
    
    # Browser chrome bar
    draw.rectangle([0, 0, w, 50], fill='#0F2A4A')
    # Window buttons
    draw.ellipse([16, 18, 28, 30], fill='#EF4444')
    draw.ellipse([36, 18, 48, 30], fill='#F59E0B')
    draw.ellipse([56, 18, 68, 30], fill='#10B981')
    
    # URL bar
    draw.rounded_rectangle([100, 10, w - 220, 40], radius=6, fill='#1E3A8A')
    draw.text((120, 16), f"https://aquamark.sanjivani.edu.in/{title.lower().replace(' ', '-')}", fill='#93C5FD', font=font_small)
    
    # User status on right
    draw.text((w - 200, 16), "👤 Prof. Bawankar (SET)", fill='#E2E8F0', font=font_small)
    
    # Navigation subheader
    draw.rectangle([0, 50, w, 100], fill='#FFFFFF', outline='#E2E8F0', width=1)
    draw.text((30, 62), "AquaMark", fill='#0F2A4A', font=font_bold)
    draw.text((150, 66), "Document Security & Watermarking Platform", fill='#64748B', font=font_small)
    
    tabs = ["Dashboard", "Documents & Watermarking", "Verify Document", "Cryptography Lab", "Audit Trail"]
    tab_x = 480
    for t in tabs:
        is_active = (t == active_tab)
        t_color = '#0284C7' if is_active else '#475569'
        draw.text((tab_x, 66), t, fill=t_color, font=font_regular)
        if is_active:
            draw.line([tab_x, 97, tab_x + len(t)*10 + 10, 97], fill='#0284C7', width=3)
        tab_x += len(t)*11 + 25
        
    return img, draw

# 1. Dashboard View
img_dash, draw_dash = create_browser_window(1200, 700, "Dashboard", "Dashboard")
# Stats cards
def draw_stat_card(draw, x, y, title, val, sub, color):
    draw.rounded_rectangle([x, y, x + 260, y + 120], radius=10, fill='#FFFFFF', outline='#E2E8F0', width=2)
    draw.rectangle([x, y, x + 8, y + 120], fill=color)
    draw.text((x + 24, y + 20), title, fill='#64748B', font=font_small)
    draw.text((x + 24, y + 42), val, fill='#0F2A4A', font=font_title)
    draw.text((x + 24, y + 85), sub, fill='#10B981', font=font_small)

draw_stat_card(draw_dash, 50, 130, "PROTECTED DOCUMENTS", "148", "✓ 100% Verified in DB", "#0284C7")
draw_stat_card(draw_dash, 335, 130, "WATERMARKED COPIES", "1,240", "✓ 0 Visual Artifacts", "#059669")
draw_stat_card(draw_dash, 620, 130, "VERIFICATION QUERIES", "412", "✓ 409 Valid, 3 Tampered", "#D97706")
draw_stat_card(draw_dash, 905, 130, "ACTIVE FACULTY USERS", "18", "✓ Role-Based Access", "#7C3AED")

# Recent documents table
draw_dash.rounded_rectangle([50, 280, 1150, 660], radius=10, fill='#FFFFFF', outline='#E2E8F0', width=2)
draw_dash.text((80, 305), "Recent Course Documents & Watermarking Activity", fill='#0F2A4A', font=font_bold)
draw_dash.line([50, 345, 1150, 345], fill='#E2E8F0', width=1)

table_headers = ["Document Title", "Course Code", "Pages", "Visible Stamp", "SHA-256 Digest", "Status"]
col_x = [80, 420, 560, 660, 810, 1030]
for i, h in enumerate(table_headers):
    draw_dash.text((col_x[i], 360), h, fill='#64748B', font=font_small)

rows = [
    ("ICS_Unit_3_Cryptography_Notes.pdf", "CIS-105", "42 pgs", "PRN: 2124UCSM1115", "e3b0c44298fc...", "Active / Protected"),
    ("Cyber_Forensics_Lab_Manual_v2.pdf", "CIS-105", "18 pgs", "PRN: 2124UCSM1115", "8f4e2b0179a3...", "Active / Protected"),
    ("Mid_Term_Question_Bank_Solutions.pdf", "24UCYPC301", "24 pgs", "PRN: 2124UCSM1115", "d41d8cd98f00...", "Active / Protected"),
    ("Network_Security_Project_Guidelines.pdf", "CIS-102", "12 pgs", "Confidential / Faculty", "a58b29140fa7...", "Active / Protected"),
    ("Cloud_Security_Assignment_3.pdf", "CIS-108", "06 pgs", "PRN: 2124UCSM1115", "7c9f112e458b...", "Active / Protected")
]

row_y = 405
for r in rows:
    draw_dash.line([50, row_y - 10, 1150, row_y - 10], fill='#F1F5F9', width=1)
    draw_dash.text((col_x[0], row_y), r[0], fill='#0F2A4A', font=font_regular)
    draw_dash.text((col_x[1], row_y), r[1], fill='#475569', font=font_small)
    draw_dash.text((col_x[2], row_y), r[2], fill='#475569', font=font_small)
    draw_dash.text((col_x[3], row_y), r[3], fill='#0284C7', font=font_small)
    draw_dash.text((col_x[4], row_y), r[4], fill='#64748B', font=font_small)
    # Green status pill
    draw_dash.rounded_rectangle([col_x[5] - 6, row_y - 4, col_x[5] + 105, row_y + 20], radius=12, fill='#DCFCE7')
    draw_dash.text((col_x[5], row_y), "✓ Verified", fill='#166534', font=font_small)
    row_y += 48

img_dash.save("scripts/report_generator/assets/ui/ui_dashboard.png", "PNG", quality=95)

# 2. Upload & Watermarking View
img_wm, draw_wm = create_browser_window(1200, 700, "Documents", "Documents & Watermarking")
# Left: Upload Form
draw_wm.rounded_rectangle([50, 130, 580, 660], radius=10, fill='#FFFFFF', outline='#E2E8F0', width=2)
draw_wm.text((80, 155), "1. Upload & Configure Course PDF", fill='#0F2A4A', font=font_bold)
draw_wm.line([50, 195, 580, 195], fill='#E2E8F0', width=1)

# Drop zone
draw_wm.rounded_rectangle([80, 215, 550, 320], radius=8, fill='#F8FAFC', outline='#0284C7', width=2)
draw_wm.text((230, 245), "📄 ICS_Lab_Manual_2026.pdf", fill='#0F2A4A', font=font_regular)
draw_wm.text((215, 275), "Size: 4.8 MB  •  Pages: 18  •  Ready", fill='#10B981', font=font_small)

# Inputs
draw_wm.text((80, 345), "Target Recipient PRN / Roll No:", fill='#475569', font=font_small)
draw_wm.rounded_rectangle([80, 370, 550, 410], radius=6, fill='#F8FAFC', outline='#CBD5E1', width=1)
draw_wm.text((95, 382), "2124UCSM1115 (Sanjivani More - Div A)", fill='#0F2A4A', font=font_regular)

draw_wm.text((80, 430), "Visible Stamp Text Overlay:", fill='#475569', font=font_small)
draw_wm.rounded_rectangle([80, 455, 550, 495], radius=6, fill='#F8FAFC', outline='#CBD5E1', width=1)
draw_wm.text((95, 467), "RESTRICTED COPY - SANJIVANI UNIV - PRN 2124UCSM1115", fill='#0F2A4A', font=font_regular)

draw_wm.text((80, 515), "Security Protection Layers:", fill='#475569', font=font_small)
draw_wm.text((105, 545), "☑ Apply Visible Diagonal Watermark (PyMuPDF at 45°, 35% opacity)", fill='#0F2A4A', font=font_small)
draw_wm.text((105, 570), "☑ Apply Invisible 2D-DCT Transform Watermark (Mid-Frequency)", fill='#0F2A4A', font=font_small)
draw_wm.text((105, 595), "☑ Generate Cryptographic SHA-256 Digest & HMAC Manifest", fill='#0F2A4A', font=font_small)

# Button
draw_wm.rounded_rectangle([80, 620, 550, 655], radius=6, fill='#0284C7')
draw_wm.text((235, 628), "Apply Watermark & Sign Document", fill='#FFFFFF', font=font_regular)

# Right: Live Document Preview
draw_wm.rounded_rectangle([610, 130, 1150, 660], radius=10, fill='#FFFFFF', outline='#E2E8F0', width=2)
draw_wm.text((640, 155), "2. Live Watermarked Document Preview", fill='#0F2A4A', font=font_bold)
draw_wm.line([610, 195, 1150, 195], fill='#E2E8F0', width=1)

# Document paper simulation
draw_wm.rounded_rectangle([660, 215, 1100, 640], radius=4, fill='#FFFFFF', outline='#94A3B8', width=2)
# Document dummy text lines
for y_pos in range(240, 620, 22):
    draw_wm.line([685, y_pos, 1075, y_pos], fill='#E2E8F0', width=3)

# Diagonal Red Watermark text simulation
draw_wm.text((710, 410), "RESTRICTED COPY - PRN 2124UCSM1115", fill='#FCA5A5', font=font_title)
draw_wm.text((735, 450), "SANJIVANI UNIVERSITY - 2026-10-29", fill='#FCA5A5', font=font_regular)

img_wm.save("scripts/report_generator/assets/ui/ui_watermark_process.png", "PNG", quality=95)

# 3. Verification & Integrity Result View
img_ver, draw_ver = create_browser_window(1200, 700, "Verify", "Verify Document")
# Top search box
draw_ver.rounded_rectangle([50, 130, 1150, 250], radius=10, fill='#FFFFFF', outline='#E2E8F0', width=2)
draw_ver.text((80, 155), "Document Integrity & Tamper Inspection Tool", fill='#0F2A4A', font=font_bold)
draw_ver.text((80, 185), "Upload any circulating course PDF to instantly verify its origin, recipient, and byte-level integrity.", fill='#64748B', font=font_small)

draw_ver.rounded_rectangle([80, 205, 950, 240], radius=6, fill='#F8FAFC', outline='#CBD5E1', width=1)
draw_ver.text((95, 215), "📄 Circulating_Lab_Manual_Inspection.pdf (Uploaded)", fill='#0F2A4A', font=font_regular)
draw_ver.rounded_rectangle([970, 205, 1120, 240], radius=6, fill='#0F2A4A')
draw_ver.text((1000, 215), "Verify Now", fill='#FFFFFF', font=font_regular)

# Verification Results Section (Comparison: Authentic vs Tampered)
# Card A: Valid
draw_ver.rounded_rectangle([50, 275, 580, 660], radius=10, fill='#FFFFFF', outline='#10B981', width=3)
draw_ver.rounded_rectangle([50, 275, 580, 335], radius=10, fill='#ECFDF5')
draw_ver.text((80, 295), "✓ INTEGRITY VERIFIED (Authentic Document)", fill='#065F46', font=font_bold)

items_valid = [
    ("Verification Status:", "MATCH - Untampered Original"),
    ("Calculated SHA-256:", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4..."),
    ("Registered DB Hash:", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4..."),
    ("Recipient Student:", "Sanjivani Rameshwar More (PRN: 2124UCSM1115)"),
    ("Issuing Faculty:", "Dr. Chetan D. Bawankar (HOD, Cyber Security)"),
    ("Issuing Timestamp:", "2026-10-22 14:02:18 IST"),
    ("Forensic Conclusion:", "Document matches byte-for-byte. Zero tampering.")
]
v_y = 355
for k, v in items_valid:
    draw_ver.text((80, v_y), k, fill='#475569', font=font_small)
    draw_ver.text((80, v_y + 18), v, fill='#0F2A4A', font=font_regular)
    v_y += 42

# Card B: Tampered Document Result
draw_ver.rounded_rectangle([620, 275, 1150, 660], radius=10, fill='#FFFFFF', outline='#EF4444', width=3)
draw_ver.rounded_rectangle([620, 275, 1150, 335], radius=10, fill='#FEF2F2')
draw_ver.text((650, 295), "⚠ TAMPERING DETECTED (Hash Mismatch)", fill='#991B1B', font=font_bold)

items_tampered = [
    ("Verification Status:", "FAILED - Modification Detected!"),
    ("Calculated SHA-256:", "7a91bf2804c81a29381048f029140a8271038b52..."),
    ("Original DB Hash:", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4..."),
    ("Integrity Avalanche:", "1-Byte text alteration resulted in total hash change"),
    ("Original Recipient:", "Traced to PRN 2124UCSM1115 from internal metadata"),
    ("Security Action:", "Flagged in University Audit Trail as Unauthorized Edit"),
    ("Forensic Conclusion:", "Page content was altered outside the AquaMark portal.")
]
t_y = 355
for k, v in items_tampered:
    draw_ver.text((650, t_y), k, fill='#475569', font=font_small)
    draw_ver.text((650, t_y + 18), v, fill='#B91C1C' if 'FAILED' in v or 'alteration' in v else '#0F2A4A', font=font_regular)
    t_y += 42

img_ver.save("scripts/report_generator/assets/ui/ui_verification_result.png", "PNG", quality=95)
print("Generated high-quality UI mockups based on actual codebase routes!")
