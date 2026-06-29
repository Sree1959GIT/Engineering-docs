# Tool catalog & selection

Default to tools that run **in this sandbox for free**. Recommend desktop/paid software only when the
user needs an editable native file in that ecosystem; in that case still produce the connection table
and a draft they can import.

## In-sandbox (free, verified to run here)

| Tool | Install | Best for | Notes |
|---|---|---|---|
| **matplotlib** | preinstalled | Block / interconnect diagrams with controlled placement, color-coded harnesses, zoning, to-scale layout | Use `scripts/fixture_diagrammer.py`. Set `ax.set_aspect('equal')` for true scale. |
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
