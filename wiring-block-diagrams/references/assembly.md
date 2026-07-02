# Assembling the final document

The deliverable is not just images — it is **diagrams + a description of each block + the connection
table + a consolidated verify list**, laid out cleanly. PDF is the default.

## Structure (use this order)

1. **Title + provenance note** — what it is, source, and that `[VERIFY]` marks unconfirmed readings.
2. **(Optional) Corrections/decisions note** — if you reworked a prior version, list the key fixes.
3. **One section per sheet/unit**, each containing:
   - the **diagram** (to scale where applicable),
   - a short **"blocks" list** describing every block in that diagram (1 line each),
   - the **connection table** for that sheet.
4. **Items to verify** — consolidated `[VERIFY]` list with section references.
5. **Footer** — assumptions (e.g. inferred relay refs/pole counts), and unexpanded acronyms.

Keep each block's description to a sentence or two: what it is and what it does, derived from the
wiring. Don't pad.

## PDF via HTML + SVG + Chromium (preferred)

This path gives exact control and honours scale. Pattern:
1. Build an HTML string: a print stylesheet + inline `<svg>` diagrams (from `schematic_lib.py`) +
   HTML tables + the per-block lists.
2. Keep figures intact across page breaks:
   ```css
   .avoid { break-inside: avoid; page-break-inside: avoid; }
   h2, h3 { break-after: avoid; page-break-after: avoid; }
   ```
   Wrap each *diagram + its block-list* and each *table* in a `<div class="avoid">`. Prefer natural
   flow over forced `page-break-before` (forced breaks tend to orphan small tables onto blank pages).
3. Render: `node scripts/render_pdf.js report.html report.pdf` (Letter, backgrounds on, ~14 mm margins).
4. **Self-check**: rasterise and eyeball before delivering —
   `pdftoppm -jpeg -r 96 report.pdf page` — then `view` the pages. Fix overlaps (a relay reference
   label colliding with its coil, captions over boxes, two relay blocks crowding) and re-render.

## PDF/PNG via matplotlib (block diagrams)

`scripts/fixture_diagrammer.py` saves PNGs at 300 dpi. Embed those PNGs either in the HTML above or in
a docx. Good when the diagram is a zoned block/harness map rather than a fine schematic.

## Word (.docx) alternative

When the user wants Word: render each diagram to PNG, then use **python-docx** to build the document —
heading per section, the embedded image, the block-description list, and a table. Mirror the same
structure as the PDF. (If you instead need rich Word features like styled tables/TOC, the separate
`docx` skill and its docx-js path is also available.)

## Optional: presentation polish with nano-banana-2 (MCP)

The `nano-banana-2` MCP server (Gemini image generation) is available for **decorative, non-technical**
polish only — a cover page background, a title-block texture, or a stylized rendering of the document
shell for a presentation deck. Rules:

- **Never** generate the wiring/block diagram content itself with `generate_image`/`edit_image`. AI
  image generation can hallucinate labels, miscount pins/contacts, or garble text — unacceptable for
  connection-critical content that must match the verified connection table exactly.
- The precise diagram (schemdraw/matplotlib/SVG output) is always the technical source of truth and is
  embedded unmodified; nano-banana only touches surrounding decorative elements (cover art, background
  imagery, section-divider graphics).
- Call `get_configuration_status` first to confirm the server has a working `GEMINI_API_KEY` before
  offering this option — treat it as unavailable and fall back to a plain title page if not configured.
- Always show the generated art to the user for approval before including it in the final PDF/docx —
  treat it like any other draft, not a guaranteed-correct output.

## Quality gate before presenting

- Every connection in the diagram appears in the table and vice-versa.
- Relays render as relay blocks (contacts + coil + A1/A2 + pole count), not plain boxes.
- A legend and a title block (with scale or "not to scale") are present on each sheet.
- All `[VERIFY]` items are visible both on the drawing and in the consolidated list.
- No invented labels, lengths, types, or part numbers.
- Pages rasterised and visually checked; no overlapping text or clipped content.
