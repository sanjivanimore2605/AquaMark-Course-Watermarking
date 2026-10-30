import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

os.makedirs("scripts/report_generator/assets/sih", exist_ok=True)

# 1. Generate QR Code for Project Demo / GitHub
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=2,
)
qr.add_data("https://github.com/sanjivani-more/AquaMark-Course-Watermarking")
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#0F2A4A", back_color="white")
qr_img.save("scripts/report_generator/assets/sih/demo_qr.png")

# 2. Generate a professional illustration for Slide 1 (Digital Document Security Shield)
w, h = 800, 800
img_ill = Image.new('RGBA', (w, h), (255, 255, 255, 0))
draw = ImageDraw.Draw(img_ill)

# Outer glowing circle
draw.ellipse([40, 40, 760, 760], fill='#F0F9FF', outline='#BAE6FD', width=6)
draw.ellipse([100, 100, 700, 700], fill='#E0F2FE', outline='#7DD3FC', width=4)

# Central Shield
shield_pts = [
    (400, 160), # Top center
    (580, 210), # Top right
    (580, 460), # Right curve
    (400, 640), # Bottom tip
    (220, 460), # Left curve
    (220, 210)  # Top left
]
draw.polygon(shield_pts, fill='#0F2A4A', outline='#0284C7', width=8)

# Document graphic inside shield
draw.rounded_rectangle([300, 250, 500, 520], radius=14, fill='#FFFFFF', outline='#E2E8F0', width=4)
# Corner fold
draw.polygon([(460, 250), (500, 290), (460, 290)], fill='#CBD5E1')

# Document content lines (dummy text)
for y in range(320, 470, 25):
    draw.line([330, y, 470, y], fill='#94A3B8', width=5)

# Watermark diagonal stamp across document
draw.line([320, 460, 480, 310], fill='#F97316', width=8)

# Center Checkmark
check_pts = [
    (360, 400),
    (390, 430),
    (445, 365)
]
draw.line(check_pts, fill='#10B981', width=10, joint='curve')

img_ill.save("scripts/report_generator/assets/sih/security_illustration.png")

# 3. Generate Feasibility Large Shield Visual for Slide 4
w_s, h_s = 600, 600
img_sh = Image.new('RGBA', (w_s, h_s), (255, 255, 255, 0))
draw_s = ImageDraw.Draw(img_sh)
shield_pts_large = [
    (300, 80),
    (480, 130),
    (480, 380),
    (300, 520),
    (120, 380),
    (120, 130)
]
draw_s.polygon(shield_pts_large, fill='#FFFFFF', outline='#38BDF8', width=8)
# Lock icon inside shield
draw_s.rounded_rectangle([230, 280, 370, 400], radius=12, fill='#0F2A4A')
draw_s.arc([250, 210, 350, 320], start=180, end=0, fill='#0F2A4A', width=14)
draw_s.ellipse([285, 320, 315, 350], fill='#F97316')
draw_s.line([300, 345, 300, 375], fill='#F97316', width=6)

img_sh.save("scripts/report_generator/assets/sih/shield_icon.png")
print("SIH assets created successfully!")
