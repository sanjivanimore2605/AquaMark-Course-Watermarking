import os
import shutil
import fitz
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage

os.makedirs("scripts/report_generator/assets/thumbs", exist_ok=True)

# 1. Render each slide of AquaMark_SIH_Style_Presentation.pdf to an image
src_pdf = fitz.open("/Users/omsaishdhokchaule/Downloads/AquaMark_SIH_Style_Presentation.pdf")
thumb_paths = []
for i, page in enumerate(src_pdf):
    pix = page.get_pixmap(dpi=150)
    out_path = f"scripts/report_generator/assets/thumbs/slide_{i+1}.png"
    pix.save(out_path)
    thumb_paths.append(out_path)
print(f"Rendered {len(thumb_paths)} slide thumbnails.")

# 2. Build 1-page A4 landscape Contact Sheet / Preview PDF
preview_pdf_path = "/Users/omsaishdhokchaule/Downloads/AquaMark_All_Slides_Preview.pdf"
doc = SimpleDocTemplate(
    preview_pdf_path,
    pagesize=landscape(A4), # 841.89 x 595.27 pt
    leftMargin=30,
    rightMargin=30,
    topMargin=20,
    bottomMargin=20
)

styles = getSampleStyleSheet()
t_title = ParagraphStyle(
    'Head', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=14, leading=17,
    textColor=colors.HexColor("#0F2A4A"), alignment=1
)
t_sub = ParagraphStyle(
    'Sub', parent=styles['Normal'],
    fontName='Helvetica', fontSize=9, leading=12,
    textColor=colors.HexColor("#64748B"), alignment=1
)

story = [
    Paragraph("AquaMark — SIH Style Presentation: Complete 6-Slide Visual Overview", t_title),
    Paragraph("Presenter: Sanjivani Rameshwar More (PRN: 2124UCSM1115)  |  Guide: Dr. Chetan D. Bawankar  |  PS Code: CIS-105", t_sub),
    Spacer(1, 10)
]

# 2 rows x 3 columns of slide thumbnails
col_w = 250
row_h = 145

grid_cells = [
    [
        Table([[RLImage(thumb_paths[0], width=245, height=138)], [Paragraph("<font size=7.5 color='#0F2A4A'><b>Slide 1: Project Cover</b></font>", t_sub)]]),
        Table([[RLImage(thumb_paths[1], width=245, height=138)], [Paragraph("<font size=7.5 color='#0F2A4A'><b>Slide 2: Proposed Solution &amp; Overview</b></font>", t_sub)]]),
        Table([[RLImage(thumb_paths[2], width=245, height=138)], [Paragraph("<font size=7.5 color='#0F2A4A'><b>Slide 3: Technical Approach &amp; Architecture</b></font>", t_sub)]]),
    ],
    [
        Table([[RLImage(thumb_paths[3], width=245, height=138)], [Paragraph("<font size=7.5 color='#0F2A4A'><b>Slide 4: Feasibility and Viability</b></font>", t_sub)]]),
        Table([[RLImage(thumb_paths[4], width=245, height=138)], [Paragraph("<font size=7.5 color='#0F2A4A'><b>Slide 5: Impact and Benefits</b></font>", t_sub)]]),
        Table([[RLImage(thumb_paths[5], width=245, height=138)], [Paragraph("<font size=7.5 color='#0F2A4A'><b>Slide 6: Research and References</b></font>", t_sub)]]),
    ]
]

t_grid = Table(grid_cells, colWidths=[255, 255, 255])
t_grid.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_grid)

doc.build(story)
shutil.copy(preview_pdf_path, "/Users/omsaishdhokchaule/Downloads/AquaMark/AquaMark_All_Slides_Preview.pdf")
print("All Slides Preview PDF created successfully!")
