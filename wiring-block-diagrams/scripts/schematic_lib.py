# -*- coding: utf-8 -*-
"""
schematic_lib.py — reusable SVG primitives for wiring / control schematics.

Build a schematic as an SVG string, drop it into an HTML page, and render to PDF with
render_pdf.js (Chromium). Coordinates are in user units; use mm() if you need true scale.

Key primitives:
  term, wire (L), polyline (PL), text (TXT), rect (RECT), circle (CIRC)
  bracket(...)                 left grouping bracket with a label
  no_contact(...) / relay(...) a relay block: ganged contacts + coil(A1/A2) + pole/ref label
  instrument(...), dmm(...), source_block(...), connector(...)
  svg(inner,w,h), html_page(svgs, title), CSS

Run `python schematic_lib.py` to emit demo.html (then: node render_pdf.js demo.html demo.pdf).
"""

# ---- scale --------------------------------------------------------------
# Default: 1 user unit == 1 px at 96 dpi. For true-scale layout drawings, convert mm->units.
PX_PER_MM = 96.0 / 25.4
def mm(v):  # millimetres -> user units (so a 50 mm part = mm(50) units wide)
    return v * PX_PER_MM

# ---- low-level ----------------------------------------------------------
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def T(x, y, r=3.4): return f'<circle cx="{x}" cy="{y}" r="{r}" class="term"/>'
def L(x1, y1, x2, y2, cls="wire"): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>'
def PL(pts, cls="wire"): return f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" class="{cls}"/>'
def TXT(x, y, s, cls="lbl", anchor="start"): return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(s)}</text>'
def RECT(x, y, w, h, cls="blk", rx=4): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>'
def CIRC(x, y, r, cls="inst"): return f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}"/>'

def bracket(x, yt, yb, label, sub=None):
    """Left curly grouping bracket spanning yt..yb with a label."""
    mid = (yt + yb) / 2
    s = PL([(x + 10, yt), (x, yt + 8), (x, mid - 6)], "brk")
    s += PL([(x, mid + 6), (x, yb - 8), (x + 10, yb)], "brk")
    s += PL([(x, mid - 6), (x - 7, mid), (x, mid + 6)], "brk")
    s += TXT(x - 12, mid - 2, label, "grp", "end")
    if sub:
        s += TXT(x - 12, mid + 13, sub, "grpsub", "end")
    return s

def no_contact(xin, xout, y, cx1, cx2, kind="NO"):
    """One switch contact on a horizontal line. kind 'NO' (open) or 'NC' (closed)."""
    s = L(xin, y, cx1, y) + L(cx2, y, xout, y) + T(cx1, y) + T(cx2, y)
    if kind == "NC":
        s += L(cx1, y, cx2, y, "contact")           # closed blade
        mx, my = (cx1 + cx2) / 2, y
    else:
        bx, by = cx2 - 1, y - 12                      # open blade
        s += L(cx1, y, bx, by, "contact")
        mx, my = (cx1 + bx) / 2, (y + by) / 2
    return s, mx, my

def relay(poles_y, xin, xout, cx1, cx2, name, ref, kind="NO"):
    """
    Draw a multi-pole relay/contactor: one `kind` contact per y in poles_y, a dashed mechanical
    link from the ganged contacts to a coil (terminals A1/A2), a dashed relay boundary, the relay
    `name` above and a `ref`/pole-count label below.
    """
    s = ''
    mids = []
    for y in poles_y:
        seg, mx, my = no_contact(xin, xout, y, cx1, cx2, kind)
        s += seg
        mids.append((mx, my))
    gx = mids[0][0]
    top_my = min(m[1] for m in mids)
    coil_top = max(poles_y) + 22
    s += L(gx, top_my, gx, coil_top, "link")
    cw, ch = 44, 18
    s += RECT(gx - cw / 2, coil_top, cw, ch, "coil", 2)
    s += L(gx - cw / 2 - 8, coil_top + ch / 2, gx - cw / 2, coil_top + ch / 2, "wire")
    s += L(gx + cw / 2, coil_top + ch / 2, gx + cw / 2 + 8, coil_top + ch / 2, "wire")
    s += TXT(gx - cw / 2 - 10, coil_top + ch / 2 + 3, "A1", "pin", "end")
    s += TXT(gx + cw / 2 + 10, coil_top + ch / 2 + 3, "A2", "pin", "start")
    bx1, bx2 = cx1 - 16, cx2 + 16
    by1, by2 = min(poles_y) - 20, coil_top + ch + 10
    s = RECT(bx1, by1, bx2 - bx1, by2 - by1, "relaybox", 6) + s
    s += TXT((bx1 + bx2) / 2, by1 - 6, name, "rtitle", "middle")
    s += TXT((bx1 + bx2) / 2, by2 + 12, ref, "pin", "middle")
    return s

def instrument(x, y, r, sym, caption=None):
    """Labelled instrument circle (M, W, V, A...)."""
    s = CIRC(x, y, r) + TXT(x, y + 5, sym, "blab", "middle")
    if caption:
        s += TXT(x, y + r + 14, caption, "cap", "middle")
    return s

def dmm(x, y, w, h, terminals, title="DMM"):
    """Instrument block (e.g. DMM) with labelled terminals down the left edge.
    `terminals` is a list of (y, label)."""
    s = RECT(x, y, w, h, "inst", 6) + TXT(x + w / 2, y + h / 2 + 4, title, "blab", "middle")
    for ty, tl in terminals:
        s += T(x, ty) + TXT(x + 8, ty + 3, tl, "pin", "start")
    return s

def source_block(x, y, w, h, label):
    s = RECT(x, y, w, h, "blk", 6)
    for i, ln in enumerate(label.split("\n")):
        s += TXT(x + w / 2, y + h / 2 + 4 + (i - (len(label.split('\n')) - 1) / 2) * 16, ln, "blab", "middle")
    return s

def connector(x, y, w, h, label, pins):
    """Connector block with pins on the right edge. pins = list of names."""
    s = RECT(x, y, w, h, "conn", 3) + TXT(x + w / 2, y + h / 2 + 4, label, "blab", "middle")
    n = len(pins)
    for i, p in enumerate(pins):
        py = y + h * (i + 1) / (n + 1)
        s += L(x + w, py, x + w + 10, py, "wire") + T(x + w + 10, py) + TXT(x + w + 14, py + 3, p, "pin", "start")
    return s

def svg(inner, w, h):
    return f'<svg viewBox="0 0 {w} {h}" class="sch" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'

CSS = """
*{box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;color:#1a2230;margin:0;font-size:11.2px;line-height:1.5}
.wrap{padding:0 6px}
h1{font-size:23px;color:#1f4e79;margin:0 0 2px;border-bottom:3px solid #1f4e79;padding-bottom:6px}
h2{font-size:15.5px;color:#1f4e79;margin:22px 0 4px;border-bottom:1px solid #cdd9e6;padding-bottom:3px}
h3{font-size:12.5px;color:#2e5e8c;margin:14px 0 4px}
.sch{width:100%;height:auto;display:block;margin:6px 0 2px}
svg .wire{fill:none;stroke:#26384f;stroke-width:1.5}
svg .bus{fill:none;stroke:#26384f;stroke-width:1.3}
svg .contact{fill:none;stroke:#1f4e79;stroke-width:2.1;stroke-linecap:round}
svg .link{fill:none;stroke:#9aa6b8;stroke-width:1;stroke-dasharray:3 3}
svg .relaybox{fill:rgba(31,78,121,.035);stroke:#1f4e79;stroke-width:1.2;stroke-dasharray:5 4}
svg .term{fill:#1f4e79}
svg .coil{fill:#eaf2fb;stroke:#1f4e79;stroke-width:1.4}
svg .blk{fill:#f3f7fb;stroke:#1f4e79;stroke-width:1.4}
svg .conn{fill:#f3f7fb;stroke:#3f6f99;stroke-width:1.3}
svg .inst{fill:#fff6ea;stroke:#b5793b;stroke-width:1.6}
svg .brk{fill:none;stroke:#5a6b82;stroke-width:1.3}
svg text{font-family:Arial,Helvetica,sans-serif}
svg .lbl{font-size:12px;fill:#1a2230}
svg .pin{font-size:10px;fill:#52627a}
svg .blab{font-size:13px;font-weight:bold;fill:#1f3350}
svg .rtitle{font-size:11.5px;font-weight:bold;fill:#1f4e79}
svg .grp{font-size:12px;font-weight:bold;fill:#33445c}
svg .grpsub{font-size:10px;fill:#52627a}
svg .cap{font-size:10px;font-style:italic;fill:#6b7a90}
svg .capw{font-size:10px;font-style:italic;fill:#b3322f}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:10.3px}
th{background:#1f4e79;color:#fff;text-align:left;padding:5px 7px;border:1px solid #1f4e79}
td{border:1px solid #cdd9e6;padding:4px 7px;vertical-align:top}
tbody tr:nth-child(even){background:#eef3f9}
.avoid{break-inside:avoid;page-break-inside:avoid}
.vf{color:#b3322f;font-weight:bold}
"""

def html_page(svgs, title="Schematic"):
    body = "".join(f'<div class="avoid">{s}</div>' for s in svgs)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body><div class='wrap'><h1>{esc(title)}</h1>{body}</div></body></html>")

# ---- demo ---------------------------------------------------------------
def _demo():
    # AC (3-pole) through a 5 A relay to an AC source + motor; DC through a 1 A relay.
    s = bracket(150, 55, 300, "Power", "to load")
    ac = [60, 100, 140]
    for y in ac:
        s += TXT(158, y + 4, "AC", "lbl", "start")
    s += relay(ac, 235, 560, 360, 440, "5 A relay", "K1  (3-pole, N.O.)")
    s += source_block(640, 48, 150, 102, "AC\nSource")
    for y in ac:
        s += L(560, y, 640, y, "wire")
    s += L(715, 150, 715, 165, "wire") + instrument(715, 182, 17, "M", "Motor")
    dc = [255, 293]
    for y in dc:
        s += TXT(158, y + 4, "DC", "lbl", "start")
    s += relay(dc, 235, 560, 360, 440, "1 A relay", "K2  (2-pole, N.O.)")
    s += source_block(640, 248, 150, 64, "DC\nSource")
    for y in dc:
        s += L(560, y, 640, y, "wire")
    sheet = svg(s, 840, 360)
    with open("demo.html", "w") as f:
        f.write(html_page([sheet], "schematic_lib demo"))
    print("wrote demo.html  ->  node render_pdf.js demo.html demo.pdf")

if __name__ == "__main__":
    _demo()
