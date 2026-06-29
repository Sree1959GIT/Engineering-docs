# -*- coding: utf-8 -*-
"""
fixture_diagrammer.py — controlled, color-coded, zoned block/interconnect diagrams in matplotlib.

Adapted and extended from the "Automated Test Fixture Architect" engine (Gemini draft). Improvements:
  * equal aspect ratio so the grid is true-scale (1 unit square = 1 unit square),
  * a proper draw_relay() symbol (boundary + N.O./N.C. contacts + coil A1/A2 + pole/ref label) —
    the original engine had no relay symbol,
  * a small connect() convenience for orthogonal links with a class color.

Conventions baked in:
  Zoning  : power/sources left, switching/logic centre, instruments/targets right.
  Colors  : red=AC/DC power, blue=measurement/logic, orange=RF/coax, navy=physical harness.
  Routing : orthogonal (90-degree) segments; avoid crossing module boxes.

Run `python fixture_diagrammer.py` to save fixture_demo.png.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

CLASS_COLORS = {
    "power":   ("#c00000", "-"),   # AC mains / DC rails
    "dc":      ("#c00000", "--"),
    "signal":  ("#1f4e79", "-"),   # measurement / logic / control
    "rf":      ("#e07b00", "-"),   # RF / coax (use lw>=3)
    "harness": ("#003366", "-"),   # physical multicore (use lw>=4)
}


class FixtureDiagrammer:
    def __init__(self, title, width=100, height=100):
        self.fig, self.ax = plt.subplots(figsize=(16, 12))
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect("equal")          # true-scale grid
        self.ax.axis("off")
        self.ax.text(width / 2, height * 0.96, title, ha="center", va="center",
                     fontsize=18, fontweight="bold")
        self.legend_y = 5
        self._legend_started = False

    # --- blocks ---------------------------------------------------------
    def draw_smps(self, x, y, w, h, label):
        self.ax.add_patch(patches.Rectangle((x, y), w, h, facecolor="#fcf8e3", edgecolor="black", lw=2))
        self.ax.plot([x, x + w], [y, y + h], color="black", lw=1)
        self.ax.text(x + w * 0.25, y + h * 0.75, "~", fontsize=20, fontweight="bold", ha="center", va="center")
        self.ax.text(x + w * 0.75, y + h * 0.25, "=", fontsize=20, fontweight="bold", ha="center", va="center")
        self.ax.text(x + w / 2, y - 2, label, ha="center", va="top", fontsize=10, fontweight="bold")

    def draw_module(self, x, y, w, h, label, sub_label="", color="#e8f4f8", shape="box"):
        if shape == "mux":
            self.ax.add_patch(patches.Polygon([[x + w * 0.1, y], [x + w * 0.9, y], [x + w, y + h], [x, y + h]],
                                              facecolor=color, edgecolor="black", lw=2))
        elif shape == "round":
            self.ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                                     facecolor=color, edgecolor="black", lw=2))
        else:
            self.ax.add_patch(patches.Rectangle((x, y), w, h, facecolor=color, edgecolor="black", lw=2))
        self.ax.text(x + w / 2, y + h / 2 + (2 if sub_label else 0), label, ha="center", va="center",
                     fontsize=10, fontweight="bold")
        if sub_label:
            self.ax.text(x + w / 2, y + h / 2 - 2, sub_label, ha="center", va="center", fontsize=8)

    def draw_terminal_block(self, x, y, w, h, terminals, label):
        self.ax.add_patch(patches.Rectangle((x, y), w, h, facecolor="#eeeeee", edgecolor="black", lw=2))
        term_h = h / terminals
        for i in range(terminals):
            cy = y + i * term_h + term_h / 2
            self.ax.add_patch(patches.Circle((x + w / 2, cy), w * 0.25, facecolor="#b0b0b0",
                                             edgecolor="black", zorder=3))
        self.ax.text(x + w / 2, y - 2, label, ha="center", va="top", fontsize=10, fontweight="bold")

    def draw_instrument(self, x, y, r, sym, label=""):
        self.ax.add_patch(patches.Circle((x, y), r, facecolor="#fff6ea", edgecolor="#b5793b", lw=2, zorder=3))
        self.ax.text(x, y, sym, ha="center", va="center", fontsize=12, fontweight="bold", zorder=4)
        if label:
            self.ax.text(x, y - r - 1.5, label, ha="center", va="top", fontsize=8)

    def draw_relay(self, x, y, poles, name, ref, pitch=6, span=18, kind="NO"):
        """
        Relay/contactor with `poles` switched contacts. Top contact line at y; contacts step DOWN
        by `pitch`. Returns (in_x, out_x, [pole_y...]) so you can wire to/from it.
        """
        in_x, out_x = x, x + span
        ys = [y - i * pitch for i in range(poles)]
        gx = (in_x + out_x) / 2
        for cy in ys:
            self.ax.plot([in_x - 2, in_x], [cy, cy], color="#1f4e79", lw=1.5)
            self.ax.plot([out_x, out_x + 2], [cy, cy], color="#1f4e79", lw=1.5)
            self.ax.add_patch(patches.Circle((in_x, cy), 0.4, color="#1f4e79", zorder=4))
            self.ax.add_patch(patches.Circle((out_x, cy), 0.4, color="#1f4e79", zorder=4))
            if kind == "NC":
                self.ax.plot([in_x, out_x], [cy, cy], color="#1f4e79", lw=2.2)
            else:
                self.ax.plot([in_x, out_x - 0.3], [cy, cy + pitch * 0.55], color="#1f4e79", lw=2.2)
        coil_y = min(ys) - pitch * 1.4
        self.ax.plot([gx, gx], [min(ys) + pitch * 0.27, coil_y + 1.2], color="#9aa6b8", lw=1, ls=(0, (2, 2)))
        cw, ch = span * 0.5, pitch * 0.9
        self.ax.add_patch(patches.Rectangle((gx - cw / 2, coil_y - ch), cw, ch,
                                            facecolor="#eaf2fb", edgecolor="#1f4e79", lw=1.4, zorder=3))
        self.ax.text(gx - cw / 2 - 0.6, coil_y - ch / 2, "A1", ha="right", va="center", fontsize=7)
        self.ax.text(gx + cw / 2 + 0.6, coil_y - ch / 2, "A2", ha="left", va="center", fontsize=7)
        bx1, bx2 = in_x - 3, out_x + 3
        by_top, by_bot = max(ys) + pitch * 0.9, coil_y - ch - 1
        self.ax.add_patch(patches.Rectangle((bx1, by_bot), bx2 - bx1, by_top - by_bot,
                                            fill=False, edgecolor="#1f4e79", lw=1.1, ls=(0, (4, 3)), zorder=2))
        self.ax.text((bx1 + bx2) / 2, by_top + 0.8, name, ha="center", va="bottom",
                     fontsize=9, fontweight="bold", color="#1f4e79")
        self.ax.text((bx1 + bx2) / 2, by_bot - 1.2, ref, ha="center", va="top", fontsize=7, color="#52627a")
        return in_x, out_x, ys

    # --- routing & legend ----------------------------------------------
    def route_orthogonal(self, x1, y1, x2, y2, cls="signal", label="", drop_y=None, lw=None):
        color, style = CLASS_COLORS.get(cls, ("#26384f", "-"))
        if lw is None:
            lw = 4 if cls == "harness" else 3 if cls == "rf" else 2
        if drop_y is not None:
            self.ax.plot([x1, x1, x2, x2], [y1, drop_y, drop_y, y2], color=color, ls=style, lw=lw)
            if label:
                self.ax.text((x1 + x2) / 2, drop_y + 1, label, ha="center", va="bottom",
                             fontsize=8, fontweight="bold", color=color)
        else:
            mid = (x1 + x2) / 2
            self.ax.plot([x1, mid, mid, x2], [y1, y1, y2, y2], color=color, ls=style, lw=lw)
            if label:
                self.ax.text(mid, max(y1, y2) + 1, label, ha="center", va="bottom",
                             fontsize=8, fontweight="bold", color=color)

    def add_legend_item(self, cls, label):
        color, style = CLASS_COLORS.get(cls, ("#26384f", "-"))
        lw = 4 if cls == "harness" else 3 if cls == "rf" else 2
        if not self._legend_started:
            self.ax.add_patch(patches.Rectangle((2, 2), 30, 14, facecolor="white", edgecolor="black", lw=1.2, zorder=5))
            self.ax.text(17, 14, "Wiring Legend", ha="center", va="center", fontweight="bold", zorder=6)
            self._legend_started = True
        self.legend_y += 2
        self.ax.plot([4, 8], [self.legend_y, self.legend_y], color=color, ls=style, lw=lw, zorder=6)
        self.ax.text(9, self.legend_y, label, va="center", fontsize=8, zorder=6)

    def save(self, filename, dpi=300):
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")
        plt.close(self.fig)


def _demo():
    d = FixtureDiagrammer("Test Fixture — Block Diagram (demo)")
    d.draw_smps(6, 60, 16, 16, "AC/DC Supply")
    d.draw_module(6, 30, 16, 14, "DUT", "controller", color="#e8f4f8")
    inx, outx, ys = d.draw_relay(46, 70, poles=3, name="5 A relay", ref="K1 (3-pole, N.O.)")
    d.draw_module(44, 30, 18, 14, "Switch\nMatrix", color="#eef4fb")
    d.draw_instrument(86, 64, 4, "DMM", "meter")
    d.draw_module(80, 30, 16, 14, "Target", color="#f3f7fb")
    d.route_orthogonal(22, 68, 46, ys[0], cls="power", label="AC")
    d.route_orthogonal(outx, ys[0], 82, 64, cls="signal", label="meas")
    d.route_orthogonal(22, 36, 44, 36, cls="harness", label="DB25")
    d.route_orthogonal(62, 36, 80, 36, cls="rf", label="coax")
    d.add_legend_item("power", "AC/DC power")
    d.add_legend_item("signal", "measurement/logic")
    d.add_legend_item("rf", "RF/coax")
    d.add_legend_item("harness", "harness/multicore")
    d.save("fixture_demo.png")
    print("wrote fixture_demo.png")


if __name__ == "__main__":
    _demo()
