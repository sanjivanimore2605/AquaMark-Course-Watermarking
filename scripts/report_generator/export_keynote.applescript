set pptxPath to POSIX file "/Users/omsaishdhokchaule/Downloads/AquaMark_Project_Presentation.pptx"
set pdfPath to POSIX file "/Users/omsaishdhokchaule/Downloads/AquaMark_Project_Presentation.pdf"

tell application "Keynote"
    activate
    set theDoc to open pptxPath
    delay 2
    export theDoc to pdfPath as PDF with properties {PDF image quality:Best}
    close theDoc saving no
end tell
