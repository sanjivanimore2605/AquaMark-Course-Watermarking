import os
import subprocess

pptx_path = os.path.abspath("/Users/omsaishdhokchaule/Downloads/AquaMark_Project_Presentation.pptx")
pdf_path = os.path.abspath("/Users/omsaishdhokchaule/Downloads/AquaMark_Project_Presentation.pdf")

# AppleScript to use Microsoft PowerPoint if available, or Keynote
apple_script_powerpoint = f'''
tell application "Microsoft PowerPoint"
    activate
    open POSIX file "{pptx_path}"
    set activePres to active presentation
    save activePres in POSIX file "{pdf_path}" as save as PDF
    close activePres saving no
end tell
'''

res = subprocess.run(["osascript", "-e", apple_script_powerpoint], capture_output=True, text=True)
print("PowerPoint conversion return code:", res.returncode)
if res.returncode != 0:
    print("PowerPoint error:", res.stderr)
    print("Trying Keynote...")
    apple_script_keynote = f'''
    tell application "Keynote"
        activate
        open POSIX file "{pptx_path}"
        set doc to front document
        export doc to POSIX file "{pdf_path}" as PDF
        close doc saving no
    end tell
    '''
    res_k = subprocess.run(["osascript", "-e", apple_script_keynote], capture_output=True, text=True)
    print("Keynote conversion return code:", res_k.returncode)
    if res_k.returncode != 0:
        print("Keynote error:", res_k.stderr)
