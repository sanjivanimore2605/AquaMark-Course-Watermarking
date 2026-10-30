import os
import fitz  # PyMuPDF
from typing import Dict, Any

def apply_visible_watermark(
    input_pdf_path: str,
    output_pdf_path: str,
    text: str,
    subtext: str = "",
    opacity: float = 0.3,
    font_size: float = 38.0,
    rotation: float = 45.0,
    color: tuple = (0.3, 0.4, 0.6)
) -> Dict[str, Any]:
    """
    Applies high-grade visible watermark overlays across PDF pages.
    Preserves vector geometry, existing layers, page rotation, and bounding boxes.
    """
    doc = fitz.open(input_pdf_path)
    page_count = len(doc)
    
    for page in doc:
        rect = page.rect
        center_x = (rect.x0 + rect.x1) / 2
        center_y = (rect.y0 + rect.y1) / 2
        
        # Center watermark box using morph rotation
        center_point = fitz.Point(center_x, center_y)
        morph = (center_point, fitz.Matrix(rotation))
        
        # Main watermark text box
        box_w = min(rect.width * 0.9, 500)
        box_h = font_size * 2.5
        main_box = fitz.Rect(center_x - box_w / 2, center_y - box_h / 2, center_x + box_w / 2, center_y + box_h / 2)
        
        page.insert_textbox(
            main_box,
            text,
            fontsize=font_size,
            color=color,
            fill_opacity=opacity,
            align=fitz.TEXT_ALIGN_CENTER,
            morph=morph
        )
        
        # Optional subtext (recipient info, timestamp, license)
        if subtext:
            sub_h = font_size * 1.5
            sub_box = fitz.Rect(center_x - box_w / 2, center_y + font_size * 0.6, center_x + box_w / 2, center_y + font_size * 0.6 + sub_h)
            page.insert_textbox(
                sub_box,
                subtext,
                fontsize=font_size * 0.45,
                color=color,
                fill_opacity=min(1.0, opacity + 0.1),
                align=fitz.TEXT_ALIGN_CENTER,
                morph=morph
            )
            
        # Top banner security marking
        banner_point = fitz.Point(rect.x0 + 20, rect.y0 + 25)
        page.insert_text(
            banner_point,
            f"AquaMark Secured Document | {text}",
            fontsize=9.0,
            color=(0.4, 0.4, 0.4),
            fill_opacity=0.6
        )
    
    doc.save(output_pdf_path, garbage=3, deflate=True)
    doc.close()
    
    return {
        "status": "SUCCESS",
        "pages_watermarked": page_count,
        "watermark_type": "visible_text_overlay"
    }
