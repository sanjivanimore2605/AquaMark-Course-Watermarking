with open("scripts/report_generator/generate_sih_style_pdf.py", "r") as f:
    text = f.read()

# Replace <para align='center'> with inline alignment style or separate Paragraphs
old_navy = """    navy_content = (
        "<para align='center'><font size=11 color='#F97316'><b>CORE SECURITY WORKFLOW</b></font></para><br/><br/>"
        "<font size=9.5 color='white'><b>▶ 1. UPLOAD PDF</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Faculty uploads course materials in standard PDF format.</font><br/><br/>"
        "<font size=9.5 color='white'><b>▶ 2. PROTECT &amp; STAMP</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Engine overlays recipient PRN stamp &amp; computes SHA-256.</font><br/><br/>"
        "<font size=9.5 color='white'><b>▶ 3. VERIFY &amp; AUDIT</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Instant green/red forensic check on circulating copies.</font><br/><br/>"
        "<para align='center'><font size=8 color='#38BDF8'><b>Sub-1.2s &nbsp;•&nbsp; 0 Distortion &nbsp;•&nbsp; 100% Catch</b></font></para>"
    )"""

new_navy = """    navy_content = (
        "<font size=11 color='#F97316'><b>CORE SECURITY WORKFLOW</b></font><br/><br/>"
        "<font size=9.5 color='white'><b>&gt; 1. UPLOAD PDF</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Faculty uploads course materials in standard PDF format.</font><br/><br/>"
        "<font size=9.5 color='white'><b>&gt; 2. PROTECT &amp; STAMP</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Engine overlays recipient PRN stamp &amp; computes SHA-256.</font><br/><br/>"
        "<font size=9.5 color='white'><b>&gt; 3. VERIFY &amp; AUDIT</b></font><br/>"
        "<font size=8.5 color='#CBD5E1'>Instant green/red forensic check on circulating copies.</font><br/><br/>"
        "<font size=8 color='#38BDF8'><b>Sub-1.2s &nbsp;•&nbsp; 0 Distortion &nbsp;•&nbsp; 100% Catch</b></font>"
    )"""

text = text.replace(old_navy, new_navy)

old_hero = """    hero_box = (
        "<para align='center'><font size=12 color='#F97316'><b>ACADEMIC SECURITY GUARANTEE</b></font><br/><br/>"
        "<font size=10 color='white'><b>SUB-SECOND EXECUTION &nbsp;•&nbsp; ZERO LICENSING COST</b></font><br/><br/>"
        "<font size=8.5 color='#CBD5E1'>Every document receives an immutable 256-bit SHA-256 digital fingerprint and recipient watermark record.</font><br/><br/>"
        "<font size=8.5 color='#93C5FD'>Standard PDF compatibility: Works on all phones, tablets, and PCs without proprietary apps.</font></para>"
    )"""

new_hero = """    hero_box = (
        "<font size=12 color='#F97316'><b>ACADEMIC SECURITY GUARANTEE</b></font><br/><br/>"
        "<font size=10 color='white'><b>SUB-SECOND EXECUTION &nbsp;•&nbsp; ZERO LICENSING COST</b></font><br/><br/>"
        "<font size=8.5 color='#CBD5E1'>Every document receives an immutable 256-bit SHA-256 digital fingerprint and recipient watermark record.</font><br/><br/>"
        "<font size=8.5 color='#93C5FD'>Standard PDF compatibility: Works on all phones, tablets, and PCs without proprietary apps.</font>"
    )"""

text = text.replace(old_hero, new_hero)

old_b_cells = """    for b_hdr, b_title, b_desc, b_clr in b_cards:
        cell_b = (
            f"<para align='center'><font size=8.5 color='white'><b>{b_hdr}</b></font></para><br/>"
            f"<font size=10 color='#0F2A4A'><b>{b_title}</b></font><br/><br/>"
            f"<font size=8.5 color='#1E293B'>{b_desc}</font>"
        )
        b_cells.append(Paragraph(cell_b, card_d))"""

new_b_cells = """    for b_hdr, b_title, b_desc, b_clr in b_cards:
        cell_b = (
            f"<font size=8.5 color='{b_clr}'><b>{b_hdr}</b></font><br/>"
            f"<font size=10 color='#0F2A4A'><b>{b_title}</b></font><br/><br/>"
            f"<font size=8.5 color='#1E293B'>{b_desc}</font>"
        )
        b_cells.append(Paragraph(cell_b, card_d))"""

text = text.replace(old_b_cells, new_b_cells)

with open("scripts/report_generator/generate_sih_style_pdf.py", "w") as f:
    f.write(text)

print("ReportLab markup sanitized!")
