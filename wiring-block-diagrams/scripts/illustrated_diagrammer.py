# -*- coding: utf-8 -*-
"""
illustrated_diagrammer.py - "Illustrated / pictorial" output tier.

Draws vector icons that resemble real component silhouettes (AC outlet, screw-terminal power
module, relay/PCB module, DIN-rail terminal strip) instead of plain rectangles - closer to a
professional CAD/product-illustration look than the plain block tier, while every label/pin
stays hand-coded from confirmed data (see references/tools.md "Output tiers"). This is NOT
photorealistic AI image generation - no detail is generated that wasn't explicitly passed in.

Run `python illustrated_diagrammer.py` to save illustrated_demo.png (the SMPS / Numato relay /
DIN-rail terminal-block worked example used to validate this tier).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class IllustratedDiagrammer:
    def __init__(self, title, width=150, height=75):
        self.fig, self.ax = plt.subplots(figsize=(width / 10, height / 10))
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.ax.text(width / 2, height * 0.96, title, ha="center", va="center",
                     fontsize=13, fontweight="bold")
        self._legend_started = False
        self._legend_y = 2

    # --- component icons -------------------------------------------------
    def draw_ac_outlet(self, x, y, label="AC Power Outlet\n(120VAC Input)"):
        """Duplex receptacle icon (two slots + ground hole per gang)."""
        ax = self.ax
        ax.add_patch(patches.FancyBboxPatch((x, y), 14, 16, boxstyle="round,pad=0.6",
                                             facecolor="#f2f2f2", edgecolor="black", lw=1.5))
        for dy in (11, 3.5):
            ax.add_patch(patches.Circle((x + 7, y + dy), 4.2, facecolor="white", edgecolor="black", lw=1.2))
            ax.add_patch(patches.Rectangle((x + 5.3, y + dy + 1), 0.7, 3, facecolor="black"))
            ax.add_patch(patches.Rectangle((x + 8, y + dy + 1), 0.7, 3, facecolor="black"))
            ax.add_patch(patches.Circle((x + 7, y + dy - 1.7), 0.6, facecolor="black"))
        ax.text(x + 7, y - 2.5, label, ha="center", va="top", fontsize=8, fontweight="bold")
        return (x, y, 14, 16)

    def draw_power_module(self, x, y, w, h, tag, part="", func="",
                           in_labels=("IN1", "IN2"), out_labels=("OUT1", "OUT2")):
        """Enclosed power-supply/converter icon: chassis body + green screw-terminal strips
        top and bottom, matching real SMPS module terminal blocks."""
        ax = self.ax
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor="#e8e8e8", edgecolor="black", lw=1.5))
        ax.add_patch(patches.Rectangle((x, y + h - 2.2), w, 2.2, facecolor="#2e7d32", edgecolor="black", lw=0.8))
        ax.add_patch(patches.Rectangle((x, y), w, 2.2, facecolor="#2e7d32", edgecolor="black", lw=0.8))
        for i in range(4):
            ax.add_patch(patches.Circle((x + 2 + i * (w - 4) / 3, y + h - 1.1), 0.5,
                                         facecolor="#c9c9c9", edgecolor="black", lw=0.5))
            ax.add_patch(patches.Circle((x + 2 + i * (w - 4) / 3, y + 1.1), 0.5,
                                         facecolor="#c9c9c9", edgecolor="black", lw=0.5))
        ax.text(x + w / 2, y + h + 5, f"{tag}\n{part}", ha="center", va="bottom",
                fontsize=8, fontweight="bold")
        ax.text(x + 2, y + h - 3.6, in_labels[0], ha="left", va="center", fontsize=7)
        ax.text(x + 2, y + 2.5, in_labels[1], ha="left", va="center", fontsize=7)
        ax.text(x + w - 2, y + h - 3.6, out_labels[0], ha="right", va="center", fontsize=7)
        ax.text(x + w - 2, y + 2.5, out_labels[1], ha="right", va="center", fontsize=7)
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=7)
        return (x, y, w, h)

    def draw_relay_module(self, x, y, w, h, tag, part="", func="", channels=2,
                           conn_labels=("COM", "NO", "NC")):
        """PCB-style relay/USB module icon: rounded board, USB connector glyph, N relay
        squares, green screw-terminal blocks for power-in (left) and switched output (right)."""
        ax = self.ax
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4",
                                             facecolor="white", edgecolor="black", lw=1.5))
        ax.text(x + w / 2, y + h + 4, f"{tag}\n{part}", ha="center", va="bottom",
                fontsize=8, fontweight="bold")
        for c in range(min(channels, 4)):
            cy = y + h - 8 - c * 7
            ax.add_patch(patches.Rectangle((x + 3, cy), 8, 5, facecolor="#111111"))
            ax.text(x + 7, cy + 2.5, f"K{c + 1}", ha="center", va="center", fontsize=5.5, color="white")
        ax.add_patch(patches.Rectangle((x + 1, y + h - 5), 3, 2.2, facecolor="#888888"))
        ax.text(x + 1.5, y + h - 7, "USB Control\n(to PC)", ha="left", va="top", fontsize=6.5)
        ax.add_patch(patches.Rectangle((x - 3, y + 1), 3, 6, facecolor="#2e7d32", edgecolor="black", lw=0.8))
        ax.text(x - 3.5, y + 8, "Power Input\nConnector", ha="right", va="bottom", fontsize=6.5)
        ax.add_patch(patches.Rectangle((x + w, y + h / 2 - 4.5), 3, 9, facecolor="#2e7d32", edgecolor="black", lw=0.8))
        for i, lbl in enumerate(conn_labels):
            ax.text(x + w + 4, y + h / 2 + 3 - i * 2.5, lbl, ha="left", va="center", fontsize=6.5)
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=6.5)
        return (x, y, w, h)

    def draw_din_rail_terminal_strip(self, x, y, n=4, tag="TB"):
        """DIN-rail mounted terminal block strip: gray rail + n numbered screw terminals."""
        ax = self.ax
        w = 6.5 * n + 4
        ax.add_patch(patches.Rectangle((x - 2, y + 2), w, 3, facecolor="#aaaaaa", edgecolor="black", lw=1))
        for i in range(n):
            cx = x + 3 + i * 6.5
            ax.add_patch(patches.Rectangle((cx - 2.5, y + 5), 5, 10, facecolor="#f5f5f5", edgecolor="black", lw=1))
            ax.add_patch(patches.Circle((cx, y + 13), 1.6, facecolor="#c9c9c9", edgecolor="black", lw=0.8))
            ax.plot([cx - 1, cx + 1], [y + 13, y + 13], color="black", lw=0.8)
            ax.text(cx, y + 15.5, str(i + 1), ha="center", va="bottom", fontsize=7, fontweight="bold")
        ax.text(x + w / 2 - 2, y + 23, tag, ha="center", va="bottom", fontsize=8, fontweight="bold")
        return (x, y, w, 18)

    def draw_generic_pcb(self, x, y, w, h, tag, part="", func=""):
        """Fallback icon for any module without a dedicated shape: green PCB silhouette
        with dark chip-outline blocks, still visually distinct from the other categories."""
        ax = self.ax
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor="#2e6b3e", edgecolor="black", lw=1.5))
        for i in range(3):
            ax.add_patch(patches.Rectangle((x + 2 + i * (w / 3), y + 2), w / 3 - 2, h - 4,
                                            facecolor="#1c1c1c", edgecolor="#444444", lw=0.5))
        ax.text(x + w / 2, y + h + 4, f"{tag}\n{part}", ha="center", va="bottom",
                fontsize=8, fontweight="bold")
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=6.5)
        return (x, y, w, h)

    # --- wiring & legend ---------------------------------------------------
    def wire(self, x1, y1, x2, y2, color, lw=2, label=""):
        self.ax.plot([x1, x2], [y1, y2], color=color, lw=lw, solid_capstyle="round", zorder=2)
        if label:
            self.ax.text((x1 + x2) / 2, max(y1, y2) + 1, label, ha="center", va="bottom",
                         fontsize=7, fontweight="bold", color=color)

    def add_legend_item(self, color, label):
        if not self._legend_started:
            self.ax.add_patch(patches.Rectangle((2, 2), 42, 13, facecolor="white", edgecolor="black", lw=1.2, zorder=5))
            self._legend_started = True
            self._legend_y = 11
        self.ax.plot([4, 8], [self._legend_y, self._legend_y], color=color, lw=3, zorder=6)
        self.ax.text(9, self._legend_y, label, va="center", fontsize=7, zorder=6)
        self._legend_y -= 3.4

    def save(self, filename, dpi=200):
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")
        plt.close(self.fig)


def _demo():
    d = IllustratedDiagrammer("System Block Diagram: SMPS, Numato Relay, and Terminal Block Connection",
                              width=150, height=75)
    d.draw_ac_outlet(6, 38)
    d.draw_power_module(26, 40, 26, 14, "SMPS", "Mean Well LRS-35-5",
                         in_labels=("AC L", "AC N"), out_labels=("+5VDC", "V-"))
    d.draw_relay_module(62, 38, 30, 20, "Numato Lab 2 Channel", "USB Relay Module", channels=2)
    d.draw_din_rail_terminal_strip(118, 40, n=4, tag="Terminal Block Strip (DIN Rail Mounted)")
    d.wire(20, 49, 26, 47, "black", lw=2)
    d.wire(20, 41.5, 26, 42.5, "black", lw=2)
    d.wire(52, 47, 59, 44, "#2e7d32", lw=2, label="+5VDC")
    d.wire(52, 42.5, 59, 41, "black", lw=2, label="GND")
    d.wire(95, 53, 118, 51, "#a00000", lw=2.2, label="Switched 120VAC L")
    d.add_legend_item("#a00000", "120VAC L (Line)")
    d.add_legend_item("black", "120VAC N (Neutral) / GND")
    d.add_legend_item("#2e7d32", "+5VDC")
    d.save("illustrated_demo.png")
    print("wrote illustrated_demo.png")


if __name__ == "__main__":
    _demo()
