# Tool catalog & selection

Default to tools that run **in this sandbox for free**. Recommend desktop/paid software only when the
user needs an editable native file in that ecosystem; in that case still produce the connection table
and a draft they can import.

## Output tiers (visual style)

Ask which tier the user wants in Phase 1 of `SKILL.md` (default: **Tier 2, illustrated/pictorial**,
unless the user says otherwise):

| Tier | What it is | Produced by | Accuracy risk |
|---|---|---|---|
| **1 — Simple block** | Abstract, category-differentiated blocks (see `conventions.md` "Block differentiation") | `scripts/fixture_diagrammer.py` | None — every label is hand-coded from confirmed data. Fastest; best for systems with many components (dozens+) where icon detail would clutter the page. |
| **2 — Illustrated / pictorial** | Vector icons resembling real component silhouettes (AC outlet, screw-terminal power module, relay/PCB board, DIN-rail terminal strip) | `scripts/illustrated_diagrammer.py` | None — same hand-coded labels, just richer icon shapes. Closer to a "professional CAD" look. Default recommendation: better for smaller component counts / customer-facing documents. |
| **3 — Photorealistic (external)** | AI-image-generated renders (e.g. Gemini/"Nano Banana") that look like real product photos | **Not available in this sandbox** — no image-generation model/plugin is connected here | **Real risk**: image-gen models can subtly hallucinate a label, pin count, or terminal number that looks plausible but is wrong. Never use for a document someone will wire a board from without a manual label-by-label check against the source. |

For Tier 3, Claude can still help: draft an accurate, ready-to-paste prompt built from the
confirmed connection table/BOM (component names, exact terminal labels, wire colors) for the user
to run through their own image-gen tool — but the resulting image must be checked against the
source data before use, exactly like any other `[VERIFY]` item.

## In-sandbox (free, verified to run here)

| Tool | Install | Best for | Notes |
|---|---|---|---|
| **matplotlib** | preinstalled | Block / interconnect diagrams with controlled placement, color-coded harnesses, zoning, to-scale layout | Use `scripts/fixture_diagrammer.py`. Set `ax.set_aspect('equal')` for true scale. |
| **matplotlib (illustrated)** | preinstalled | Tier 2 illustrated/pictorial diagrams — component-shaped icons instead of plain blocks | Use `scripts/illustrated_diagrammer.py` (`draw_ac_outlet`, `draw_power_module`, `draw_relay_module`, `draw_din_rail_terminal_strip`, `draw_generic_pcb`). |
| **schemdraw** | `pip install --break-system-packages schemdraw` | Electrical schematics with standard symbols (sources, resistors, switches, **relays**, meters) | Has `elements.Relay`, `Switch`, `SourceSin`, `MeterV/A`. Least effort for recognisable schematics. |
| **Graphviz `dot`** | preinstalled (`dot -V`) | Fast auto-laid-out block/flow/topology diagrams | Auto-layout fights orthogonal zoning; use for first-pass topology only. |
| **Mermaid** | render in an artifact, or `npm i -g @mermaid-js/mermaid-cli` (+ Chromium) | Quick block/flow diagrams that also render live in chat for review | Good for the Phase-5 review loop. |
| **SVG + Chromium** | Playwright preinstalled | Pixel- and scale-exact custom schematics; final PDF assembly | `scripts/schematic_lib.py` + `scripts/render_pdf.js`. Highest fidelity. |
| **python-docx** | `pip install --break-system-packages python-docx` | Word output with embedded diagram PNGs | When the user wants `.docx` instead of PDF. |

## Desktop / open-source the user runs themselves (cannot run headless here)

- **QElectroTech** — *best open-source for industrial electrical.* 8,000+ symbols incl. full **IEC
  60617** and ISO, custom symbol editor, exports PDF/SVG/DXF/BOM. Free (GPL). Recommend when the user
  needs editable, standard-compliant industrial schematics (relay logic, terminal strips,
  contactors). Claude can hand them the connection table and an SVG draft.
- **KiCad** — open-source EDA for electronics/PCB (schematic capture, netlists, PCB, Gerber). Use when
  the work is circuit/PCB rather than industrial wiring. Has a CLI (`kicad-cli`) the user can script.
- **draw.io / diagrams.net** — free, open-source, browser-based; has an AI "Generate" prompt-to-diagram
  feature. General symbols (not strict IEC). Great for block/architecture diagrams the user wants to
  keep editing.
- **gEDA** — mature Linux EDA suite; dated UI; electronics focus.

## Paid (mention only if the user asks or needs them)

- **EPLAN Electric P8** — industry gold standard for control panels; database-driven (one change
  cascades to wire numbers, terminals, BOM, cable lists); IEC 60617/ISO/NFPA. ~€3.5–8k/seat/yr.
- **AutoCAD Electrical** — drafting-focused electrical CAD; IEC/NFPA/JIC/IEEE; ~US$2k/yr.
- **Zuken E3.series** — database-driven; *FunctionalDesign* turns block sketches into detailed wiring;
  strong cable/harness + 3D. Pricing on request.
- **SmartDraw** — easy browser diagramming with IEC/ANSI libraries; documentation-grade. ~US$10/mo.
- **Cadence OrCAD X** — PCB schematic capture + SPICE simulation. Electronics, not industrial wiring.

## AI prompt-to-diagram tools (emerging; mostly electronics)

ProtoFlow and Skimatly (NL → KiCad/EasyEDA schematics), CircuitLM (research), draw.io AI, Eraser.io.
Key limitation as of 2026: they do **electronic circuits** and **general block/architecture** well but
do **not** reliably produce ISO-60617 industrial wiring (relay logic, terminal strips). For that, the
QElectroTech-symbols + structured-input path is more dependable.

## Selection cheat-sheet

- Industrial control schematic, standard symbols, editable → **QElectroTech** (user-side) + Claude's table/draft.
- Recognisable schematic produced here, low effort → **schemdraw**.
- Exact look / scale / house style produced here → **SVG (`schematic_lib.py`)**.
- System block / harness map, color-coded & zoned → **matplotlib (`fixture_diagrammer.py`)**.
- Just show topology fast / live review → **Mermaid** or **Graphviz**.
- Electronics / PCB → **KiCad**.
