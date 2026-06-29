#!/usr/bin/env python3
"""
orchestrator.py — Engineering Documentation Orchestrator

Systematic 5-phase workflow:

  Phase 1 : Collect user description + upload files
  Phase 2 : Parse files (Excel/CSV/PDF) → structured text
  Phase 3 : Multi-turn Haiku 4.5 triage — Q&A until full component clarity
  Phase 4 : Opus full engineering workflow → connection table + diagram code
  Phase 5 : Render diagrams (schemdraw / matplotlib)
  Phase 6 : Assemble PDF + docx with embedded diagrams

Usage:
  python orchestrator.py
  python orchestrator.py --project "TestRig-CU1" --files "wiring.xlsx"
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Local modules
from auth import verify_claude_auth
from file_parser import file_to_context, summarise_files
from triage import run_triage
from diagram_engine import render_diagrams, successful_diagrams
from doc_builder import build_pdf, build_docx

# ── Model config ───────────────────────────────────────────────────────────────

HAIKU_MODEL = os.getenv("HAIKU_MODEL",   "claude-haiku-4-5-20251001")
OPUS_MODEL  = os.getenv("OPUS_MODEL",    "claude-opus-4-7")
OUTPUT_DIR  = os.getenv("OUTPUT_FOLDER", "./outputs")

# ── Claude CLI call ────────────────────────────────────────────────────────────

def call_claude(prompt: str, system: str, model: str, label: str) -> str:
    cmd = [
        "claude", "-p", prompt,
        "--model",         model,
        "--system-prompt", system,
        "--output-format", "text",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=360)
        if result.returncode != 0:
            print(f"  [{label}] CLI error:\n{result.stderr.strip()}")
            return ""
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  [{label}] Timed out after 6 minutes.")
        return ""
    except FileNotFoundError:
        print("  ERROR: 'claude' CLI not found. Ensure Claude Code is installed and on PATH.")
        sys.exit(1)


# ── Opus system prompt ─────────────────────────────────────────────────────────

OPUS_SYSTEM = """You are an expert hardware engineer and technical documentarian specialising in:
  • Electrical schematics (IEC 60617, ANSI/IEEE, NEMA)
  • Wiring diagrams, block diagrams, connection tables
  • schemdraw Python library — generate precise IEC-compliant electrical schematics
  • matplotlib / FixtureDiagrammer — generate block / system architecture diagrams
  • Adversarial source review — never invent data; flag all ambiguities as [VERIFY]

════════════════════════════════════════════════════════════════
REQUIRED OUTPUT STRUCTURE — PRODUCE ALL SECTIONS IN ORDER
════════════════════════════════════════════════════════════════

## 1. Project Overview
Brief description of the system, scope, and document purpose.

## 2. System Description
Describe each subsystem, its function, and how subsystems interconnect.

## 3. Component List
Tabular component register:

| Ref | Type | Description | Manufacturer | Part No. | Ratings | Standard |
|-----|------|-------------|--------------|----------|---------|---------|

## 4. Connection Table
Complete From → Via → To table:

| From | Via | To | Signal | Wire Spec | Notes |
|------|-----|----|--------|-----------|-------|

Include every connection. Mark uncertain entries [VERIFY].

## 5. Adversarial Review
List every ambiguity, potential error, or missing data item found.
Mark each: [VERIFY] <item> — <reason>

## 6. Diagram Code
For EACH diagram, output a Python code block with this header comment:

For schematics (schemdraw):
```python
# DIAGRAM: <diagram_name> | TYPE: schemdraw | OUTPUT: <name>.svg
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(show=False) as d:
    # ... schemdraw elements ...
    d.save(OUTPUT_DIR + "/<name>.svg")
```

For block diagrams (matplotlib / FixtureDiagrammer):
```python
# DIAGRAM: <diagram_name> | TYPE: matplotlib | OUTPUT: <name>.png
import sys
sys.path.insert(0, "./scripts")
from fixture_diagrammer import FixtureDiagrammer

diag = FixtureDiagrammer(width=14, height=10, title="<title>")
# ... add_block / draw_connection calls ...
diag.save(OUTPUT_DIR + "/<name>.png")
```

Rules for diagram code:
  • Always use OUTPUT_DIR variable (injected at runtime) for save paths.
  • Use show=False for schemdraw drawings (no GUI pop-up).
  • Code must be self-contained and executable with standard library + schemdraw/matplotlib.
  • Use actual component values from the triage data — no placeholders.
  • Draw to IEC 60617 conventions unless triage specifies otherwise.
  • Produce at minimum: one block/system overview diagram + one detailed schematic.

## 7. Document Sections
### 7.1 Diagram Descriptions
Describe what each diagram shows and how to read it.

### 7.2 Signal Conventions
List signal types used, their colour/style conventions in the diagrams.

### 7.3 Verification Items
Numbered list of all [VERIFY] items from Section 5 and the diagrams.

### 7.4 Next Steps
What the engineer must verify, test, or complete before the document is final.
"""


# ── Phase 4: Opus engineering ──────────────────────────────────────────────────

def phase_opus(user_description: str, triage_data: dict, project_name: str) -> dict:
    print("\n" + "═" * 70)
    print("  PHASE 4 — Full Engineering Workflow (Opus)")
    print("═" * 70)
    print("  Running Opus... (allow 2–5 minutes for complex schematics)")

    prompt = f"""PROJECT: {project_name}
{"═"*70}

USER DESCRIPTION:
{user_description}

{"═"*70}
TRIAGE DATA (fully verified — use these values exactly):
{json.dumps(triage_data, indent=2)}
{"═"*70}

Execute the full engineering documentation workflow.
Follow the REQUIRED OUTPUT STRUCTURE exactly.
All diagram code must use the OUTPUT_DIR variable (set at runtime) for file paths.
"""

    response = call_claude(prompt, OPUS_SYSTEM, OPUS_MODEL, "Opus")
    if not response:
        return {"status": "error", "error": "No response from Opus"}

    # Save raw Opus output for reference
    return {"status": "success", "response": response, "model": OPUS_MODEL}


# ── Collect file inputs ────────────────────────────────────────────────────────

def _collect_files_interactive() -> list[str]:
    """Prompt user for file paths and parse them. Returns list of context strings."""
    print("\n  Upload files? (Excel, CSV, PDF, images, text)")
    print("  Enter one file path per line. Press Enter with no input when done.")
    print("  Tip: drag the file into the terminal to paste its path.\n")

    contexts = []
    while True:
        raw = input("  File path: ").strip().strip('"').strip("'")
        if not raw:
            break
        if not os.path.exists(raw):
            print(f"  ✗ Not found: {raw}")
            continue
        print(f"  Parsing {Path(raw).name}...")
        ctx = file_to_context(raw)
        contexts.append(ctx)
        print(f"  ✓ Parsed  ({len(ctx):,} chars)")
    return contexts


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Engineering Documentation Orchestrator"
    )
    parser.add_argument("--project", help="Project name (skip interactive prompt)")
    parser.add_argument("--files",   nargs="*", help="File paths to parse upfront")
    args = parser.parse_args()

    # Auth check
    verify_claude_auth()

    print()
    print("╔" + "═"*68 + "╗")
    print("║  ENGINEERING DOCUMENTATION ORCHESTRATOR                          ║")
    print("║  Haiku 4.5 (triage) → Opus (engineering) → PDF + docx + diagrams║")
    print("╚" + "═"*68 + "╝")

    # ── Phase 1: Collect description ────────────────────────────────────────────
    print("\n" + "─"*70)
    print("  PHASE 1 — Project Description")
    print("─"*70)
    print("  Describe your engineering task.")
    print("  Include: what you have (sketches, tables, specs), what you need.")
    print("  Type your description, then type 'done' on its own line.\n")

    lines = []
    try:
        while True:
            line = input("  > ")
            if line.strip().lower() == "done":
                break
            lines.append(line)
    except EOFError:
        lines = sys.stdin.readlines()

    user_description = "\n".join(lines).strip()
    if not user_description:
        print("  No description provided. Exiting.")
        sys.exit(0)

    # ── Phase 2: Parse files ────────────────────────────────────────────────────
    print("\n" + "─"*70)
    print("  PHASE 2 — File Parsing")
    print("─"*70)

    file_contexts = []
    if args.files:
        for fp in args.files:
            if os.path.exists(fp):
                ctx = file_to_context(fp)
                file_contexts.append(ctx)
                print(f"  ✓ Parsed: {Path(fp).name} ({len(ctx):,} chars)")
    else:
        file_contexts = _collect_files_interactive()

    if not file_contexts:
        print("  (No files uploaded — proceeding with description only)")

    # ── Phase 3: Project name ───────────────────────────────────────────────────
    if args.project:
        project_name = args.project
    else:
        project_name = input("\n  Project name (e.g., 'TestRig-CU1'): ").strip()
    if not project_name:
        project_name = f"Engineering-{datetime.now().strftime('%Y%m%d_%H%M')}"

    # ── Phase 3: Multi-turn triage ──────────────────────────────────────────────
    print("\n" + "═"*70)
    print("  PHASE 3 — Component Triage (Haiku 4.5 — multi-turn Q&A)")
    print("═"*70)
    print("  Haiku will analyse your submission and ask clarifying questions.")
    print("  Answer each round until Haiku signals it has full clarity.\n")

    haiku_fn = lambda prompt, system: call_claude(prompt, system, HAIKU_MODEL, "Haiku")

    triage_data = run_triage(
        user_description=user_description,
        file_contexts=file_contexts,
        call_claude_fn=haiku_fn,
    )

    # ── Confirm before Opus ─────────────────────────────────────────────────────
    print("\n" + "─"*70)
    proceed = input("  Proceed with Opus engineering workflow? (yes/no): ").strip().lower()
    if proceed not in ("yes", "y"):
        print("  Workflow cancelled.")
        sys.exit(0)

    # ── Phase 4: Opus ───────────────────────────────────────────────────────────
    opus_result = phase_opus(user_description, triage_data, project_name)
    if opus_result.get("status") != "success":
        print(f"\n  ✗ Opus failed: {opus_result.get('error')}")
        sys.exit(1)

    opus_text = opus_result["response"]

    # ── Create output folder ────────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_dir   = os.path.join(OUTPUT_DIR, f"{project_name}_{timestamp}")
    os.makedirs(out_dir, exist_ok=True)

    # Save raw Opus output
    raw_path = os.path.join(out_dir, "opus_raw_output.md")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(f"# Opus Raw Output — {project_name}\n")
        f.write(f"Generated: {timestamp}\n\n")
        f.write(opus_text)

    # Save triage JSON
    triage_path = os.path.join(out_dir, "triage_data.json")
    with open(triage_path, "w", encoding="utf-8") as f:
        json.dump(triage_data, f, indent=2)

    # ── Phase 5: Render diagrams ────────────────────────────────────────────────
    print("\n" + "═"*70)
    print("  PHASE 5 — Diagram Rendering (schemdraw / matplotlib)")
    print("═"*70)

    diagram_results = render_diagrams(opus_text, out_dir)

    # ── Phase 6: Build documents ────────────────────────────────────────────────
    print("\n" + "═"*70)
    print("  PHASE 6 — Document Assembly (PDF + docx)")
    print("═"*70)

    pdf_path  = build_pdf( project_name, triage_data, opus_text, diagram_results, out_dir)
    docx_path = build_docx(project_name, triage_data, opus_text, diagram_results, out_dir)

    # ── Summary ─────────────────────────────────────────────────────────────────
    ok_diagrams = successful_diagrams(diagram_results)
    print()
    print("╔" + "═"*68 + "╗")
    print("║  WORKFLOW COMPLETE                                               ║")
    print("╠" + "═"*68 + "╣")
    print(f"║  Project    : {project_name:<52} ║")
    print(f"║  Output dir : {out_dir:<52} ║")
    print(f"║  Diagrams   : {len(ok_diagrams)} rendered                                          ║")
    print(f"║  PDF        : {Path(pdf_path).name if pdf_path else 'not built':<52} ║")
    print(f"║  Word doc   : {Path(docx_path).name if docx_path else 'not built':<52} ║")
    print("╚" + "═"*68 + "╝")

    verify_items = triage_data.get("verify_items", [])
    if verify_items:
        print(f"\n  ⚠  {len(verify_items)} items need verification before this doc is final.")
        for v in verify_items[:5]:
            print(f"    • {v}")
        if len(verify_items) > 5:
            print(f"    ... and {len(verify_items)-5} more (see PDF Section 7.3)")


if __name__ == "__main__":
    main()
