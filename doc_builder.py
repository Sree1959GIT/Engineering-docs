"""
doc_builder.py — Assemble PDF and docx engineering documentation packages.

PDF  : reportlab (pure-Python, Windows-friendly)
docx : python-docx

Both outputs embed:
  • Cover page with project metadata
  • Triage summary (components table, connections table)
  • Opus engineering narrative (parsed into sections)
  • Rendered diagrams (SVG→PNG converted for PDF; PNG/SVG for docx)
  • Verification checklist
  • Assumptions log
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# ── Section parser ─────────────────────────────────────────────────────────────

_HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)
_TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")


def _parse_sections(text: str) -> list[dict]:
    """
    Split Opus markdown output into sections.
    Returns: [{"heading": str, "body": str}]
    """
    sections = []
    parts = re.split(r"(?m)^(#{1,3}\s+.+)$", text)
    # parts alternates: pre-heading text, heading, body, heading, body ...
    if parts[0].strip():
        sections.append({"heading": "Overview", "body": parts[0].strip()})
    i = 1
    while i < len(parts) - 1:
        heading = parts[i].lstrip("#").strip()
        body    = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections.append({"heading": heading, "body": body})
        i += 2
    if not sections:
        sections = [{"heading": "Engineering Documentation", "body": text}]
    return sections


def _markdown_tables(text: str) -> list[list[list[str]]]:
    """Extract all markdown tables from text. Returns list of tables (list of rows)."""
    tables = []
    current_table = []
    for line in text.splitlines():
        if _TABLE_ROW_RE.match(line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            current_table.append(cells)
        else:
            if len(current_table) > 1:
                # Drop separator row (---)
                clean = [r for r in current_table if not all(re.match(r"^[-:]+$", c) for c in r)]
                if len(clean) > 1:
                    tables.append(clean)
            current_table = []
    if len(current_table) > 1:
        clean = [r for r in current_table if not all(re.match(r"^[-:]+$", c) for c in r)]
        if len(clean) > 1:
            tables.append(clean)
    return tables


# ── SVG → PNG conversion (for PDF embedding) ──────────────────────────────────

def _svg_to_png(svg_path: str) -> str | None:
    """Convert SVG to PNG using cairosvg or svglib. Returns PNG path or None."""
    png_path = str(Path(svg_path).with_suffix(".png"))
    # Try cairosvg
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path, scale=2.0)
        return png_path
    except ImportError:
        pass
    except Exception:
        pass
    # Try svglib + reportlab
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        drawing = svg2rlg(svg_path)
        if drawing:
            renderPM.drawToFile(drawing, png_path, fmt="PNG")
            return png_path
    except ImportError:
        pass
    except Exception:
        pass
    return None


def _resolve_image_path(path: str) -> str | None:
    """Return a PDF-embeddable image path (PNG/JPEG). Convert SVG if needed."""
    if not path or not os.path.exists(path):
        return None
    ext = Path(path).suffix.lower()
    if ext in (".png", ".jpg", ".jpeg"):
        return path
    if ext == ".svg":
        png = _svg_to_png(path)
        return png  # may be None if conversion failed
    return None


# ══════════════════════════════════════════════════════════════════════════════
# PDF (reportlab)
# ══════════════════════════════════════════════════════════════════════════════

def build_pdf(
    project_name: str,
    triage_data: dict,
    opus_text: str,
    diagram_results: list[dict],
    output_dir: str,
) -> str:
    """Build a professional PDF. Returns path to PDF file."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm, cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, Image, HRFlowable,
        )
        from reportlab.platypus.flowables import KeepTogether
    except ImportError:
        print("  [PDF] reportlab not installed — skipping PDF. Run: pip install reportlab")
        return ""

    pdf_path = os.path.join(output_dir, f"{project_name.replace(' ', '_')}_Engineering.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=25*mm,  bottomMargin=20*mm,
        title=f"Engineering Documentation: {project_name}",
        author="Engineering Documentation Orchestrator",
    )

    styles = getSampleStyleSheet()
    W, H = A4

    # Custom styles
    def style(name, **kw):
        base = styles.get(name, styles["Normal"])
        return ParagraphStyle(name + "_custom", parent=base, **kw)

    S = {
        "title":    style("Title",   fontSize=22, textColor=colors.HexColor("#003366"),
                          spaceAfter=6),
        "subtitle": style("Normal",  fontSize=12, textColor=colors.HexColor("#336699"),
                          spaceAfter=4),
        "h1":       style("Heading1", fontSize=14, textColor=colors.HexColor("#003366"),
                          spaceBefore=12, spaceAfter=4),
        "h2":       style("Heading2", fontSize=12, textColor=colors.HexColor("#336699"),
                          spaceBefore=8, spaceAfter=3),
        "body":     style("Normal",  fontSize=9,  leading=13, spaceAfter=6),
        "mono":     style("Code",    fontSize=8,  leading=11, fontName="Courier",
                          spaceAfter=4),
        "caption":  style("Normal",  fontSize=8,  textColor=colors.grey, spaceAfter=8),
        "verify":   style("Normal",  fontSize=9,  textColor=colors.HexColor("#CC0000"),
                          spaceAfter=3),
    }

    story = []
    ts_cover = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Cover page ──────────────────────────────────────────────────────────────
    story += [
        Spacer(1, 40*mm),
        Paragraph(project_name, S["title"]),
        Paragraph("Engineering Documentation Package", S["subtitle"]),
        HRFlowable(width="100%", thickness=2, color=colors.HexColor("#003366")),
        Spacer(1, 4*mm),
        Paragraph(f"Generated: {ts_cover}", S["body"]),
        Paragraph(f"Document type: {triage_data.get('document_type','N/A')}", S["body"]),
        Paragraph(f"Standard: {triage_data.get('standard','N/A')}", S["body"]),
        Paragraph(f"Drawing tool: {triage_data.get('diagram_tool','N/A')}", S["body"]),
        Paragraph(f"Complexity: {triage_data.get('complexity','N/A')}", S["body"]),
        Spacer(1, 6*mm),
        Paragraph(triage_data.get("project_scope", ""), S["body"]),
        PageBreak(),
    ]

    # ── Components table ────────────────────────────────────────────────────────
    components = triage_data.get("components", [])
    if components:
        story.append(Paragraph("Component Register", S["h1"]))
        headers = ["Ref", "Type", "Description", "Manufacturer", "Part No.", "Standard"]
        col_w = [(W-40*mm) * f for f in [0.07, 0.10, 0.28, 0.18, 0.20, 0.17]]
        rows = [headers]
        for c in components:
            rows.append([
                c.get("ref", ""),
                c.get("type", ""),
                c.get("description", ""),
                c.get("manufacturer", ""),
                c.get("part_number", ""),
                c.get("symbol_standard", ""),
            ])
        t = Table(rows, colWidths=col_w, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTSIZE",   (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F7")]),
            ("GRID",       (0, 0), (-1, -1), 0.5, colors.HexColor("#AAAAAA")),
            ("VALIGN",     (0, 0), (-1, -1), "TOP"),
            ("PADDING",    (0, 0), (-1, -1), 4),
        ]))
        story += [t, Spacer(1, 6*mm)]

    # ── Connection table ────────────────────────────────────────────────────────
    connections = triage_data.get("connections", [])
    if connections:
        story.append(Paragraph("Connection Table", S["h1"]))
        headers = ["From", "Via", "To", "Signal", "Wire Spec", "Notes"]
        col_w = [(W-40*mm) * f for f in [0.17, 0.17, 0.17, 0.18, 0.15, 0.16]]
        rows = [headers]
        for cn in connections:
            rows.append([
                cn.get("from", ""), cn.get("via", ""), cn.get("to", ""),
                cn.get("signal", ""), cn.get("wire_spec", ""), cn.get("notes", ""),
            ])
        t = Table(rows, colWidths=col_w, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTSIZE",   (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F7")]),
            ("GRID",       (0, 0), (-1, -1), 0.5, colors.HexColor("#AAAAAA")),
            ("VALIGN",     (0, 0), (-1, -1), "TOP"),
            ("PADDING",    (0, 0), (-1, -1), 4),
        ]))
        story += [t, Spacer(1, 6*mm)]

    # ── Diagrams ────────────────────────────────────────────────────────────────
    diagram_paths = [_resolve_image_path(r["path"]) for r in diagram_results if r.get("success")]
    diagram_paths = [p for p in diagram_paths if p]

    if diagram_paths:
        story.append(PageBreak())
        story.append(Paragraph("Engineering Diagrams", S["h1"]))
        avail_w = W - 40*mm
        for img_path in diagram_paths:
            try:
                img = Image(img_path, width=avail_w, height=avail_w * 0.65, kind="proportional")
                caption = Paragraph(Path(img_path).stem, S["caption"])
                story += [KeepTogether([img, caption]), Spacer(1, 6*mm)]
            except Exception as e:
                story.append(Paragraph(f"[Image error: {img_path} — {e}]", S["body"]))

    # ── Opus narrative sections ─────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Engineering Analysis", S["h1"]))
    sections = _parse_sections(opus_text)
    for sec in sections:
        if sec["heading"] not in ("Engineering Documentation",):
            story.append(Paragraph(sec["heading"], S["h2"]))

        # Render body: detect tables vs. paragraphs
        body = sec["body"]
        tables = _markdown_tables(body)
        if tables:
            for tbl_rows in tables:
                if not tbl_rows:
                    continue
                n_cols = max(len(r) for r in tbl_rows)
                col_w = [(W - 40*mm) / n_cols] * n_cols
                t = Table(tbl_rows, colWidths=col_w, repeatRows=1)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#336699")),
                    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
                    ("FONTSIZE",   (0, 0), (-1, -1), 8),
                    ("GRID",       (0, 0), (-1, -1), 0.4, colors.grey),
                    ("PADDING",    (0, 0), (-1, -1), 3),
                ]))
                story += [t, Spacer(1, 4*mm)]
            # Print non-table paragraphs
            non_table = "\n".join(
                l for l in body.splitlines()
                if not _TABLE_ROW_RE.match(l) and not re.match(r"^\s*[-:]+\s*$", l)
            ).strip()
            if non_table:
                for para in non_table.split("\n\n"):
                    para = para.strip()
                    if para:
                        story.append(Paragraph(para.replace("\n", " "), S["body"]))
        else:
            for para in body.split("\n\n"):
                para = para.strip()
                if para:
                    style_key = "verify" if "[VERIFY]" in para else "body"
                    story.append(Paragraph(para.replace("\n", " "), S[style_key]))

    # ── Verification checklist ──────────────────────────────────────────────────
    verify_items = triage_data.get("verify_items", [])
    if verify_items:
        story += [PageBreak(), Paragraph("Verification Checklist", S["h1"])]
        for item in verify_items:
            story.append(Paragraph(f"☐  {item}", S["verify"]))

    # ── Assumptions log ─────────────────────────────────────────────────────────
    assumptions = triage_data.get("assumptions", [])
    if assumptions:
        story.append(Spacer(1, 8*mm))
        story.append(Paragraph("Assumptions Log", S["h1"]))
        for a in assumptions:
            story.append(Paragraph(f"~  {a}", S["body"]))

    # Build
    doc.build(story)
    print(f"  ✓ PDF saved: {pdf_path}")
    return pdf_path


# ══════════════════════════════════════════════════════════════════════════════
# DOCX (python-docx)
# ══════════════════════════════════════════════════════════════════════════════

def build_docx(
    project_name: str,
    triage_data: dict,
    opus_text: str,
    diagram_results: list[dict],
    output_dir: str,
) -> str:
    """Build a Word document. Returns path to docx file."""
    try:
        from docx import Document
        from docx.shared import Pt, Cm, RGBColor, Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
    except ImportError:
        print("  [docx] python-docx not installed — skipping. Run: pip install python-docx")
        return ""

    docx_path = os.path.join(output_dir, f"{project_name.replace(' ', '_')}_Engineering.docx")
    doc = Document()

    # ── Page margins ──────────────────────────────────────────────────────────
    for section in doc.sections:
        section.top_margin    = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def heading(text, level=1):
        p = doc.add_heading(text, level=level)
        return p

    def para(text, style="Normal", bold=False, italic=False, color=None):
        p = doc.add_paragraph(style=style)
        run = p.add_run(text)
        run.bold   = bold
        run.italic = italic
        if color:
            run.font.color.rgb = RGBColor(*color)
        return p

    def add_table(headers, rows, col_widths=None):
        n_cols = len(headers)
        t = doc.add_table(rows=1 + len(rows), cols=n_cols)
        t.style = "Table Grid"
        # Header row
        hdr_cells = t.rows[0].cells
        for i, h in enumerate(headers):
            hdr_cells[i].text = h
            run = hdr_cells[i].paragraphs[0].runs[0] if hdr_cells[i].paragraphs[0].runs else \
                  hdr_cells[i].paragraphs[0].add_run(h)
            run.bold = True
            run.font.size = Pt(9)
            # Header background
            tc = hdr_cells[i]._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"),   "clear")
            shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"),  "003366")
            tcPr.append(shd)
            # Header text colour
            rpr = OxmlElement("w:rPr")
            clr = OxmlElement("w:color")
            clr.set(qn("w:val"), "FFFFFF")
            rpr.append(clr)
        # Data rows
        for r_idx, row_data in enumerate(rows):
            cells = t.rows[r_idx + 1].cells
            for c_idx, cell_text in enumerate(row_data):
                if c_idx < n_cols:
                    cells[c_idx].text = str(cell_text)
                    for run in cells[c_idx].paragraphs[0].runs:
                        run.font.size = Pt(9)
        return t

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Cover page ─────────────────────────────────────────────────────────────
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(60)
    run = p.add_run(project_name)
    run.bold = True
    run.font.size = Pt(26)
    run.font.color.rgb = RGBColor(0, 51, 102)

    para("Engineering Documentation Package", bold=True)
    para(f"Generated: {ts}")
    para(f"Document type: {triage_data.get('document_type','N/A')}")
    para(f"Standard: {triage_data.get('standard','N/A')}")
    para(f"Drawing tool: {triage_data.get('diagram_tool','N/A')}")
    para(f"Complexity: {triage_data.get('complexity','N/A')}")

    scope = triage_data.get("project_scope", "")
    if scope:
        doc.add_paragraph()
        para(scope)

    doc.add_page_break()

    # ── Component register ─────────────────────────────────────────────────────
    components = triage_data.get("components", [])
    if components:
        heading("Component Register", 1)
        headers = ["Ref", "Type", "Description", "Manufacturer", "Part No.", "Standard"]
        rows = [[
            c.get("ref",""), c.get("type",""), c.get("description",""),
            c.get("manufacturer",""), c.get("part_number",""),
            c.get("symbol_standard",""),
        ] for c in components]
        add_table(headers, rows)
        doc.add_paragraph()

    # ── Connection table ───────────────────────────────────────────────────────
    connections = triage_data.get("connections", [])
    if connections:
        heading("Connection Table", 1)
        headers = ["From", "Via", "To", "Signal", "Wire Spec", "Notes"]
        rows = [[
            cn.get("from",""), cn.get("via",""), cn.get("to",""),
            cn.get("signal",""), cn.get("wire_spec",""), cn.get("notes",""),
        ] for cn in connections]
        add_table(headers, rows)
        doc.add_paragraph()

    # ── Diagrams ───────────────────────────────────────────────────────────────
    img_paths = []
    for r in diagram_results:
        if not r.get("success") or not r.get("path"):
            continue
        p = r["path"]
        ext = Path(p).suffix.lower()
        if ext in (".png", ".jpg", ".jpeg"):
            img_paths.append(p)
        elif ext == ".svg":
            png = _svg_to_png(p)
            if png:
                img_paths.append(png)

    if img_paths:
        doc.add_page_break()
        heading("Engineering Diagrams", 1)
        for img_path in img_paths:
            try:
                doc.add_picture(img_path, width=Inches(6.0))
                caption_p = doc.add_paragraph(Path(img_path).stem)
                caption_p.paragraph_format.space_after = Pt(12)
                caption_p.runs[0].italic = True
                caption_p.runs[0].font.size = Pt(9)
            except Exception as e:
                para(f"[Image error: {img_path} — {e}]")

    # ── Engineering narrative ──────────────────────────────────────────────────
    doc.add_page_break()
    heading("Engineering Analysis", 1)
    sections = _parse_sections(opus_text)
    for sec in sections:
        if sec["heading"] not in ("Engineering Documentation",):
            heading(sec["heading"], 2)
        body = sec["body"]
        tables = _markdown_tables(body)
        if tables:
            for tbl_rows in tables:
                if not tbl_rows:
                    continue
                headers_ = tbl_rows[0]
                data_    = tbl_rows[1:]
                add_table(headers_, data_)
                doc.add_paragraph()
            non_table = "\n".join(
                l for l in body.splitlines()
                if not _TABLE_ROW_RE.match(l) and not re.match(r"^\s*[-:]+\s*$", l)
            ).strip()
            if non_table:
                for p_text in non_table.split("\n\n"):
                    p_text = p_text.strip()
                    if p_text:
                        para(p_text.replace("\n", " "))
        else:
            for p_text in body.split("\n\n"):
                p_text = p_text.strip()
                if not p_text:
                    continue
                if "[VERIFY]" in p_text:
                    p_ = doc.add_paragraph()
                    run = p_.add_run(p_text.replace("\n", " "))
                    run.font.color.rgb = RGBColor(204, 0, 0)
                    run.font.size = Pt(9)
                else:
                    para(p_text.replace("\n", " "))

    # ── Verification checklist ─────────────────────────────────────────────────
    verify_items = triage_data.get("verify_items", [])
    if verify_items:
        doc.add_page_break()
        heading("Verification Checklist", 1)
        for item in verify_items:
            p_ = doc.add_paragraph(style="List Bullet")
            run = p_.add_run(f"☐  {item}")
            run.font.color.rgb = RGBColor(204, 0, 0)
            run.font.size = Pt(9)

    # ── Assumptions log ────────────────────────────────────────────────────────
    assumptions = triage_data.get("assumptions", [])
    if assumptions:
        heading("Assumptions Log", 1)
        for a in assumptions:
            p_ = doc.add_paragraph(style="List Bullet")
            p_.add_run(f"~  {a}").font.size = Pt(9)

    doc.save(docx_path)
    print(f"  ✓ Word doc saved: {docx_path}")
    return docx_path
