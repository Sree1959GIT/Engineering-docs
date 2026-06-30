# ISO/IEC standards for component & module notation

Reference material for understanding standardized symbols, reference designations, and letter
codes when transcribing source drawings and building block/wiring diagrams. Use alongside
`conventions.md` (drawing rules), `tools.md` (what to draw with), and `assembly.md` (final
document structure). Sources: ISO/IEC 81346 introduction booklet, IEC 60617 symbol catalog
extract, and a P&ID training course covering ANSI/ISA 5.1 and the wider standards landscape
(see **Sources** at the end). The two reference URLs the user supplied (AutoCAD Electrical IEC
help page, Wikipedia ISO 14617) returned HTTP 403 in this sandbox and could not be fetched —
re-attempt if the user can supply the page content directly.

## ISO/IEC 81346 — Reference designations ("TAGs")

*Industrial systems, installations and equipment and industrial products — Structuring
principles and reference designations.* Part 1: Basic rules. Part 2: Classification of objects
and letter codes. (Also published as DS/EN Handbook 166:2010.) Governs how components, modules,
and equipment are **tagged**, independent of which graphical symbol is drawn.

A reference designation is built from up to three **aspects**, each introduced by its own
prefix character and freely combinable in a single tag:

| Aspect | Prefix | Answers | Example |
|---|---|---|---|
| Function | `=` | What does it do? | `=V11` |
| Location | `+` | Where is it installed? | `+B1` |
| Product | `−` | What part/product is it? | `−K4` |

A full tag chains aspects, e.g. `=B1.V11` (function V11 within function-group B1) or
`+B1−K4` (product K4 located in B1). Read tags left to right as a path: higher-level
groupings first, the specific item last.

### Letter-code classes (function aspect, A–X)

81346-2 assigns each function-aspect letter a class of object, e.g.:

| Letter | Class (examples) |
|---|---|
| A | Two state physical phenomena / system (general) |
| B | Conversion (non-electrical → electrical signal, sensors) |
| C | Storage |
| E | Miscellaneous (heating, lighting, non-electrical energy) |
| F | Protection (fuses, breakers, protective relays) |
| G | Generation, power supply |
| K | Relays, contactors |
| M | Motors |
| P | Presentation, indication (meters, displays) |
| Q | Switching/protection in the power circuit (switchgear) |
| R | Resistors, limiting devices |
| S | Manual switches/selectors |
| T | Transforming (transformers, converters) |
| V | Processing (valves, in fluid/process contexts) |
| W | Conductors, wiring, transmission paths |
| X | Terminals, connectors, plugs |

This is the same letter-code idea behind component prefixes seen on schematics (K1 for a relay,
M1 for a motor, Q1 for a breaker, X1 for a terminal block) — use it to sanity-check a tag's
prefix letter against what the symbol actually does.

### How to apply this here

- When a source drawing already tags components (`K1`, `M1`, `T001`, `P001`...), preserve the
  tag exactly — don't renumber or "clean up" the designator.
  Cross-check the letter against the table above; flag `[VERIFY]` if a letter looks misapplied
  (e.g. a "K" tag on something that is clearly a motor) rather than silently correcting it.
- When source material gives a part description but no tag, it is fine to describe the block by
  function in prose; don't invent a tag the source never stated.
- Aspect prefixes (`=`, `+`, `−`) are mainly seen on EPLAN/E3.series-generated industrial
  drawings. Simpler P&ID/wiring sources usually use a flat `LETTER+NUMBER` tag (`ANSI/ISA 5.1`
  style, below) without the aspect prefixes — match whichever convention the source uses.

## ANSI/ISA 5.1 — Instrumentation symbols and identification

The dominant standard for **P&ID instrument tagging** (process/instrumentation, not strictly
ISO/IEC, but the de facto companion standard wherever a drawing has instrument bubbles). A tag is
built from a **first letter** (measured/initiating variable) plus **succeeding letters**
(readout/passive function, output/active function, modifier), inside a circle ("bubble"), plus a
loop number.

Common first letters: `A` analysis · `E` voltage · `F` flow · `H` hand (manual) · `I` current ·
`L` level · `P` pressure · `Q` quantity · `S` speed/frequency · `T` temperature · `W`
weight/force · `Z` position. Succeeding letters: `T` transmit · `I` indicate · `C` control ·
`R` record · `S` switch · `A` alarm · `Y` relay/compute. So `LT` = level transmitter, `FIC` =
flow indicating controller, `PSL` = pressure switch low.

Bubble line style indicates **location**: solid circle = field-mounted; circle split by a solid
horizontal line = panel-front, normally accessible; split by a dashed line = panel-front,
normally inaccessible (e.g. inside a locked cabinet); double line = shared
display/computer/PLC function (see source PDF Figure 19 for the full field/panel/auxiliary ×
accessible/inaccessible grid).

Always check for a **legend/abbreviation table** on the source drawing first — site-specific
letter usage (e.g. "M" for Motor vs. Manway) is common and overrides the generic table when they
conflict. If no legend is given and a letter is ambiguous, mark `[VERIFY]` rather than guessing.

## IEC 60617 — Graphical symbols for diagrams

The base international standard (≈1900 symbols across multiple parts) for **how a component is
drawn**, independent of how it's tagged. Covers: connections/conductors, terminals, switches and
contacts, **relays and contactors** (coil + contact + mechanical-link convention used in
`conventions.md`), protective devices, generating/converting equipment, passive components
(R/L/C), semiconductors (diodes, transistors, thyristors), rotating machines (motors/generators),
transformers, instruments/meters, indicators, and selector switches. `schemdraw` (see
`tools.md`) implements a useful subset (`elements.Relay`, `Switch`, `SourceSin`, `MeterV/A`)
directly from this standard's conventions. IEC 60617 cross-references **ISO 14617** for symbols
outside the electrical domain (e.g. Fan = ISO 14617 symbol 2302, Pump = ISO 14617 symbol 2301) —
use IEC 60617 for electrical/relay-logic symbols and ISO 14617 / ISO 10628 (below) for
mechanical/process equipment symbols on the same sheet.

## ISO 14617 / ISO 10628 / ISO 15519 — Process & general diagram symbols

Used when a diagram mixes electrical control with **piping, process, or mechanical** elements
(pumps, valves, vessels, heat exchangers, fans) — common in P&IDs and in fixture/test-rig block
diagrams that include both wiring and plumbing.

- **ISO 14617** (parts 1–15, ~300 pages) — general graphical symbols for diagrams: functional
  links, control loops, processing functions, logic functions. The general-purpose counterpart
  to IEC 60617 for non-electrical technical drawings.
- **ISO 10628** — diagrams for the chemical and petrochemical industry; defines letter symbols
  for that sector.
- **ISO 15519** (parts 1 & 2) — specification for diagrams in the process industry: block
  diagram / PFD / P&ID layout, connecting-line conventions, inscription, scale, and limits.
- **PIP PIC001** and **EN 62424** — industry-consortium and IEC standards for P&ID documentation
  criteria and P&ID software/controls-interface representation, respectively. Mentioned for
  completeness; rarely needed unless the source explicitly cites them.

Common symbols seen across these process-diagram standards (pipe, flexible connection, fan,
mixing vessel, packed/plate column, heat exchanger variants, gas vent, steam trap, viewing glass,
gate/control/needle/butterfly/check/diaphragm/ball valve, pump, compressor, dryer, pressurized
vessel, furnace, cooling tower, filter, funnel) line up closely with the symbol set already
described qualitatively in `conventions.md`'s **Symbols** section — treat that section as the
house style and this document as the standards basis behind it.

### ISO 14617 symbol catalog (worked reference, 103 symbols)

A 6-page company-internal instruction sheet ("ISO 14617 SYMBOLS", Wärtsilä Technology Oy, drawing
4V92A1174, 2002 edition) numbers and draws 103 ISO 14617 process symbols. Each entry cites its
ISO 14617 part/clause and item number (e.g. `8-4.1.1.Sym 2101` = part 8, clause 4.1.1, item
2101 = two-way valve). Useful as a recognition reference when a source drawing uses bare process
symbols with no label. Grouped by category (pos. numbers from that sheet in brackets):

- **Valves — two-way** [1–18]: plain two-way valve; manual/weight-loaded/float-operated/
  solenoid/electric-motor/diaphragm/double-acting-cylinder actuated variants; spring-loaded
  safety valve with automatic return; combined non-return + manually actuated stop valve;
  self-operating pressure-reducing control valve. Actuator type is shown as a small symbol
  stacked on the valve body (motor = circled M, diaphragm = curved cap, solenoid = coil box,
  cylinder = rectangle, spring = zigzag).
- **Valves — three-way** [17–25]: three-way valve with the same actuator-variant pattern
  (solenoid, electric motor, diaphragm, double-acting cylinder), plus self-operating
  pressure-reducing and self-operating thermostatic three-way control valves.
- **Valves — angled** [26–30]: angle two-way valve, weight-loaded, spring-loaded safety,
  non-return (plain and hand-operating) angled valves.
- **Valves — restriction/release/shuttle** [31–35, 99, 102–103]: adjustable restrictor, orifice
  plate, restrictor, self-operating release valve / steam trap / air vent, shuttle valve with
  AND-function, overflow safety valve, and the open/close two-position vs. infinite-position
  automatic valve-operator symbols (circle-on-stem next to the valve body, with OPEN/CLOSE
  labels) — these last two are the standard way to show a valve's actuator has discrete vs.
  continuous positioning.
- **Valves — multi-port (2/3/4-way pneumatic/solenoid/lever/manual)** [36–50]: the
  pneumatic-distribution-valve symbol family (`Valve_2_2_...`, `Valve_3_2_...`,
  `Valve_4_2_...`) — a row of small boxes (port/flow-path positions) with an actuator symbol at
  each end (pneumatic, solenoid, lever+spring, manual+spring). Common on hydraulic/pneumatic
  circuit diagrams rather than P&IDs.
- **Rotating machines** [51–58]: turbogenerator (circle + triangle), turbogenerator with gear
  transmission, turbocharger, electric motor (circled M), compressor (circle with flat side),
  liquid pump and hydraulic pump (circle with internal triangle/arrow), manual hydraulic pump.
- **Heat transfer & vessels** [59–65, 92–95]: boiler feedwater vessel with deaerator, heating/
  cooling coil, heat exchanger/condenser, pneumatic-air lubricator, air fin cooler with induced
  draft (radiator), drain funnel, trough/drip tray with drain funnel, pipeline with/without
  thermal insulation, pressure vessel with diaphragm (expansion vessel), pressure/vacuum vessel.
- **Pipe fittings & joints** [66–79]: blind flange pair, flange coupling/pair, end cap, screwed
  joint, pipe reducer (concentric and eccentric), quick-release coupling elements (female/male,
  with/without automatic closing on decoupling), flexible pipe/bellows/hose, expansion sleeve,
  expansion bellows.
- **Vents, traps & silencers** [80–82, 96–97]: siphon/anti-siphon trap, air vent, air vent +
  flame arrestor, silencer, viewing glass.
- **Filters & separators** [83–91]: high-speed centrifuge (separator), centrifugal filter,
  candle filter with rotating drum (plain and with by-pass), bag/candle/leaf/cartridge filter,
  duplex filter, screen/sieve/strainer/filter, settling separator, cyclone separator — these
  share a family resemblance (a box with an internal filter-element hatch pattern); the specific
  hatch/internal-symbol distinguishes the filter type.
- **Indicating instruments** [98, 100–101]: generic indicating/measuring instrument (circled X
  with a letter key — P pressure, T temperature, V viscosity, F flow rate — cites **ISO 3511**
  for the instrument letter codes, the predecessor scheme ANSI/ISA 5.1 superseded for most new
  work), flow-rate indication (circled FI), flow-rate recording with volume summation (circled
  FRQ + FT pair).

Treat the descriptions above as a recognition aid, not a redraw template — when a source drawing
uses one of these symbols, identify it from this list and describe its function in the blocks
list per `assembly.md`, rather than copying the schematic glyph pixel-for-pixel.

## Quick lookup: which standard governs what

| Question | Standard |
|---|---|
| What letter/number does this component's tag use? | ISO/IEC 81346 (general) or ANSI/ISA 5.1 (P&ID instrument bubbles specifically) |
| How should this electrical/relay symbol be drawn? | IEC 60617 |
| How should this process/mechanical symbol (pump, valve, vessel) be drawn? | ISO 14617 / ISO 10628 |
| How should the overall P&ID sheet be laid out (line types, scale, limits)? | ISO 15519 |
| What does this bubble's line style (solid/split/double) mean? | ANSI/ISA 5.1 (field vs. panel vs. shared/computer location) |

## Sources

- *Brief introduction to ISO/IEC 81346* (uploaded PDF, 8 pp.) — aspects, letter-code classes,
  tag structure examples.
- IEC 60617 symbol catalog extract (uploaded PDF, 53 pp.) — symbol descriptions across
  connections, switches, relays, protective devices, machines, transformers, instruments;
  page 52 cross-references ISO 14617 (Fan 2302, Pump 2301).
- *ISO 14617 Symbols* (uploaded PDF, 6 pp.) — Wärtsilä Technology Oy internal instruction sheet,
  drawing 4V92A1174, numbering and drawing 103 ISO 14617:2002-01 process symbols (valves,
  rotating machines, heat transfer/vessels, pipe fittings, filters/separators, instruments) with
  ISO part/clause/item citations per symbol.
- Mark Ludwigson, *Piping and Instrumentation Diagrams* (SunCam online CE course, uploaded PDF,
  pp. 1–26 read) — P&ID overview, related diagram types (block flow, PFD, instrument schematic,
  wiring diagram, SCADA, logic diagrams), **Table 1: Summary of Standards for P&IDs** (ANSI/ISA
  5.1, ISA 5.3, IEC 60617, ISO 10628, ISO 14617, ISO 15519, PIP PIC001, EN 62424), ANSI/ISA 5.1
  letter-designation tables, and common P&ID symbol sets (Figures 18a/18b, 19).
- AutoCAD Electrical IEC help page and Wikipedia ISO 14617 — requested by the user but returned
  HTTP 403 in this sandbox; not yet incorporated.
