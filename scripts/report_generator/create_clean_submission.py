import docx
import shutil

src = "/Users/omsaishdhokchaule/Downloads/ICS_Short_Project_Report_Format.docx"
sub_file = "/Users/omsaishdhokchaule/Downloads/2124UCSM11115_CIS-105_ICSReport.docx"

# Copy original edited file to submission name
shutil.copy(src, sub_file)

doc = docx.Document(sub_file)

# In submission file, delete elements of the instruction page (Table 0, P0-P12, Table 1, Table 2)
# Let's inspect the body elements to delete everything before "A Project Report on"
body = doc.element.body
elements_to_delete = []

for child in body:
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        p = docx.text.paragraph.Paragraph(child, doc)
        if "A Project Report on" in p.text:
            break
        elements_to_delete.append(child)
    elif tag == 'tbl':
        t = docx.table.Table(child, doc)
        # Check if it's Table 0, 1, or 2 (before the Cover Page)
        elements_to_delete.append(child)

print(f"Deleting {len(elements_to_delete)} instruction elements from submission file...")
for el in elements_to_delete:
    body.remove(el)

doc.save(sub_file)
shutil.copy(sub_file, "/Users/omsaishdhokchaule/Downloads/AquaMark/2124UCSM11115_CIS-105_ICSReport.docx")
print("Saved clean submission file without instruction page!")
