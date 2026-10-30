import os
from PIL import Image, ImageDraw, ImageFont

# Set up canvas with high resolution (300 DPI equivalent)
width, height = 2400, 1300
img = Image.new('RGB', (width, height), color='#FFFFFF')
draw = ImageDraw.Draw(img)

# Try loading standard system fonts or fall back to default
font_title = None
font_box_title = None
font_body = None
font_small = None

font_candidates = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf"
]

for fc in font_candidates:
    if os.path.exists(fc):
        try:
            font_title = ImageFont.truetype(fc, 44)
            font_box_title = ImageFont.truetype(fc, 32)
            font_body = ImageFont.truetype(fc, 24)
            font_small = ImageFont.truetype(fc, 20)
            break
        except Exception:
            pass

if not font_title:
    font_title = ImageFont.load_default()
    font_box_title = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_small = ImageFont.load_default()

# 1. Main outer border and header banner
draw.rounded_rectangle([30, 30, width - 30, height - 30], radius=20, outline='#0F2A4A', width=4)
draw.rounded_rectangle([30, 30, width - 30, 130], radius=20, fill='#0F2A4A')
draw.rectangle([30, 90, width - 30, 130], fill='#0F2A4A') # square bottom corners

title_text = "AquaMark: Layered Digital Watermarking & Document Integrity Architecture"
draw.text((width // 2, 80), title_text, fill='#FFFFFF', font=font_title, anchor='mm')

# 2. Top Tier: 3 Primary Actors / Components
# User / Faculty Client -> Web UI (React) -> Application Server (FastAPI)
def draw_card(box, title, subtitle, items, bg_color='#F4F6F9', border_color='#0F2A4A'):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=bg_color, outline=border_color, width=3)
    # Header of card
    draw.rounded_rectangle([x0, y0, x1, y0 + 60], radius=14, fill=border_color)
    draw.rectangle([x0, y0 + 30, x1, y0 + 60], fill=border_color)
    draw.text(((x0 + x1) // 2, y0 + 30), title, fill='#FFFFFF', font=font_box_title, anchor='mm')
    
    cur_y = y0 + 80
    if subtitle:
        draw.text(((x0 + x1) // 2, cur_y), subtitle, fill='#555555', font=font_small, anchor='mm')
        cur_y += 35
        
    for item in items:
        draw.text((x0 + 25, cur_y), "•  " + item, fill='#222222', font=font_body)
        cur_y += 38

# Card 1: Faculty / Student Client
draw_card([80, 180, 720, 480], "1. User & Client Interface", "Educators, Students & Evaluators", [
    "Upload original lecture notes & course PDFs",
    "Specify recipient details (PRN, batch, subject)",
    "Download protected course documents",
    "Upload distributed PDFs for tamper verification"
], bg_color='#F8FAFC', border_color='#1E3A8A')

# Card 2: Frontend Application
draw_card([840, 180, 1560, 480], "2. Web Application Interface", "Modern Responsive Frontend (React)", [
    "Secure JWT-based user session handling",
    "Interactive document management dashboard",
    "Live preview of visible watermark placement",
    "Real-time integrity & audit report visualization"
], bg_color='#F8FAFC', border_color='#0369A1')

# Card 3: Backend Controller
draw_card([1680, 180, 2320, 480], "3. Application Controller", "High-Performance Backend (FastAPI)", [
    "RESTful API endpoints for all workflows",
    "Role-based access control & authentication",
    "Asynchronous PDF document processing",
    "Audit logging & event dispatching"
], bg_color='#F8FAFC', border_color='#047857')

# Arrows connecting top cards
def draw_arrow(start, end, text="", color='#0F2A4A'):
    x0, y0 = start
    x1, y1 = end
    draw.line([x0, y0, x1, y1], fill=color, width=4)
    # Arrow head pointing to (x1, y1)
    if x1 > x0: # pointing right
        draw.polygon([(x1, y1), (x1 - 18, y1 - 10), (x1 - 18, y1 + 10)], fill=color)
    elif x1 < x0: # pointing left
        draw.polygon([(x1, y1), (x1 + 18, y1 - 10), (x1 + 18, y1 + 10)], fill=color)
    elif y1 > y0: # pointing down
        draw.polygon([(x1, y1), (x1 - 10, y1 - 18), (x1 + 10, y1 - 18)], fill=color)
    if text:
        draw.text(((x0 + x1) // 2, (y0 + y1) // 2 - 18), text, fill='#0F2A4A', font=font_small, anchor='mm')

draw_arrow((720, 330), (840, 330), "HTTP / JSON")
draw_arrow((1560, 330), (1680, 330), "REST API")

# Arrow from Backend down to Processing Pipeline
draw_arrow((2000, 480), (2000, 560), "Dispatch")

# 3. Middle Tier: Core Processing Engines
# Big container for Watermarking & Cryptographic Core
draw.rounded_rectangle([80, 560, 2320, 940], radius=16, fill='#F1F5F9', outline='#475569', width=2)
draw.text((120, 580), "CORE DOCUMENT PROTECTION & INTEGRITY ENGINE", fill='#0F2A4A', font=font_box_title)

# Engine Box A: Visible Watermarking Engine
draw_card([120, 630, 780, 910], "Visible Watermark Layer", "Deterrence & Identification", [
    "Applies diagonal semi-transparent text",
    "Stamps Recipient PRN, Name & Timestamp",
    "Embeds institutional copyright notice",
    "Preserves complete reading legibility"
], bg_color='#FFFFFF', border_color='#B91C1C')

# Engine Box B: Invisible Watermark Engine
draw_card([830, 630, 1570, 910], "Invisible Watermark Layer", "Transform-Domain Robustness", [
    "Decomposes page graphics into 8x8 blocks",
    "Embeds covert tracking bits in mid-frequencies",
    "Humanly imperceptible (PSNR > 40 dB)",
    "Resists format conversion, noise & cropping"
], bg_color='#FFFFFF', border_color='#D97706')

# Engine Box C: Cryptographic Integrity Engine
draw_card([1620, 630, 2280, 910], "Cryptographic Integrity Layer", "Tamper Detection & Verification", [
    "Generates unique SHA-256 document hash",
    "Creates signed HMAC verification manifest",
    "Detects single-character or single-byte changes",
    "Instantly validates file authenticity"
], bg_color='#FFFFFF', border_color='#059669')

# Connect backend to engines
draw.line([(2000, 560), (450, 560)], fill='#0F2A4A', width=3)
draw_arrow((450, 560), (450, 630))
draw_arrow((1200, 560), (1200, 630))
draw_arrow((1950, 560), (1950, 630))

# Arrow down from engines to Storage Tier
draw_arrow((1200, 940), (1200, 1000), "Persist & Audit")

# 4. Bottom Tier: Secure Storage & Audit Layer
draw.rounded_rectangle([80, 1000, 2320, 1240], radius=16, fill='#FAF5FF', outline='#7E22CE', width=3)
draw.text((width // 2, 1030), "4. SECURE STORAGE, VERIFICATION & AUDIT LAYER", fill='#6B21A8', font=font_box_title, anchor='mm')

storage_items = [
    ("Relational Database (SQLite)", "Stores user records, document metadata, watermark history, and cryptographic digests."),
    ("Protected Document Vault", "Safely separates untampered original files from watermarked and distributed deliverables."),
    ("Verification & Tamper Engine", "Recomputes hashes upon upload and flags any modification, page removal, or text tampering."),
    ("Complete Audit Trail", "Maintains indisputable evidence logs of who generated, received, and verified each course document.")
]

card_w = 520
start_x = 110
for idx, (head, desc) in enumerate(storage_items):
    bx = start_x + idx * (card_w + 30)
    draw.rounded_rectangle([bx, 1070, bx + card_w, 1210], radius=10, fill='#FFFFFF', outline='#C084FC', width=2)
    draw.text((bx + 20, 1090), head, fill='#581C87', font=font_body)
    # wrap description text
    words = desc.split()
    line1 = " ".join(words[:5])
    line2 = " ".join(words[5:11])
    line3 = " ".join(words[11:])
    draw.text((bx + 20, 1125), line1, fill='#4A5568', font=font_small)
    draw.text((bx + 20, 1150), line2, fill='#4A5568', font=font_small)
    if line3:
        draw.text((bx + 20, 1175), line3, fill='#4A5568', font=font_small)

os.makedirs("scripts/report_generator/assets", exist_ok=True)
output_path = "scripts/report_generator/assets/system_architecture.png"
img.save(output_path, "PNG", quality=95)
print(f"Professional architecture diagram generated at: {output_path}")
