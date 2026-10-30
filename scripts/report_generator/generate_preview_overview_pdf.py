import fitz # PyMuPDF
import os
import shutil
from PIL import Image

src_pdf = "/Users/omsaishdhokchaule/Downloads/AquaMark_SIH_Style_Presentation.pdf"
preview_pdf_out = "/Users/omsaishdhokchaule/Downloads/AquaMark_All_Slides_Preview.pdf"

doc = fitz.open(src_pdf)
print(f"Opened source presentation with {len(doc)} pages.")

# Render each page to an image
pixmaps = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    img_path = f"scripts/report_generator/assets/sih/page_{i+1}.png"
    pix.save(img_path)
    pixmaps.append(img_path)

# Create a composite 2 columns x 3 rows sheet (or A4 landscape overview)
# Canvas width: 2400 x 1800
canvas_w, canvas_h = 2400, 1800
composite = Image.new('RGB', (canvas_w, canvas_h), color='#F1F5F9')

# Grid setup
cols, rows = 2, 3
thumb_w, thumb_h = 1080, 520
pad_x = 80
pad_y = 50

for idx, p_img in enumerate(pixmaps):
    im = Image.open(p_img)
    im_resized = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    c = idx % cols
    r = idx // cols
    pos_x = pad_x + c * (thumb_w + pad_x)
    pos_y = pad_y + r * (thumb_h + pad_y)
    composite.paste(im_resized, (pos_x, pos_y))

composite_img_path = "scripts/report_generator/assets/sih/all_slides_sheet.png"
composite.save(composite_img_path, "PNG", quality=95)

# Convert composite image into single-page overview PDF
comp_pdf = fitz.open()
img_doc = fitz.open(composite_img_path)
rect = img_doc[0].rect
pdfbytes = img_doc.convert_to_pdf()
img_pdf = fitz.open("pdf", pdfbytes)
page = comp_pdf.new_page(width=rect.width, height=rect.height)
page.show_pdf_page(rect, img_pdf, 0)
comp_pdf.save(preview_pdf_out)
comp_pdf.close()
doc.close()

shutil.copy(preview_pdf_out, "/Users/omsaishdhokchaule/Downloads/AquaMark/AquaMark_All_Slides_Preview.pdf")
print(f"Generated visual thumbnail preview PDF at: {preview_pdf_out}")
