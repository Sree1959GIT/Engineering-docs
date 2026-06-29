"""
triage.py — Multi-turn Haiku triage engine.

Haiku reads all uploaded files + user description, asks targeted clarifying
questions in rounds, and loops until it has FULL component/symbol clarity
before handing a structured triage dict to Opus.
"""

import json
import re
import sys
from typing import Callable

# ── System prompt ──────────────────────────────────────────────────────────────

TRIAGE_SYSTEM = """You are an expert engineering documentation triage specialist with deep
knowledge of:
  • Electrical/electronic schematics and wiring diagrams
  • IEC 60617, ANSI/IEEE, NEMA, and manufacturer-specific symbol standards
  • Industrial fixture, panel, and system documentation
  • Component identification, manufacturer lookup, and BOM interpretation
  • Drawing tools: schemdraw (IEC schematics), matplotlib (block/system diagrams),
    SVG custom (layout/harness diagrams), KiCad (PCB-level)

════════════════════════════════════════════════════════════════
YOUR WORKFLOW — FOLLOW STRICTLY
════════════════════════════════════════════════════════════════

STEP 1 — DEEP ANALYSIS (every first round)
  a) Parse ALL submitted files thoroughly: Excel tabs, CSV rows, PDFs, text.
  b) Identify EVERY component referenced (relays, MCBs, contactors, sensors,
     terminals, connectors, fuses, motors, instruments, PLC I/O, etc.).
  c) For each component note what is KNOWN vs UNKNOWN:
       Known: reference designator, rough type, any specs in the data.
       Unknown: manufacturer, part number, exact ratings, contact config,
                wiring standard, pin/terminal numbering.
  d) Map out all connections you can infer (From → Via → To).
  e) Identify what document type is needed and which drawing standard applies.
  f) Identify what is still ambiguous or missing.

STEP 2 — ASK GROUPED CLARIFYING QUESTIONS (until all unknowns resolved)
  Group questions by category. Be specific — quote reference designators.
  Do NOT ask one question at a time. Group related questions together.
  Suggest plausible answers where you can (e.g., "Is K1 a Finder 40.31 or similar
  SPDT relay? Please confirm or correct").
  If many components are unknown, ASK the user to upload a BOM.
  If a component has a known part number, state the assumed standard symbol
  and ask the user to confirm rather than asking from scratch.

STEP 3 — SIGNAL READY when ALL of these are confirmed:
  ✓ Every component has: type, manufacturer/part (or confirmed assumption),
    electrical ratings, symbol convention.
  ✓ All connections are mapped: From, Via, To, signal type, wire spec (if known).
  ✓ Document type and drawing standard are confirmed.
  ✓ Output formats are confirmed (PDF, docx, SVG, etc.).
  ✓ No [UNRESOLVED] items remain.

════════════════════════════════════════════════════════════════
OUTPUT FORMAT — USE EXACTLY
════════════════════════════════════════════════════════════════

While clarifying, output ONLY this JSON (no prose before/after):

{
  "status": "NEEDS_CLARIFICATION",
  "round": <integer>,
  "analysis": {
    "document_type": "schematic | block_diagram | wiring_harness | layout | mixed",
    "standard": "IEC 60617 | ANSI/IEEE | NEMA | custom | TBD",
    "diagram_tool": "schemdraw | matplotlib | svg_custom | mixed",
    "identified_components": [
      {
        "ref": "K1",
        "type": "relay",
        "description": "5A SPDT relay",
        "manufacturer": "unknown",
        "part_number": "unknown",
        "coil_voltage": "unknown",
        "contacts": "unknown",
        "symbol_standard": "IEC 60617",
        "confidence": "low | medium | high"
      }
    ],
    "identified_connections": [
      {
        "from": "TB1.1",
        "via": "K1 coil",
        "to": "TB1.2",
        "signal": "24VDC control",
        "wire_spec": "unknown",
        "confidence": "low | medium | high"
      }
    ],
    "unresolved_items": ["list every gap that still blocks documentation"],
    "bom_available": false
  },
  "questions": [
    {
      "group": "Group label (e.g., Component Specs — Relays)",
      "items": [
        "Specific, quoted question referencing the designator and why it matters"
      ]
    }
  ],
  "can_proceed_with_assumptions": false,
  "assumptions_if_proceeding": []
}

When ready (ALL unknowns resolved or user accepted assumptions), output ONLY:

{
  "status": "READY",
  "document_type": "schematic | block_diagram | wiring_harness | layout | mixed",
  "standard": "IEC 60617 | ANSI/IEEE | NEMA | custom",
  "diagram_tool": "schemdraw | matplotlib | svg_custom | mixed",
  "output_formats": ["pdf", "docx", "svg"],
  "components": [
    {
      "ref": "K1",
      "type": "relay",
      "description": "Finder 40.31 SPDT relay",
      "manufacturer": "Finder",
      "part_number": "40.31.9.024.0010",
      "coil_voltage": "24VDC",
      "contacts": "SPDT 10A",
      "symbol_standard": "IEC 60617",
      "notes": ""
    }
  ],
  "connections": [
    {
      "from": "GCF.TB1.1",
      "via": "K1-A1/A2",
      "to": "GCF.TB1.2",
      "signal": "24VDC control",
      "wire_spec": "0.5mm² red",
      "notes": ""
    }
  ],
  "assumptions": ["list any assumed values accepted by user"],
  "verify_items": ["list any [VERIFY] flags for Opus to double-check"],
  "project_scope": "one-paragraph description of what will be produced",
  "complexity": "low | medium | high",
  "estimated_diagrams": 2
}

RULES:
  • Output ONLY valid JSON. No text before or after the JSON block.
  • Never invent specs. Mark unknowns as "unknown" and ask.
  • If user says 'proceed with assumptions', list all assumptions in
    `assumptions_if_proceeding` and set `can_proceed_with_assumptions: true`.
  • Ask for BOM upload if >3 components have unknown manufacturer/part.
  • Maximum rounds before offering assumption-based proceed: 4.
"""

# ── Helpers ────────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> dict | None:
    """Extract the first valid JSON object from a text response."""
    # Try raw parse first
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    # Find first {...} block
    start = text.find("{")
    end   = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    return None


def _print_analysis(data: dict, round_num: int) -> None:
    """Pretty-print Haiku's analysis to the terminal."""
    analysis = data.get("analysis", {})
    components = analysis.get("identified_components", [])
    connections = analysis.get("identified_connections", [])
    unresolved  = analysis.get("unresolved_items", [])

    print(f"\n  Document type : {analysis.get('document_type', '?')}")
    print(f"  Standard      : {analysis.get('standard', '?')}")
    print(f"  Drawing tool  : {analysis.get('diagram_tool', '?')}")

    if components:
        print(f"\n  Components identified ({len(components)}):")
        for c in components:
            conf  = c.get("confidence", "?")
            mfr   = c.get("manufacturer", "unknown")
            pn    = c.get("part_number",  "unknown")
            print(f"    [{conf:6}] {c['ref']:8} {c['type']:15} {c['description'][:40]}")
            if mfr != "unknown":
                print(f"             ↳ {mfr} {pn}")

    if connections:
        print(f"\n  Connections identified ({len(connections)}):")
        for cn in connections[:10]:
            print(f"    {cn.get('from','?'):15} → {cn.get('via','direct'):20} → {cn.get('to','?')}")
        if len(connections) > 10:
            print(f"    ... and {len(connections)-10} more")

    if unresolved:
        print(f"\n  Still unresolved ({len(unresolved)}):")
        for item in unresolved:
            print(f"    ✗ {item}")


def _print_questions(questions: list) -> None:
    """Print Haiku's clarifying questions."""
    print()
    for q_group in questions:
        group = q_group.get("group", "Questions")
        items = q_group.get("items", [])
        print(f"  ┌─ {group} {'─'*max(0, 55-len(group))}┐")
        for i, item in enumerate(items, 1):
            # Word-wrap at 70 chars
            words = item.split()
            line = f"  │ {i}. "
            for word in words:
                if len(line) + len(word) > 75:
                    print(line)
                    line = "  │    " + word + " "
                else:
                    line += word + " "
            if line.strip():
                print(line)
        print("  └" + "─" * 57 + "┘")


# ── Main triage loop ───────────────────────────────────────────────────────────

def run_triage(
    user_description: str,
    file_contexts: list,
    call_claude_fn: Callable[[str, str], str],
    max_rounds: int = 6,
) -> dict:
    """
    Run multi-turn Haiku triage until READY or user accepts assumptions.

    Returns the final READY triage dict for Opus.
    """
    # Build the initial context block
    file_block = ""
    if file_contexts:
        file_block = "\n\n" + ("═" * 70) + "\nUPLOADED FILES:\n" + ("═" * 70) + "\n"
        file_block += ("\n" + "─" * 70 + "\n").join(file_contexts)

    # Accumulated Q&A history (grows each round)
    qa_history = ""
    round_num  = 0

    initial_prompt = f"""ENGINEERING DOCUMENTATION REQUEST
{"═"*70}
USER DESCRIPTION:
{user_description}
{file_block}
{"═"*70}

Analyse all material above thoroughly and begin the triage process.
"""

    current_prompt = initial_prompt

    while round_num < max_rounds:
        round_num += 1
        print(f"\n{'─'*70}")
        print(f"  HAIKU TRIAGE — Round {round_num}")
        print(f"{'─'*70}")
        print("  Analysing... (this may take 15–30 seconds)")

        response_text = call_claude_fn(current_prompt, TRIAGE_SYSTEM)
        if not response_text:
            print("  [ERROR] No response from Haiku. Retrying may help.")
            break

        triage_data = _extract_json(response_text)
        if not triage_data:
            print("  [WARNING] Could not parse Haiku's JSON response.")
            print("  Raw response:")
            print(response_text[:800])
            # Give user option to continue or abort
            choice = input("\n  Type 'retry' to resend, or 'abort' to stop: ").strip().lower()
            if choice == "abort":
                sys.exit(0)
            continue

        status = triage_data.get("status", "").upper()

        # ── READY ──────────────────────────────────────────────────────────────
        if status == "READY":
            print("\n  ✓ TRIAGE COMPLETE — Haiku has full component clarity.")
            _print_summary(triage_data)
            return triage_data

        # ── NEEDS CLARIFICATION ────────────────────────────────────────────────
        if status == "NEEDS_CLARIFICATION":
            _print_analysis(triage_data, round_num)
            questions = triage_data.get("questions", [])
            can_assume = triage_data.get("can_proceed_with_assumptions", False)
            assumptions = triage_data.get("assumptions_if_proceeding", [])

            if questions:
                print(f"\n  Haiku needs clarification on the following:")
                _print_questions(questions)
            else:
                print("\n  No further questions — asking Haiku to finalise.")

            # Offer assumption path after round 3
            if round_num >= 3 and can_assume and assumptions:
                print("\n  ─── Assumption-based proceed available ───────────────────")
                print("  Haiku can proceed with these assumptions:")
                for a in assumptions:
                    print(f"    • {a}")
                print()
                assume_choice = input("  Proceed with these assumptions? (yes/no): ").strip().lower()
                if assume_choice in ("yes", "y"):
                    # Ask Haiku to emit READY with assumptions
                    finalize_prompt = (
                        current_prompt + qa_history +
                        "\n\nUSER DECISION: Proceed with all listed assumptions. "
                        "Mark assumed values clearly. Emit the READY JSON now."
                    )
                    print("\n  Finalising triage with assumptions...")
                    resp2 = call_claude_fn(finalize_prompt, TRIAGE_SYSTEM)
                    final = _extract_json(resp2)
                    if final and final.get("status", "").upper() == "READY":
                        print("\n  ✓ TRIAGE COMPLETE (with assumptions).")
                        _print_summary(final)
                        return final

            # Collect user answers
            if questions:
                print("\n  Your answers (press Enter twice when done):\n")
                answer_lines = []
                blank_count  = 0
                while blank_count < 2:
                    line = input("  > ")
                    if line.strip() == "":
                        blank_count += 1
                    else:
                        blank_count = 0
                        answer_lines.append(line)
                user_answers = "\n".join(answer_lines).strip()
            else:
                user_answers = "(No questions — please finalise.)"

            # Build next prompt: append history
            qa_entry = (
                f"\n\n{'═'*70}\n"
                f"TRIAGE ROUND {round_num} — USER ANSWERS:\n"
                f"{'═'*70}\n"
                f"{user_answers}\n"
            )
            qa_history  += qa_entry
            current_prompt = initial_prompt + qa_history

        else:
            # Unexpected status — treat as raw text answer
            print(f"\n  [Unexpected response status: {status}]")
            print(f"  Raw: {response_text[:400]}")
            break

    # ── Max rounds reached ─────────────────────────────────────────────────────
    print(f"\n  Maximum rounds ({max_rounds}) reached.")
    print("  Options:")
    print("    1. Continue with whatever Haiku resolved (partial data)")
    print("    2. Abort")
    choice = input("\n  Choose (1/2): ").strip()
    if choice == "2":
        sys.exit(0)

    # Return last known triage (best effort)
    return triage_data if triage_data else {"status": "PARTIAL", "error": "Triage incomplete"}


# ── Summary printer ────────────────────────────────────────────────────────────

def _print_summary(data: dict) -> None:
    print(f"\n  Document type  : {data.get('document_type', '?')}")
    print(f"  Standard       : {data.get('standard', '?')}")
    print(f"  Tool           : {data.get('diagram_tool', '?')}")
    print(f"  Output formats : {', '.join(data.get('output_formats', ['pdf','docx']))}")
    print(f"  Complexity     : {data.get('complexity', '?')}")
    print(f"  Est. diagrams  : {data.get('estimated_diagrams', '?')}")

    components = data.get("components", [])
    if components:
        print(f"\n  Components ({len(components)}):")
        for c in components:
            print(f"    {c['ref']:8} {c['type']:15} {c.get('manufacturer','')[:20]:20} {c['description'][:35]}")

    verify = data.get("verify_items", [])
    if verify:
        print(f"\n  [VERIFY] items for Opus ({len(verify)}):")
        for v in verify:
            print(f"    ⚠ {v}")

    assumptions = data.get("assumptions", [])
    if assumptions:
        print(f"\n  Assumptions accepted ({len(assumptions)}):")
        for a in assumptions:
            print(f"    ~ {a}")
