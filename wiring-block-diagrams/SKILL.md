---
name: wiring-block-diagrams
description: >-
  End-to-end builder for engineering electrical drawings: wiring diagrams, block/interconnect
  diagrams, control schematics, test-fixture / ATE harness maps, and connection/signal diagrams.
  Use this whenever the user wants to create, draft, redraw, clean up, or document electrical wiring
  or block diagrams — from handwritten sketches, photos, netlists, connection CSV/Excel, BOMs, or a
  plain description — and produce a documentation package with to-scale diagrams (proper relay,
  terminal, instrument and connector symbols), labels, and a written description of each block.
  Trigger even when the user only says "diagram my wiring", "draw the connections", "make a schematic
  from these notes", "block diagram of this system", or "turn this sketch into a proper drawing".
  Prefers free / open-source tools that run without paid services.
---

# Wiring & Block Diagram Builder

## Operating principle

Run the whole job, not just the drawing step: understand the goal → gather any reference docs and
inputs → **build a connection table that is the single source of truth** → **research/confirm what
each component actually is** → draft diagrams → review with the user → assemble a final document of
to-scale diagrams plus a description of each block.

Default to **open-source, in-sandbox tools** (matplotlib, schemdraw, Graphviz, SVG→Chromium→PDF,
python-docx). Only suggest paid/desktop software (EPLAN, AutoCAD Electrical, QElectroTech, KiCad,
draw.io) when the user needs an editable manufacturing-grade native file — and even then, produce the
connection table + a draft they can import. See `references/tools.md`.

The most common failure mode is **inventing detail that wasn't in the source** (a misread label, a
guessed wire length, a fabricated component). Treat the source adversarially: transcribe exactly,
flag anything unclear as `[VERIFY]`, and confirm before drawing. This discipline matters more than
any drawing trick.

## Workflow

Work through these phases in order. Ask questions in small batches (use the interactive choice tool
when on mobile). Don't stall waiting for answers you can reasonably default — state the assumption and
proceed, but never invent technical content.

### Phase 1 — Understand the goal
Establish, briefly:
- **Purpose / type**: control schematic, system block diagram, point-to-point wiring, test-fixture
  (ATE) harness map, single-line, interconnect overview.
- **Audience / use**: quick documentation vs. manufacturing/build-ready vs. review/presentation.
- **Standard**: IEC 60617, ISO, ANSI/IEEE, or "house style / none". This sets symbol shapes.
- **Output**: PDF (default), Word/.docx, and/or editable source for a desktop tool.
- **Scale**: is true physical scale required (layout/harness) or is a topological schematic fine?
  Be honest about which — see `references/conventions.md` ("Scale").

### Phase 2 — Reference documents (ask if the user has them)
Ask explicitly: *"Do you have any reference material I should follow?"* — e.g. a drawing
standard / symbol sheet, a title-block or template to match, an earlier drawing whose style to
mirror, or a parts/relay list. If provided, read them and **adopt their symbols, labels, sheet
layout and naming** rather than your own defaults.

### Phase 3 — Input information (ask, then review adversarially)
Ask what inputs exist: handwritten sketches or **photos**, netlists, a **connection list
(CSV/Excel)**, a BOM, or prior documents. Read every input (for spreadsheets/PDFs use the matching
skill; for images, read them directly).

Then, before drawing:
1. **Transcribe every signal and connection into a connection table** (From → Via → To → Notes).
   This table — not the drawing — is the source of truth.
2. **Adversarial check.** Re-read the source against your table. Watch for misreads (e.g. "loom"
   read as "100m"; "T1/T2" read as "±1/±2"), omitted components, and labels you supplied that the
   source never stated. Anything uncertain in the scan/handwriting gets `[VERIFY]`, not a guess.
3. **Confirm the table with the user** before investing in diagrams, especially the `[VERIFY]` rows.

### Phase 4 — Component & module research (BOM)
Every block in the final diagram and its description must be grounded in a real, identified
component — not a guess. This phase resolves what each item in the connection table actually *is*
before any drawing starts.

**If the user has provided a BOM** (manufacturer part numbers against the connection data):
1. Extract the list of **unique** components/modules referenced (dedupe by part number, not by
   reference designator — the same part number can appear at many tags).
2. Since a real BOM typically has many unique parts, **spawn one research subagent per component
   (or small batched groups of related parts)** rather than researching serially — use the `Agent`
   tool in parallel calls. Each subagent's task: given a manufacturer + part number, find its
   **physical packaging/enclosure type, dimensions, pin/terminal labeling convention, and a short
   function summary** from public datasheet/product info. Instruct each subagent to mark anything
   it can't confirm as `[VERIFY]` rather than inferring it.
3. Consolidate every subagent's findings into one **component table** (Part # → Manufacturer →
   Package/enclosure → Dimensions → Pin/terminal labels → Function). This table feeds the blocks
   list in the final document (`references/assembly.md`) and informs symbol choice in Phase 5.

**If the user has not provided a BOM**, do not silently assume component identities:
1. From the connection table alone, list every distinct component/module type you can identify
   (by tag, footprint, or description in the source).
2. Draft your own best-effort understanding of what each one is and its likely function, based on
   how it's wired — this is a hypothesis, not a confirmed fact.
3. **Present this consolidated understanding to the user and ask them to confirm or correct it**
   (batch the questions/table in one pass) before proceeding. Do not move to diagram drafting
   until the user has reviewed and approved this understanding — everything downstream depends on
   these identities being right, not assumed.

### Phase 5 — Draft the diagrams
Pick the tool per diagram from the routing table below. Then:
- Draw with **proper symbols**, not plain boxes: relays as relay blocks (dashed boundary, ganged
  N.O./N.C. contacts, mechanical link to a coil with A1/A2, pole/reference label); terminals as
  filled dots; instruments as labelled circles/blocks (DMM, M, W, V, A); connectors as pin blocks.
- Apply **conventions** (color coding, orthogonal routing, power-left / switching-centre /
  instruments-right zoning, a legend on every sheet, scale in the title block). See
  `references/conventions.md`.
- Render drafts to PNG/SVG so they can be shown in chat.

### Phase 6 — Review with the user
Show the draft(s) inline and ask focused questions, leading with the `[VERIFY]` items. Iterate on
layout/labels. Don't proceed to the polished document until the content is confirmed.

### Phase 7 — Assemble the final document
Produce the deliverable: each diagram (to scale where applicable) followed by a **short description
of each block**, the connection table, and a consolidated **"Items to verify"** list. PDF is the
default (best fidelity via Chromium); use `.docx` if the user wants Word. See
`references/assembly.md`. Then present the files.

## Tool routing

| Diagram / need | Use | Why |
|---|---|---|
| Electrical schematic with standard component symbols (relays, contacts, sources, meters) | **schemdraw** (`scripts/schemdraw_example.py`) | Real IEC-style symbols incl. a `Relay` element; least drawing effort |
| Exact-scale or custom wiring schematic, full control, precise relay blocks | **hand-built SVG** (`scripts/schematic_lib.py`) → PDF | Pixel/scale control; matches a house style exactly |
| System / interconnect block diagram (modules, connectors, looms, harnesses) with zoned, color-coded, orthogonal routing | **matplotlib engine** (`scripts/fixture_diagrammer.py`) | Controlled placement; color-coded harnesses; to-scale via equal aspect |
| Quick auto-laid-out block/flow diagram | **Graphviz `dot`** or **Mermaid** | Fast; Mermaid also renders live in chat for review |
| Editable, manufacturing-grade, ISO-symbol native file | Recommend **QElectroTech** (IEC 60617, free), **KiCad** (electronics), or **draw.io** to the user | These can't run headless here; supply them the connection table + a draft to import |
| Final assembly to PDF | **HTML + SVG → Chromium** (`scripts/render_pdf.js`) | Highest fidelity, honours scale and page layout |
| Final assembly to Word | **python-docx** (embed the rendered PNGs) | When the user specifically wants `.docx` |

Note on Graphviz: the bundled matplotlib engine is preferred for *controlled* engineering layouts
(auto-layout tends to fight zoning and orthogonal routing). Graphviz/Mermaid are fine for fast
first-pass block diagrams or when the user just wants topology.

## Bundled scripts

Read or run these directly; they encode the conventions so you don't re-derive them each time.

- `scripts/schematic_lib.py` — SVG primitives: `term`, `wire`, `no_contact`, `relay` (configurable
  pole count and N.O./N.C.), `instrument`, `dmm`, `source_block`, `connector`, `bracket`, plus
  `svg()` / `html_page()` wrappers and a `mm()` scale helper. Import it to build schematics. A
  `__main__` demo renders a sample sheet.
- `scripts/render_pdf.js` — `node render_pdf.js <input.html> <output.pdf>`: renders HTML/SVG to a
  Letter PDF via Chromium (Playwright). Use `printBackground:true` is already set.
- `scripts/fixture_diagrammer.py` — improved matplotlib `FixtureDiagrammer` (orthogonal routing,
  harness color-coding, zoning, legend) **plus a `draw_relay` method** for proper relay/contactor
  symbols. A `__main__` demo saves a sample PNG.
- `scripts/schemdraw_example.py` — minimal working schemdraw example (source → relay-switched
  contact → load, with coil) showing the standard-symbol path.

Install note: `pip install --break-system-packages schemdraw` (matplotlib, python-docx, Graphviz
`dot`, and Playwright/Chromium are already present).

## References
- `references/tools.md` — full open-source vs. paid tool catalog and selection guidance.
- `references/conventions.md` — symbols, color code, routing, zoning, scale, title block, and the
  source-review discipline.
- `references/assembly.md` — building the final PDF (HTML structure, keep-together rules,
  per-block descriptions, verify list) and the python-docx alternative.
- `references/iso-standards.md` — ISO/IEC 81346 reference designations, ANSI/ISA 5.1 instrument
  tagging, IEC 60617 electrical symbols, and ISO 14617/10628/15519 process symbols.
