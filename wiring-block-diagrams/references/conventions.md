# Drawing conventions

Apply these unless the user's reference material says otherwise — their house style always wins.

## Source-review discipline (read this first)

Diagrams are only as good as the transcription behind them. Before drawing:
1. Build a **connection table** (From → Via → To → Notes) capturing every signal/conductor.
2. Re-read the source *against* the table, adversarially. Common, real errors to catch:
   - "loom" misread as "100m"; a wiring loom turned into a length.
   - Terminal "T1/T2/T3" misread as "±1/±2/±3" (a bar over T looks like ±).
   - A component silently dropped (e.g. a motor/fan load left off).
   - Invented attributes: loom *types*, lengths, ratings, or part numbers the source never stated.
3. Mark every uncertain reading `[VERIFY]`. **Flag, don't guess.**
4. Don't expand acronyms you can't source — describe function from the wiring and say the expansion
   isn't given.
5. Confirm the table (especially `[VERIFY]` rows) with the user before polishing.

## Symbols

Prefer recognised conventions over plain rectangles:

- **Relay / contactor** — a dashed relay-boundary box containing one switched **contact per pole**
  (normally-open = open blade; normally-closed = closed blade), a dashed **mechanical link** from the
  ganged contacts to a **coil** drawn as a small rectangle with terminals **A1 / A2**, and a label
  giving the **reference and pole count** (e.g. "K1 — 3-pole, N.O."). This is the single most
  important symbol to get right; plain boxes labelled "relay" are not acceptable.
- **Terminal / junction** — filled dot. A dot means connection; lines crossing **without** a dot are
  no-connect.
- **Instrument** — labelled circle: `M` motor, `W` wattmeter, `V` voltmeter, `A` ammeter; or a block
  for multi-function (e.g. `DMM`). Show the terminals it lands on.
- **Source** — `AC Source` / `DC Source` block, or an IEC source symbol (sine for AC, `=`/`~` for an
  SMPS). The bundled matplotlib `draw_smps` draws the `~` over `=` convention.
- **Connector** — pin block labelled with its designator (e.g. `J4`) and pin names.
- **Bus / multicore** — multiple parallel lines or one thick line annotated with conductor count.

## Color code (harness / signal class)

Put a **legend on every sheet**.

| Class | Color | Style |
|---|---|---|
| AC mains / DC power rails | Red | solid (AC) / dashed (DC) or annotate |
| Low-frequency measurement / logic / control | Blue | solid |
| High-frequency RF / coax | Orange | thick |
| Physical multicore harness (DB25/DB50, looms) | Dark navy `#003366` | thick |
| Signal / generic | Dark slate | thin |

## Routing & layout

- **Orthogonal**: connection lines run at 90°. Avoid routing lines across module boxes.
- **Zoning**: power/sources on the **left**, switching/logic/relays in the **centre**,
  instrumentation/targets on the **right**. Signals generally flow left→right.
- Keep relay groups vertically separated so contact stacks and coils don't collide (give each relay
  block clear space below its lowest pole for the coil + reference label).
- Label every conductor at least once; label terminals at both ends where space allows.

## Scale

Be honest about what "to scale" means:
- **Schematics are topological** — symbol size and spacing aid readability, not physical dimension.
  Put "Schematic — not to physical scale" in the title block when that's the case.
- **Layout / harness / panel drawings can be true-scale.** Then fix a scale (e.g. `1 unit = 5 mm`),
  use equal aspect (`ax.set_aspect('equal')` in matplotlib, or a fixed mm→px factor in SVG — see
  `schematic_lib.mm()`), draw components at real size, and **state the scale in the title block**.
- When a user says "to scale", clarify which of the two they mean; default schematics to topological
  with neat, consistent spacing.

## Title block (every sheet)

Include: drawing **title**, **unit / system ID**, **revision**, **date**, **scale** (or "not to
scale"), and a provenance line such as "Drawn from <source>; verify against original." Mirror the
user's template if they gave one.
