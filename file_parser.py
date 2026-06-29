"""
file_parser.py — Parse uploaded files into structured text context for Haiku triage.

Supported: Excel (.xlsx/.xls), CSV, PDF, plain text, images (description prompt).
"""

import os
import csv
import json
from pathlib import Path


# ── Excel ──────────────────────────────────────────────────────────────────────

def _parse_excel(filepath: str) -> dict:
    try:
        import openpyxl
    except ImportError:
        return {"_error": "openpyxl not installed — run: pip install openpyxl"}

    wb = openpyxl.load_workbook(filepath, data_only=True)
    result = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = []
        for row in ws.iter_rows(values_only=True):
            if any(cell is not None for cell in row):
                rows.append([str(c).strip() if c is not None else "" for c in row])
        if rows:
            result[sheet_name] = rows
    return result


def _excel_to_text(filepath: str) -> str:
    data = _parse_excel(filepath)
    name = Path(filepath).name

    if "_error" in data:
        return f"FILE: {name}\n[ERROR: {data['_error']}]"

    lines = [f"FILE: {name}  (Excel workbook — {len(data)} sheet(s))\n"]
    for sheet, rows in data.items():
        lines.append(f"\n┌─ Sheet: '{sheet}' ({len(rows)} rows) ─────────────────┐")
        # First row as header
        if rows:
            header = rows[0]
            lines.append("  COLUMNS: " + " | ".join(f"[{i}] {h}" for i, h in enumerate(header)))
            lines.append("  ─────────────────────────────────────────────────────")
        for r_idx, row in enumerate(rows[:150]):   # cap: 150 rows / sheet
            lines.append("  " + "\t".join(row))
        if len(rows) > 150:
            lines.append(f"  ... ({len(rows)-150} more rows truncated)")
        lines.append("└─────────────────────────────────────────────────────────┘")
    return "\n".join(lines)


# ── CSV ────────────────────────────────────────────────────────────────────────

def _csv_to_text(filepath: str) -> str:
    name = Path(filepath).name
    rows = []
    try:
        with open(filepath, newline="", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        return f"FILE: {name}\n[ERROR reading CSV: {e}]"

    lines = [f"FILE: {name}  (CSV — {len(rows)} rows)\n"]
    if rows:
        lines.append("  COLUMNS: " + " | ".join(f"[{i}] {h}" for i, h in enumerate(rows[0])))
        lines.append("  ─────────────────────────────────────────────────────")
    for row in rows[:200]:
        lines.append("  " + "\t".join(row))
    if len(rows) > 200:
        lines.append(f"  ... ({len(rows)-200} more rows truncated)")
    return "\n".join(lines)


# ── PDF ────────────────────────────────────────────────────────────────────────

def _pdf_to_text(filepath: str) -> str:
    name = Path(filepath).name
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            pages = []
            for i, page in enumerate(pdf.pages[:30]):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append(f"--- Page {i+1} ---\n{text}")
        full = "\n\n".join(pages)
        return f"FILE: {name}  (PDF — {len(pdf.pages)} page(s))\n\n{full}"
    except ImportError:
        pass

    try:
        import PyPDF2
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            pages = []
            for i, page in enumerate(reader.pages[:30]):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append(f"--- Page {i+1} ---\n{text}")
        full = "\n\n".join(pages)
        return f"FILE: {name}  (PDF)\n\n{full}"
    except ImportError:
        pass

    return (
        f"FILE: {name}  (PDF)\n"
        "[NOTE: PDF text extraction unavailable. "
        "Install pdfplumber: pip install pdfplumber]\n"
        "Please describe the PDF content or paste relevant sections as text."
    )


# ── Plain text / markdown ──────────────────────────────────────────────────────

def _text_to_text(filepath: str) -> str:
    name = Path(filepath).name
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            content = f.read()
        return f"FILE: {name}\n\n{content}"
    except Exception as e:
        return f"FILE: {name}\n[ERROR: {e}]"


# ── Images ────────────────────────────────────────────────────────────────────

def _image_note(filepath: str) -> str:
    name = Path(filepath).name
    return (
        f"FILE: {name}  (Image — {Path(filepath).suffix.upper()})\n"
        "[Image files cannot be parsed as text. "
        "Please describe the schematic/diagram content, "
        "or list the components and connections visible in the image.]"
    )


# ── Public API ─────────────────────────────────────────────────────────────────

EXTENSION_MAP = {
    ".xlsx": _excel_to_text,
    ".xls":  _excel_to_text,
    ".xlsm": _excel_to_text,
    ".csv":  _csv_to_text,
    ".pdf":  _pdf_to_text,
    ".txt":  _text_to_text,
    ".md":   _text_to_text,
    ".rst":  _text_to_text,
    ".json": _text_to_text,
    ".png":  _image_note,
    ".jpg":  _image_note,
    ".jpeg": _image_note,
    ".bmp":  _image_note,
    ".tiff": _image_note,
    ".svg":  _text_to_text,   # SVG is XML — readable
}


def file_to_context(filepath: str) -> str:
    """Convert any supported file to a text context string."""
    ext = Path(filepath).suffix.lower()
    handler = EXTENSION_MAP.get(ext)
    if handler:
        return handler(filepath)
    # Attempt generic text read
    try:
        return _text_to_text(filepath)
    except Exception:
        return f"FILE: {Path(filepath).name}  (unsupported format: {ext})"


def summarise_files(file_contexts: list[str]) -> str:
    """Join multiple file contexts with clear separators."""
    if not file_contexts:
        return "(No files uploaded)"
    separator = "\n" + "═" * 70 + "\n"
    return separator.join(file_contexts)
