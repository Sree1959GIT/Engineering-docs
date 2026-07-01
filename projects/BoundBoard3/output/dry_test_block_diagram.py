"""
BoundBoard3 dry-test block diagram (3-component Phase 4/5 walkthrough) - Rev 2.

Draws the three components confirmed in the Gate 2 packaging report as
category-distinguishable blocks (see wiring-block-diagrams/references/conventions.md,
"Block differentiation"): a power supply (rounded, red), a relay/switching module
(dashed, blue), and an interface/adapter module (rounded, gray).

Rev 2 additionally applies the CAD-grade notation added after the Rev 1 review:
  - ISO 128 line weights (thick continuous = main power, thin continuous = control/signal)
  - Pin-side orientation (power in at top, signal flow left->right)
  - Off-page connectors for signals that continue beyond this partial 3-block diagram
  - A title block (title, unit/system ID, revision, date, scale, provenance)
"""
import sys
import os
import matplotlib.patches as patches

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..",
                                 "wiring-block-diagrams", "scripts"))
from fixture_diagrammer import FixtureDiagrammer  # noqa: E402

d = FixtureDiagrammer("BoundBoard3 - Dry Test Block Diagram (3 components)", width=120, height=75)

# --- SMPS1 - power supply (left, per zoning convention) ---------------------
d.draw_categorized_block(
    6, 38, 22, 18,
    tag="B3SMPS1",
    category="power",
    part="MEAN WELL RT-125D",
    func="AC-DC supply, 5V/12V/24V out",
)
# Pin-side orientation: power supply takes mains in at the TOP.
d.ax.annotate("", xy=(17, 56), xytext=(17, 62),
              arrowprops=dict(arrowstyle="-|>", color="#a00000", lw=1.8))
d.ax.text(17, 63, "L / N / PE (AC MAINS)", ha="center", va="bottom",
          fontsize=8, fontweight="bold", color="#a00000")

# --- Numato 32ch relay board - relay/switching module (centre) --------------
d.draw_categorized_block(
    40, 38, 24, 18,
    tag="B3RL1",
    category="relay",
    part="Numato 32-ch Relay [VERIFY interface]",
    func="Relay matrix - top-probe switching",
)

# --- TI UCD interface adapter - interface/adapter module (right) ------------
d.draw_categorized_block(
    76, 38, 20, 18,
    tag="JF3 / UCD",
    category="interface",
    part="TI USB-to-I2C [VERIFY model]",
    func="USB<->I2C/PMBus bridge",
)

# --- Connectivity: ISO 128 line weights (main=thick, control=thin) ----------
# Main power path: SMPS -> relay board (thick continuous per ISO 128 "main")
d.route_orthogonal(28, 47, 40, 47, cls="power", label="12VDC", lw=4)
# Control/signal path: relay board -> UCD interface (thin continuous per ISO 128 "control")
d.route_orthogonal(64, 47, 76, 47, cls="signal", label="SCL/SDA/GND", lw=1.2)

# --- Off-page connectors: signals that continue beyond this 3-block excerpt -
# The relay board's real job is switching top-probe test points elsewhere on the
# full board (out of scope for this 3-component dry test) - show it leaving the page.
d.draw_offpage_connector(52, 34, "TOP PROBES", direction="out", w=8)
# The UCD interface's I2C/PMBus bus continues to the target UCD power-controller IC,
# which is not one of the 3 components in this dry test - show it leaving the page.
d.draw_offpage_connector(98, 34, "UCD IC (PMBus)", direction="out", w=8)

d.add_legend_item("power", "Main power (thick, ISO128 continuous-thick)")
d.add_legend_item("signal", "Control/signal (thin, ISO128 continuous-thin)")

# --- Title block (conventions.md "Title block") ------------------------------
tb_x, tb_y, tb_w, tb_h = 55, 2, 43, 16
d.ax.add_patch(patches.Rectangle(
    (tb_x, tb_y), tb_w, tb_h, facecolor="white", edgecolor="black", lw=1.2, zorder=5))
title_lines = [
    ("Title:", "BoundBoard3 - Dry Test Block Diagram"),
    ("Unit / System ID:", "BoundBoard3 (BB3) - 3-component excerpt"),
    ("Revision:", "Rev 2 - CAD-grade notation applied"),
    ("Scale:", "Schematic - not to physical scale"),
    ("Provenance:", "Drawn from user-approved Gate 2 packaging report; [VERIFY] items open"),
]
for i, (k, v) in enumerate(title_lines):
    ty = tb_y + tb_h - 2 - i * 2.8
    d.ax.text(tb_x + 1, ty, k, ha="left", va="top", fontsize=7, fontweight="bold", zorder=6)
    d.ax.text(tb_x + 1, ty - 1.3, v, ha="left", va="top", fontsize=7, zorder=6)

d.save(os.path.join(os.path.dirname(__file__), "dry_test_block_diagram.png"))
print("wrote dry_test_block_diagram.png")
