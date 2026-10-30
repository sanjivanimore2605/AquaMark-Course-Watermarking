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
            font_large = ImageFont.truetype(fc, 38)
            font_mid = ImageFont.truetype(fc, 20)
            font_small = ImageFont.truetype(fc, 14)
            break
        except Exception:
            pass

if not font_large:
    font_large = ImageFont.load_default()
    font_mid = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Background subtle rings
for r in [80, 140, 200, 260]:
    draw.ellipse([210 - r, 220 - r, 210 + r, 220 + r], outline='#1E3A8A', width=1)

# Large Center Badge
draw.text((210, 45), "DEFENSE IN DEPTH", fill='#38BDF8', font=font_small, anchor='mm')

# Center Shield
sh_x0, sh_y0, sh_x1, sh_y1 = 110, 85, 310, 295
draw.rounded_rectangle([sh_x0, sh_y0, sh_x1, sh_y1], radius=24, fill='#1E3A8A', outline='#EA580C', width=4)

draw.text((210, 145), "🛡️", fill='#FFFFFF', font=font_large, anchor='mm')
draw.text((210, 205), "3-TIER", fill='#FFFFFF', font=font_large, anchor='mm')
draw.text((210, 245), "SECURITY", fill='#FED7AA', font=font_mid, anchor='mm')

# Workflow text
draw.rounded_rectangle([30, 325, 390, 465], radius=12, fill='#0B1F36', outline='#38BDF8', width=1)
draw.text((210, 355), "CORE PROTECTION GUARANTEE", fill='#EA580C', font=font_small, anchor='mm')

items = [
    "✓ 100% Zero New Hardware Needed",
    "✓ Standard PDF Client Compatibility",
    "✓ 0.82s Real-Time Latency / Page",
    "✓ SHA-256 Byte-Level Tamper Proof"
]
cur_y = 380
for it in items:
    draw.text((50, cur_y), it, fill='#E2E8F0', font=font_small)
    cur_y += 20

os.makedirs("scripts/report_generator/assets/sih", exist_ok=True)
out_path = "scripts/report_generator/assets/sih/sih_feasibility_art.png"
img.save(out_path, "PNG", quality=95)
print(f"Generated SIH feasibility panel art at: {out_path}")
