with open("scripts/report_generator/generate_sih_style_presentation.py", "r") as f:
    code = f.read()

# Replace p_t.add_run(f"  [{tag}]")
old_line = 'r_tag = p_t.add_run(f"  [{tag}]")'
new_line = 'r_tag = p_t.add_run()\n        r_tag.text = f"  [{tag}]"'

code = code.replace(old_line, new_line)

with open("scripts/report_generator/generate_sih_style_presentation.py", "w") as f:
    f.write(code)

print("Fixed add_run syntax!")
