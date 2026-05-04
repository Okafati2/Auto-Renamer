# Invoice Auto-Renamer — PLAN.md

## Project Overview
A Python script that reads PDF invoices, extracts the invoice 
number and date from the first page using OCR, and renames 
the file automatically. Packaged as a Windows installer 
(.exe) using PyInstaller + NSIS.

## Renamed File Format
F-[last 4 digits of invoice number]_DD-MM-YYYY.pdf
Example: F-2345_14-05-2026.pdf

## Invoice Fields to Extract
- Número de factura: XXX-XXX-XX-XXXXXXXX → take last 4 digits
- Fecha de emisión: XX de mes de 202X HH:MM → convert to DD-MM-YYYY

## How It Works
- Manual mode: point the script at a folder, 
  it processes all PDFs inside
- Watch mode: monitors a folder continuously, 
  renames new PDFs as they arrive
- After renaming: original file is deleted, 
  renamed file takes its place in the same folder

## Tech Stack
- Language: Python
- PDF text extraction: pdfplumber (no Tesseract needed)
- Folder watching: watchdog library
- Date parsing: Python built-in datetime
- Text matching: regex (built-in re module)
- Packaging: PyInstaller + NSIS

## Folder Structure
invoice-renamer/
├── main.py           # Entry point, handles manual/watch mode
├── extractor.py      # PDF text extraction and field parsing
├── renamer.py        # File renaming and deletion logic
├── watcher.py        # Folder watch mode using watchdog
├── config.py         # Settings (folder path, patterns)
├── requirements.txt  # Python dependencies for developers
└── PLAN.md           # This file

## Requirements.txt Contents
pdfplumber
watchdog
pyinstaller

## Spanish Month Mapping
enero=01, febrero=02, marzo=03, abril=04,
mayo=05, junio=06, julio=07, agosto=08,
septiembre=09, octubre=10, noviembre=11, diciembre=12

## For Developers (running from source)
1. Clone the repository
2. Run: pip install -r requirements.txt
3. Run: python main.py

## For End Users (Windows installer)
1. Download InvoiceRenamer_Setup.exe
2. Double-click and follow the install wizard
3. Launch from Start Menu or Desktop shortcut

## Tasks

### Task 1 — Project setup
- Create folder structure and empty files
- Create requirements.txt with: pdfplumber, watchdog, 
  pyinstaller
- Install dependencies: pip install -r requirements.txt
- Verify all imports work

### Task 2 — PDF text extraction
- In extractor.py, write a function extract_text(filepath):
  - Opens a PDF using pdfplumber
  - Extracts text from the first page only
  - Returns the raw text as a string
  - If extraction fails, returns None
- Test with a real invoice PDF

### Task 3 — Field parsing
- In extractor.py, write two functions:
  - extract_invoice_number(text): uses regex to find
    "Número de factura: XXX-XXX-XX-XXXXXXXX"
    and returns the last 4 digits of the final segment
  - extract_date(text): uses regex to find
    "Fecha de emisión: XX de mes de 202X HH:MM"
    converts Spanish month name to number
    and returns the date as DD-MM-YYYY
- Include full Spanish month name to number mapping:
  enero=01, febrero=02, marzo=03, abril=04,
  mayo=05, junio=06, julio=07, agosto=08,
  septiembre=09, octubre=10, noviembre=11, diciembre=12
- Test both functions with real extracted text

### Task 4 — Renaming logic
- In renamer.py, write rename_invoice(filepath):
  - Calls extractor.py to get invoice number and date
  - Builds new filename: F-XXXX_DD-MM-YYYY.pdf
  - Checks if a file with that name already exists —
    if so, appends a counter: F-XXXX_DD-MM-YYYY_2.pdf
  - Renames the file in the same folder
  - Deletes the original file
  - Returns the new filepath
  - If extraction fails, skips and logs a warning

### Task 5 — Manual mode
- In main.py, write process_folder(folder_path):
  - Validates that the folder exists
  - Scans for all .pdf files in the folder
  - Calls rename_invoice() on each one
  - Prints a live progress update for each file
  - Prints a final summary:
    "Done: X renamed, X skipped"

### Task 6 — Watch mode
- In watcher.py, use watchdog to:
  - Monitor a folder for new .pdf files
  - When a new PDF is detected, do NOT process it immediately
  - Instead, run a file stability check:
    - Check the file size
    - Wait 1 second
    - Check the file size again
    - If size is unchanged → file is fully written → process it
    - If size changed → wait 1 more second and check again
    - Repeat until stable, with a maximum timeout of 120 seconds
    - If 120 seconds pass and file is still changing →
      log "Timeout waiting for file to finish writing: [filename]"
      and skip it
  - Once file is confirmed stable, call rename_invoice() on it
  - Print a timestamped message for each file processed
  - Keep running until the user presses Ctrl+C

### Task 7 — Entry point
- In main.py, add a simple menu at launch:
  - Option 1: Manual mode — asks for folder path,
    processes all PDFs currently in the folder
  - Option 2: Watch mode — asks for folder path,
    starts monitoring for new PDFs
  - Option 3: Exit
- Print clear instructions for each option
- Handle invalid menu input gracefully

### Task 8 — Error handling
- If pdfplumber cannot read a PDF:
  log "Could not read: [filename]"
- If regex finds no match:
  log "Could not extract fields from: [filename]"
- If a duplicate filename is detected:
  append counter to avoid overwriting
- If renaming fails:
  log "Rename failed: [filename] — [error]"
- Never crash on a single bad file —
  always continue to the next one

### Task 9 — Testing checklist
- [ ] Script launches and shows menu
- [ ] Manual mode renames all PDFs correctly
- [ ] Watch mode detects and renames new PDFs automatically
- [ ] Duplicate filenames handled without overwriting
- [ ] Unreadable files skipped with clear warning
- [ ] No original files left behind after successful rename
- [ ] pip install -r requirements.txt installs everything

### Task 10 — Package as Windows installer
- Use PyInstaller to build a standalone .exe
- Use NSIS to wrap it into a proper Windows installer with:
  - Install wizard (Next, Next, Install)
  - Start Menu shortcut
  - Desktop shortcut (optional, user choice)
  - Uninstall entry in Windows Settings
- Final output: InvoiceRenamer_Setup.exe
- Test installer on a clean Windows environment