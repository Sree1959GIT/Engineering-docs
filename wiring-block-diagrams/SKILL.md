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
inputs → **build a connection table that is the single source of truth** → **establish and confirm
component identity/packaging (two approval gates before and after any research subagents)** → draft
diagrams → review with the user → assemble a final document of to-scale diagrams plus a description
of each block.

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
- **Output tier**: ask which visual style — **Tier 1 simple block** (fast, abstract, best for
  systems with many components), **Tier 2 illustrated/pictorial** (vector icons resembling real
  components — default recommendation), or **Tier 3 photorealistic** (AI-image-generated —
  requires an external tool this sandbox doesn't have, and carries real label/pin hallucination
  risk; Claude can only draft a prompt for the user to run elsewhere). See `references/tools.md`
  ("Output tiers").
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
   Also watch for unresolved CAD auto-tag placeholders (e.g. literal `%K%3` instead of `K3` —
   see `references/iso-standards.md` "Automatic tag placeholders") — flag `[VERIFY]`, don't
   invent the resolved number yourself.
3. **Confirm the table with the user** before investing in diagrams, especially the `[VERIFY]` rows.

### Phase 4 — Component & module research (BOM)
Every block in the final diagram and its description must be grounded in a real, identified
component — not a guess. This phase resolves what each item in the connection table actually *is*,
and its physical packaging/dimensions, before any drawing starts. It has **two hard approval gates**
— never spawn research subagents, and never move to Phase 5, without the user's sign-off at each one.

**Step A — Establish component identities.**

- **If the user has provided a BOM** (manufacturer part numbers against the connection data),
  extract the list of **unique** components/modules referenced (dedupe by part number, not by
  reference designator — the same part number can appear at many tags). Skip to Step B with this
  list.
- **If the user has not provided a BOM**, don't silently assume identities:
  1. From the connection table, list every distinct component/module type you can identify (by
     tag, footprint, or description in the source).
  2. Ask the user, per component, for whatever identifying detail they can give: a manufacturer +
     part number/model, a URL, an uploaded datasheet/document, or a free-text description. Batch
     these questions together (don't ask one at a time).
  3. Where the user gives nothing beyond a functional description, draft your own best-effort
     hypothesis of what it is, clearly marked as inferred (not confirmed).

**Step B — Preliminary report (Gate 1).**
Before doing any research, write up a plain summary of exactly what you have for each component:
what the user told you verbatim (part#/make/model, URL, doc, or description) plus any of your own
inferred hypotheses, clearly labeled as such. **Present this and get explicit user approval before
proceeding.** This gate exists so research effort isn't wasted chasing a misread part number or a
wrong assumption.

**Step C — Spawn research subagents.**
Once Gate 1 is approved, for every component that has an external reference to chase (a
manufacturer+part#, a URL, or an uploaded document) spawn a research subagent — **one subagent per
component** (or small batched groups of closely related parts), run in parallel via the `Agent`
tool, since a real component set typically has many unique items and serial research doesn't scale.
Each subagent's brief: given the reference, find its **physical packaging/enclosure type,
dimensions, pin/terminal labeling convention, and a short function summary**, sourced from the
datasheet/URL/document/public product info. Instruct every subagent to mark anything it can't
confirm as `[VERIFY]` rather than inferring it. Components fully specified by the user's own
free-text description in Step A (no external reference to chase) don't need a subagent — carry
their description straight through.

**Step D — Packaging report (Gate 2).**
Consolidate every subagent's findings — plus the directly-specified components — into one
**component table**: Component/Tag → Part # → Manufacturer → Package/enclosure → Dimensions →
Pin/terminal labels → Function. Present this as the packaging report: *this is the physical data
that will be represented in the final block/wiring diagrams*. **Get explicit user approval before
proceeding to Phase 5.** By this gate you have a confirmed understanding of both connectivity
(Phase 3) and component identity/packaging (Phase 4), sufficient to draft the functional
description and diagrams without further guessing.

This table feeds the blocks list in the final document (`references/assembly.md`) and informs
symbol choice and physical layout in Phase 5.

### Phase 5 — Draft the diagrams
Pick the tool per diagram from the routing table below, matching the **output tier** agreed in
Phase 1 (`references/tools.md` "Output tiers"): Tier 1 uses `scripts/fixture_diagrammer.py`
(plain category-styled blocks); Tier 2 uses `scripts/illustrated_diagrammer.py` (component-shaped
icons — AC outlet, power-module screw terminals, relay/PCB board, DIN-rail terminal strip); Tier 3
is out of scope for this sandbox (draft a prompt for the user's own external tool instead). Then:
- Draw with **proper symbols**, not plain boxes: relays as relay blocks (dashed boundary, ganged
  N.O./N.C. contacts, mechanical link to a coil with A1/A2, pole/reference label); terminals as
  filled dots; instruments as labelled circles/blocks (DMM, M, W, V, A); connectors as pin blocks.
- In **block/interconnect diagrams**, make module **categories visually distinguishable** (power
  supply vs. relay/switching module vs. interface/adapter vs. custom board vs. connector — distinct
  shape/border/fill per category, not one plain rectangle for everything), and label every block
  with its tag, part number/manufacturer (if known), and a one-line function. Orient pins by
  function (inputs left, outputs right, power in top, ground/common bottom) unless the source
  drawing already establishes a different, consistent orientation. See `references/conventions.md`
  ("Block differentiation" and its "Pin-side orientation" subsection).
- Use **ISO 128 line-type semantics** so the drawing still reads correctly without color: thick
  continuous for primary power/bus, thin continuous for control/signal, dashed thin for mechanical
  linkages/enclosure boundaries, chain-thin for centerlines. See `references/conventions.md`
  ("Line types & layers").
- When a signal crosses sheets or leaves/enters a block that isn't directly adjacent on the page,
  use matching **off-page arrow connectors** (`SIGNAL >>` at the exit, `>> SIGNAL` at the entry)
  rather than letting a wire dangle. See `references/conventions.md` ("Cross-sheet / off-page
  signal connectors").
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
| System / interconnect block diagram (modules, connectors, looms, harnesses) with zoned, color-coded, orthogonal routing — Tier 1 (simple block) | **matplotlib engine** (`scripts/fixture_diagrammer.py`) | Controlled placement; color-coded harnesses; to-scale via equal aspect |
| System / interconnect block diagram, Tier 2 (illustrated/pictorial — component-shaped icons) | **matplotlib illustrated engine** (`scripts/illustrated_diagrammer.py`) | Same accuracy discipline as Tier 1, but icons resemble real component silhouettes (outlet, screw terminals, PCB, DIN rail) |
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
  symbols, `draw_categorized_block` for Tier-1 category-styled blocks, ISO 128 line-style
  constants, and `draw_offpage_connector`/`draw_mechanical_link` helpers. A `__main__` demo saves
  a sample PNG.
- `scripts/illustrated_diagrammer.py` — Tier 2 (illustrated/pictorial) `IllustratedDiagrammer`:
  `draw_ac_outlet`, `draw_power_module`, `draw_relay_module`, `draw_din_rail_terminal_strip`,
  `draw_generic_pcb` icons, plus `wire`/`add_legend_item`. A `__main__` demo saves a sample PNG.
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
