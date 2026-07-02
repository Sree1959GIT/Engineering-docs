# -*- coding: utf-8 -*-
"""
bb3_system_diagram.py — BB3 system block diagram: TB-1 terminal block, SMPS1/SMPS2,
Numato 32-ch relay board (B3RL1), JTAG mux (JP6/TAP1), and GPIO/USB-to-serial interface.

Source data: _MPPOsc_mux_Wiring_List.xlsx, BB3_WIRING_DIAGRAM_03_10_2025.xlsx,
SCHEMATICSBB3260626.xlsx (tabs: TB WIRING, DB CONNECTOR, BB3 SUNRISE, GPIO, JTAG MUX).

No inter-module power/signal wire is drawn between modules 2-3, 3-4, or 4-5 because the
source wiring lists do not document a direct connection there.
"""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from fixture_diagrammer import FixtureDiagrammer

d = FixtureDiagrammer(
    "SYSTEM BLOCK DIAGRAM: BB3 POWER, RELAY, JTAG MUX & SERIAL INTERFACE",
    width=230, height=110,
)
d.fig.set_size_inches(23, 11)

# --- Zone 1: TB-1 terminal block (230V AC input) ---------------------------
d.draw_terminal_block(6, 55, 8, 42, 6, "TB-1 Terminal Block\n(230V AC Input)")
term_h = 42 / 6
term_y = [55 + i * term_h + term_h / 2 for i in range(6)]
# pin1-3: 230V PH (top three, index 3-5), pin4-6: 230V NEUTRAL (bottom three, index 0-2)
ph_mid = sum(term_y[3:6]) / 3
neu_mid = sum(term_y[0:3]) / 3
d.ax.text(2, ph_mid, "230V PH", ha="center", va="center", fontsize=7, rotation=90)
d.ax.text(2, neu_mid, "230V NEUTRAL", ha="center", va="center", fontsize=7, rotation=90)

# --- Zone 2: SMPS1 / SMPS2 --------------------------------------------------
d.draw_smps(28, 78, 18, 16, "SMPS1 (RT125D)")
d.draw_smps(28, 55, 18, 16, "SMPS2 (LM15-23B03)")
d.ax.text(37, 94.5, "AC-P", ha="center", fontsize=7)
d.ax.text(37, 76.5, "AC-N", ha="center", fontsize=7)
d.ax.text(37, 71.5, "AC-P", ha="center", fontsize=7)
d.ax.text(37, 53.5, "AC-N", ha="center", fontsize=7)

# Phase (red) TB-1 pins 1-3 -> SMPS1/SMPS2 AC-P; Neutral (blue) pins 4-6 -> AC-N
d.route_orthogonal(14, term_y[5], 28, 94, cls="power", label="B3SMPS1-ACP", drop_y=94)
d.route_orthogonal(14, term_y[4], 28, 71, cls="power", label="B3SMPS2-ACP", drop_y=71)
d.route_orthogonal(14, term_y[2], 28, 78, cls="dc", label="B3SMPS1-ACN", drop_y=78)
d.route_orthogonal(14, term_y[1], 28, 55, cls="dc", label="B3SMPS2-ACN", drop_y=55)

def labeled_box(ax, x, y, w, h, title, sub_label, color):
    ax.add_patch(patches.Rectangle((x, y), w, h, facecolor=color, edgecolor="black", lw=2))
    ax.text(x + w / 2, y + h - 3, title, ha="center", va="top", fontsize=10, fontweight="bold")
    ax.text(x + w / 2, y + h - 9, sub_label, ha="center", va="top", fontsize=7, color="#555555")


import matplotlib.patches as patches

# --- Zone 3: Numato 32-ch relay board (B3RL1) -------------------------------
rx, ry0, rw, rh = 64, 40, 26, 55
labeled_box(d.ax, rx, ry0, rw, rh, "Numato 32-CH\nRelay Board (B3RL1)",
            "DB25A connector, channels K4-K8", "#eef6ee")
relay_channels = [("K4", "TP10"), ("K5", "TP16"), ("K6", "TP13"), ("K7", "TP6"), ("K8", "TP9")]
pin_top = ry0 + rh - 16
ry = [pin_top - i * 7 for i in range(5)]
for (ch, tp), y in zip(relay_channels, ry):
    d.ax.text(rx + 2, y, ch, ha="left", va="center", fontsize=8, fontweight="bold")
    d.route_orthogonal(rx + 6, y, rx + rw + 24, y, cls="signal", lw=1.5)
    d.ax.text(rx + rw + 26, y, tp, ha="left", va="center", fontsize=8)

# --- Zone 4: JTAG MUX (JP6 / TAP1) ------------------------------------------
jx, jy0, jw, jh = 126, 35, 22, 60
labeled_box(d.ax, jx, jy0, jw, jh, "JTAG MUX\n(JP6 / TAP1)", "Xilinx PT USB-II <-> TAP1",
            "#eef2fb")
jtag_pins = [("VREF", "Vcc"), ("TDI", "U1-IP-3"), ("TCK", "U1-IP-4"),
             ("TMS", "U1-IP-5"), ("TDO", "U1-IP-6"), ("GND", "Gnd")]
jpin_top = jy0 + jh - 18
jy = [jpin_top - i * 6.5 for i in range(6)]
for (pin, dest), y in zip(jtag_pins, jy):
    d.ax.text(jx + 2, y, pin, ha="left", va="center", fontsize=7, fontweight="bold")
    d.route_orthogonal(jx + 8, y, jx + jw + 12, y, cls="signal", lw=1.2)
    d.ax.text(jx + jw + 14, y, dest, ha="left", va="center", fontsize=7)

# --- Zone 5: GPIO / USB-to-serial interface --------------------------------
gx, gw, gh = 188, 26, 32
labeled_box(d.ax, gx, 68, gw, gh, "J5\n(USB-to-Serial)", "RX/TX/GND -> DB9F", "#fdf3e7")
j5_pins = [("RX", "DB9F.2 TX"), ("TX", "DB9F.3 RX"), ("GND", "DB9F.5 GND")]
j5_top = 68 + gh - 16
j5y = [j5_top - i * 7 for i in range(3)]
for (pin, dest), y in zip(j5_pins, j5y):
    d.ax.text(gx + 2, y, f"{pin} -> {dest}", ha="left", va="center", fontsize=7, fontweight="bold")

labeled_box(d.ax, gx, 30, gw, gh, "JF3\n(UCD)", "SCL/SDA/GND -> DB9F", "#fdf3e7")
jf3_pins = [("SCL", "DB9F-3"), ("SDA", "DB9F-2"), ("GND", "DB9F-5")]
jf3_top = 30 + gh - 16
jf3y = [jf3_top - i * 7 for i in range(3)]
for (pin, dest), y in zip(jf3_pins, jf3y):
    d.ax.text(gx + 2, y, f"{pin} -> {dest}", ha="left", va="center", fontsize=7, fontweight="bold")

# --- legend ------------------------------------------------------------------
d.add_legend_item("signal", "signal / relay / JTAG wiring")
d.add_legend_item("dc", "230V Neutral")
d.add_legend_item("power", "230V Phase / AC Line")

d.ax.text(105, 5, "Source: wiring-list Excel exports (TB WIRING, DB CONNECTOR, BB3 SUNRISE, GPIO, JTAG MUX tabs). "
                  "Modules 2-5 shown independently; no inter-module link is documented in source.",
          ha="center", fontsize=8, color="#555555")

d.save("/home/user/Engineering-docs/generated_imgs/bb3_system_block_diagram.png")
print("wrote bb3_system_block_diagram.png")
