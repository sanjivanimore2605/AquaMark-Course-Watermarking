import os
from PIL import Image, ImageDraw, ImageFont

w, h = 900, 700
img = Image.new('RGB', (w, h), color='#0F2A4A')
draw = ImageDraw.Draw(img)

# Try loading standard system fonts
font_large = None
font_mid = None
font_small = None
font_tiny = None

font_candidates = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/Library/Fonts/Arial.ttf"
]
for fc in font_candidates:
    if os.path.exists(fc):
        try:
            font_large = ImageFont.truetype(fc, 34)
            font_mid = ImageFont.truetype(fc, 22)
            font_small = ImageFont.truetype(fc, 16)
            font_tiny = ImageFont.truetype(fc, 13)
            break
        except Exception:
            pass

if not font_large:
    font_large = ImageFont.load_default()
    font_mid = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_tiny = ImageFont.load_default()

# 1. Background subtle grid and glowing circular rings
for r in range(120, 480, 70):
    draw.ellipse([450 - r, 350 - r, 450 + r, 350 + r], outline='#1E3A8A', width=1)

# Glowing radial dots
for x in range(60, 840, 60):
    for y in range(50, 650, 60):
        draw.point((x, y), fill='#1E3A8A')

# 2. Central PDF Document Mockup
doc_x0, doc_y0, doc_x1, doc_y1 = 200, 100, 700, 600
# Document drop shadow
draw.rounded_rectangle([doc_x0 + 15, doc_y0 + 15, doc_x1 + 15, doc_y1 + 15], radius=16, fill='#07182C')
# Document body (White paper)
draw.rounded_rectangle([doc_x0, doc_y0, doc_x1, doc_y1], radius=16, fill='#FFFFFF', outline='#38BDF8', width=3)

# Header ribbon on PDF
draw.rounded_rectangle([doc_x0, doc_y0, doc_x1, doc_y0 + 70], radius=16, fill='#F8FAFC')
draw.rectangle([doc_x0, doc_y0 + 40, doc_x1, doc_y0 + 70], fill='#F8FAFC')
draw.line([doc_x0, doc_y0 + 70, doc_x1, doc_y0 + 70], fill='#E2E8F0', width=2)

# PDF icon badge
draw.rounded_rectangle([doc_x0 + 25, doc_y0 + 18, doc_x0 + 75, doc_y0 + 54], radius=6, fill='#EA580C')
draw.text((doc_x0 + 35, doc_y0 + 24), "PDF", fill='#FFFFFF', font=font_small)

draw.text((doc_x0 + 90, doc_y0 + 22), "CIS-105_Course_Notes_Protected.pdf", fill='#0F2A4A', font=font_mid)

# Document text lines simulation
line_y = doc_y0 + 95
for idx in range(11):
    w_line = 440 if idx % 3 != 0 else 320
    draw.rounded_rectangle([doc_x0 + 30, line_y, doc_x0 + 30 + w_line, line_y + 10], radius=4, fill='#F1F5F9')
    line_y += 24

# 3. Prominent Diagonal Red/Orange Watermark Banner across document
# Rotated simulated banner
draw.line([doc_x0 + 30, doc_y1 - 100, doc_x1 - 30, doc_y0 + 100], fill='#FDBA74', width=45)
draw.line([doc_x0 + 30, doc_y1 - 100, doc_x1 - 30, doc_y0 + 100], fill='#FB923C', width=38)

# Center watermark text
draw.text((450, 335), "RESTRICTED COPY — PRN: 2124UCSM1115", fill='#FFFFFF', font=font_mid, anchor='mm')
draw.text((450, 365), "SANJIVANI UNIVERSITY • TAMPER PROTECTED", fill='#431407', font=font_tiny, anchor='mm')

# 4. Central Verification Shield Badge (Floating bottom-right)
sh_x0, sh_y0, sh_x1, sh_y1 = 530, 430, 740, 620
draw.rounded_rectangle([sh_x0 + 8, sh_y0 + 8, sh_x1 + 8, sh_y1 + 8], radius=16, fill='#07182C')
draw.rounded_rectangle([sh_x0, sh_y0, sh_x1, sh_y1], radius=16, fill='#0F2A4A', outline='#22C55E', width=3)

draw.text(((sh_x0 + sh_x1)//2, sh_y0 + 28), "🛡️ VERIFIED", fill='#22C55E', font=font_mid, anchor='mm')
draw.text(((sh_x0 + sh_x1)//2, sh_y0 + 60), "SHA-256 HASH", fill='#38BDF8', font=font_small, anchor='mm')
draw.text(((sh_x0 + sh_x1)//2, sh_y0 + 85), "e3b0c44298fc...", fill='#94A3B8', font=font_tiny, anchor='mm')
draw.rounded_rectangle([sh_x0 + 20, sh_y0 + 115, sh_x1 - 20, sh_y0 + 150], radius=8, fill='#166534')
draw.text(((sh_x0 + sh_x1)//2, sh_y0 + 132), "✓ 100% UNTAMPERED", fill='#FFFFFF', font=font_tiny, anchor='mm')

# 5. Floating Key / Security Token Chip (Floating top-left)
chip_x0, chip_y0, chip_x1, chip_y1 = 140, 160, 330, 260
draw.rounded_rectangle([chip_x0 + 6, chip_y0 + 6, chip_x1 + 6, chip_y1 + 6], radius=12, fill='#07182C')
draw.rounded_rectangle([chip_x0, chip_y0, chip_x1, chip_y1], radius=12, fill='#EA580C', outline='#FED7AA', width=2)
draw.text((chip_x0 + 15, chip_y0 + 18), "🔑 2D-DCT FREQUENCY", fill='#FFFFFF', font=font_small)
draw.text((chip_x0 + 15, chip_y0 + 44), "Invisible Forensic Mark", fill='#FFEDD5', font=font_tiny)
draw.text((chip_x0 + 15, chip_y0 + 68), "PSNR: 42.8 dB (Hidden)", fill='#FEF08A', font=font_tiny)

os.makedirs("scripts/report_generator/assets/sih", exist_ok=True)
cover_art_path = "scripts/report_generator/assets/sih/sih_cover_art.png"
img.save(cover_art_path, "PNG", quality=95)
print(f"Generated SIH cover art illustration at: {cover_art_path}")
