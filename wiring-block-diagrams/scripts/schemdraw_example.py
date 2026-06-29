# -*- coding: utf-8 -*-
"""
schemdraw_example.py — the "standard symbols, least effort" path.

schemdraw ships recognised electrical symbols (sources, switches, relays, meters), so a simple
relay-switched circuit needs very little code. Use this when you want a conventional schematic look
without hand-placing every line.

Install: pip install --break-system-packages schemdraw
Run    : python schemdraw_example.py   -> writes schemdraw_demo.svg and .png
"""
import schemdraw
import schemdraw.elements as elm


def build():
    with schemdraw.Drawing(file="schemdraw_demo.svg", show=False) as d:
        d.config(unit=2.4)
        # AC source -> relay (switched contact) -> motor load, with the coil energised from a control pair.
        src = d.add(elm.SourceSin().up().label("AC\nSource", loc="left"))
        d.add(elm.Line().right().length(1.2))
        rly = d.add(elm.Relay(unit=2).right().label("K1\n5 A", loc="top"))
        d.add(elm.Line().right().length(1.2))
        d.add(elm.Motor().down().label("M", loc="right"))
        d.add(elm.Line().left().tox(src.start))
        d.add(elm.Line().up().toy(src.start))
    # also export PNG for embedding in docs
    with schemdraw.Drawing(file="schemdraw_demo.png", show=False) as d:
        d.config(unit=2.4)
        src = d.add(elm.SourceSin().up().label("AC\nSource", loc="left"))
        d.add(elm.Line().right().length(1.2))
        d.add(elm.Relay(unit=2).right().label("K1\n5 A", loc="top"))
        d.add(elm.Line().right().length(1.2))
        d.add(elm.Motor().down().label("M", loc="right"))
        d.add(elm.Line().left().tox(src.start))
        d.add(elm.Line().up().toy(src.start))
    print("wrote schemdraw_demo.svg and schemdraw_demo.png")


if __name__ == "__main__":
    build()
