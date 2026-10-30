import os
import subprocess

docx_path = os.path.abspath("/Users/omsaishdhokchaule/Downloads/2124UCSM11115_CIS-105_ICSReport.docx")
pdf_path = os.path.abspath("/Users/omsaishdhokchaule/Downloads/2124UCSM11115_CIS-105_ICSReport.pdf")

apple_script = f'''
tell application "Microsoft Word"
    activate
    open POSIX file "{docx_path}"
    set activeDoc to active document
    save as activeDoc file name "{pdf_path}" file format format PDF
    close activeDoc saving no
end tell
'''

res = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
