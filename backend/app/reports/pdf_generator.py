import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from typing import Dict, Any

def generate_pdf_verification_report(report_data: Dict[str, Any], output_path: str):
    """Generates an official cryptographic audit verification report in PDF format."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Header Banner
    c.setFillColor(colors.HexColor("#0f172a")) # Slate 900
    c.rect(0, height - 90, width, 90, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 45, "AquaMark™ Forensic Verification Certificate")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 65, "Cryptographic Authenticity & Digital Watermark Analysis Report")
    
    # Body Content
    c.setFillColor(colors.black)
    y = height - 120
    
    def draw_row(label: str, value: str, is_highlight: bool = False, color=colors.black):
        nonlocal y
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(40, y, label)
        c.setFont("Helvetica", 10)
        c.setFillColor(color if is_highlight else colors.black)
        c.drawString(220, y, str(value)[:75])
        y -= 22

    status_str = report_data.get("status_summary", "UNKNOWN")
    status_color = colors.HexColor("#16a34a") if "AUTHENTIC" in status_str else colors.HexColor("#dc2626")
    
    draw_row("Overall Verdict:", status_str, is_highlight=True, color=status_color)
    draw_row("Verification Timestamp:", report_data.get("timestamp", ""))
    draw_row("Candidate File Name:", report_data.get("candidate_filename", ""))
    draw_row("Candidate SHA-256 Hash:", report_data.get("candidate_sha256", ""))
    
    y -= 10
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.line(40, y, width - 40, y)
    y -= 20
    
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawString(40, y, "Cryptographic Manifest & Signature Evaluation")
    y -= 25
    
    draw_row("Manifest ID:", report_data.get("manifest_id", "Not Provided"))
    draw_row("Signing Key ID:", report_data.get("signing_key_id", "Not Provided"))
    draw_row("Digital Signature Valid:", "YES (Ed25519 Canonical Verified)" if report_data.get("signature_valid") else "NO / FAILED")
    draw_row("File Hash Match Recorded:", "YES (Exact match with recorded output)" if report_data.get("exact_hash_match") else "NO (Modified content detected)")
    
    y -= 10
    c.line(40, y, width - 40, y)
    y -= 20
    
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawString(40, y, "Digital Watermark Forensic Extraction")
    y -= 25
    
    draw_row("Watermark Method:", report_data.get("watermark_algorithm", "None"))
    draw_row("Watermark Detected:", "YES" if report_data.get("watermark_detected") else "NO")
    draw_row("Extracted Payload / Text:", report_data.get("extracted_payload") or "N/A")
    draw_row("Recipient Identifier:", report_data.get("recipient_identifier") or "None (Generic)")
    
    # Security Note / Disclaimer
    y -= 30
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.rect(40, y - 50, width - 80, 60, fill=True, stroke=True)
    c.setFillColor(colors.HexColor("#475569"))
    c.setFont("Helvetica-Oblique", 8)
    disclaimer = (
        "IMPORTANT FORENSIC NOTICE: AquaMark verification confirms cryptographic integrity and embedded payload "
        "presence relative to records signed by the verified authority. Digital signatures verify integrity under stated "
        "trust assumptions and do not constitute legal proof of original document ownership."
    )
    c.drawString(50, y - 20, disclaimer[:105])
    c.drawString(50, y - 32, disclaimer[105:])
    
    c.save()
    return output_path
