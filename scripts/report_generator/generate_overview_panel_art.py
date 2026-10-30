import os
from PIL import Image, ImageDraw, ImageFont

w, h = 420, 500
img = Image.new('RGB', (w, h), color='#0F2A4A')
draw = ImageDraw.Draw(img)

font_large = None
font_mid = None
font_small = None

font_candidates = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf"
]
for fc in font_candidates:
    if os.path.exists(fc):
        try:
            font_large = ImageFont.truetype(fc, 32)
            font_mid = ImageFont.truetype(fc, 18)
            font_small = ImageFont.truetype(fc, 14)
            break
        except Exception:
            pass

if not font_large:
    font_large = ImageFont.load_default()
    font_mid = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Header
draw.text((210, 40), "DOCUMENT TRUST WORKFLOW", fill='#38BDF8', font=font_small, anchor='mm')
draw.text((210, 75), "Upload • Protect • Verify", fill='#FFFFFF', font=font_large, anchor='mm')
draw.line([60, 95, 360, 95], fill='#EA580C', width=3)

# 3 Flow Cards
steps = [
    ("1. UPLOAD", "Original Course Materials", "Faculty uploads lecture notes, assignments, or lab manuals in PDF format.", "#0284C7"),
    ("2. PROTECT", "Dual-Layer Watermarking", "Applies diagonal PRN stamp & 2D-DCT frequency watermark + SHA-256 hash.", "#EA580C"),
    ("3. VERIFY", "Instant Integrity Audit", "Re-upload circulating copies to detect single-byte edits and trace sources.", "#22C55E")
]

cur_y = 120
for step, sub, desc, border_c in steps:
    draw.rounded_rectangle([30, cur_y, 390, cur_y + 95], radius=10, fill='#0B1F36', outline=border_c, width=2)
    # Step header
    draw.text((45, cur_y + 15), step, fill=border_c, font=font_small)
    draw.text((130, cur_y + 15), sub, fill='#FFFFFF', font=font_small)
    # Desc
    words = desc.split()
    l1 = " ".join(words[:6])
    l2 = " ".join(words[6:12])
    l3 = " ".join(words[12:])
    draw.text((45, cur_y + 38), l1, fill='#94A3B8', font=font_small)
    draw.text((45, cur_y + 56), l2, fill='#94A3B8', font=font_small)
    if l3:
        draw.text((45, cur_y + 74), l3, fill='#94A3B8', font=font_small)
    cur_y += 112

draw.rounded_rectangle([30, 455, 390, 485], radius=6, fill='#EA580C')
draw.text((210, 470), "LIVE DEMO → http://localhost:8000/docs", fill='#FFFFFF', font=font_small, anchor='mm')

out_path = "scripts/report_generator/assets/sih/sih_overview_art.png"
img.save(out_path, "PNG", quality=95)
print(f"Generated SIH overview panel art at: {out_path}")
