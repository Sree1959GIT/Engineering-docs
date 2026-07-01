# -*- coding: utf-8 -*-
"""
illustrated_diagrammer.py - "Illustrated / pictorial" output tier.

Draws vector icons that resemble real component silhouettes (AC outlet, screw-terminal power
module, relay/PCB module, DIN-rail terminal strip) instead of plain rectangles - closer to a
professional CAD/product-illustration look than the plain block tier, while every label/pin
stays hand-coded from confirmed data (see references/tools.md "Output tiers"). This is NOT
photorealistic AI image generation - no detail is generated that wasn't explicitly passed in.

Routing discipline: `wire()` always draws a strictly orthogonal (90-degree) path and callers are
expected to assign each signal a consistent y-lane across the whole diagram so parallel wires
never cross (see references/conventions.md "Routing & layout").

Run `python illustrated_diagrammer.py` to save illustrated_demo.png (the SMPS / Numato relay /
DIN-rail terminal-block worked example used to validate this tier).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def _shade_rect(ax, x, y, w, h, base_color, bands=5, lighten=0.12, **kw):
    """Simple brushed-metal / chassis shading: stacked horizontal bands, alternating lighter
    and darker than base_color, to suggest a real enclosure surface without a raster gradient."""
    import matplotlib.colors as mcolors
    r, g, b = mcolors.to_rgb(base_color)
    band_h = h / bands
    for i in range(bands):
        f = lighten if i % 2 == 0 else -lighten * 0.6
        shade = tuple(min(1, max(0, c + f)) for c in (r, g, b))
        ax.add_patch(patches.Rectangle((x, y + i * band_h), w, band_h, facecolor=shade,
                                        edgecolor="none", zorder=kw.get("zorder", 1)))
    ax.add_patch(patches.Rectangle((x, y), w, h, fill=False, edgecolor="black",
                                    lw=kw.get("lw", 1.5), zorder=kw.get("zorder", 1) + 1))


def _shadow(ax, patch_fn, dx=0.6, dy=-0.6, alpha=0.18):
    """Draw a soft drop-shadow copy of a patch-producing callback, offset down-right."""
    import matplotlib.transforms as mtransforms
    shadow_patch = patch_fn()
    shadow_patch.set_facecolor("black")
    shadow_patch.set_edgecolor("none")
    shadow_patch.set_alpha(alpha)
    shadow_patch.set_zorder(0)
    offset = mtransforms.Affine2D().translate(dx, dy) + ax.transData
    shadow_patch.set_transform(offset)
    ax.add_patch(shadow_patch)


class IllustratedDiagrammer:
    def __init__(self, title, width=160, height=90):
        self.fig, self.ax = plt.subplots(figsize=(width / 10, height / 10))
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.ax.text(width / 2, height * 0.97, title, ha="center", va="center",
                     fontsize=14, fontweight="bold")
        self._legend_started = False
        self._legend_y = 2

    # --- component icons -------------------------------------------------
    def draw_ac_outlet(self, x, y, label="AC Power Outlet\n(120VAC Input)", w=16, h=20):
        """NEMA 5-15 duplex receptacle wall plate: two outlet faces, each with polarized
        blade slots and a U-shaped ground pin, plus wall-plate mounting screws."""
        ax = self.ax
        ax.add_patch(patches.FancyBboxPatch((x + 0.5, y - 0.5), w, h, boxstyle="round,pad=0.3",
                     facecolor="black", edgecolor="none", alpha=0.15, zorder=0))
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5",
                     facecolor="#f4f2ec", edgecolor="#555555", lw=1.4, zorder=1))
        ax.add_patch(patches.Circle((x + w / 2, y + h - 1.2), 0.35, facecolor="#888888", zorder=2))
        ax.add_patch(patches.Circle((x + w / 2, y + 1.2), 0.35, facecolor="#888888", zorder=2))
        cx = x + w / 2
        for dy in (h * 0.68, h * 0.22):
            cy = y + dy
            ax.add_patch(patches.Circle((cx, cy), w * 0.32, facecolor="#fbfbfb",
                                         edgecolor="#333333", lw=1.1, zorder=2))
            # polarized blade slots (one taller = neutral, one shorter = line)
            ax.add_patch(patches.Rectangle((cx - w * 0.13, cy + 0.3), w * 0.09, 2.6,
                                            facecolor="#1a1a1a", zorder=3))
            ax.add_patch(patches.Rectangle((cx + w * 0.05, cy + 0.6), w * 0.09, 2.0,
                                            facecolor="#1a1a1a", zorder=3))
            # U-shaped ground pin
            ax.add_patch(patches.Arc((cx, cy - 2.6), 2.4, 2.4, angle=0, theta1=200, theta2=340,
                                      color="#1a1a1a", lw=1.8, zorder=3))
        ax.text(x + w / 2, y - 2.5, label, ha="center", va="top", fontsize=8, fontweight="bold")
        return {"bbox": (x, y, w, h),
                "line_out": (x + w, y + h * 0.68),
                "neutral_out": (x + w, y + h * 0.22)}

    def draw_power_module(self, x, y, w, h, tag, part="", func="",
                           in_labels=("IN1", "IN2"), out_labels=("OUT1", "OUT2")):
        """Enclosed chassis-mount power-supply icon: brushed-metal body, cooling vents, a
        label sticker, and green screw-terminal blocks on the LEFT edge (input) and RIGHT
        edge (output) - mirrors the pin-side orientation convention (input left, output
        right) so lane-based wiring never has to cross the case body."""
        ax = self.ax
        _shadow(ax, lambda: patches.Rectangle((x, y), w, h))
        _shade_rect(ax, x, y, w, h, "#c9c9c9", bands=6, lighten=0.10, zorder=1)
        # cooling vents (centre of the case face)
        for i in range(5):
            vx = x + w * 0.42 + i * 1.4
            ax.add_patch(patches.Rectangle((vx, y + h * 0.32), 0.45, h * 0.36,
                                            facecolor="#8a8a8a", zorder=3))
        # label sticker
        ax.add_patch(patches.Rectangle((x + w * 0.06, y + h * 0.68), w * 0.28, h * 0.2,
                                        facecolor="white", edgecolor="#999999", lw=0.6, zorder=3))
        for i in range(2):
            ax.plot([x + w * 0.08, x + w * 0.3], [y + h * 0.74 + i * h * 0.07] * 2,
                    color="#bbbbbb", lw=0.8, zorder=4)
        pins = {}
        # LEFT edge: input terminal block (stacked, 2 pins)
        ax.add_patch(patches.Rectangle((x - 3, y + h * 0.2), 3, h * 0.6, facecolor="#1e5e2b",
                                        edgecolor="black", lw=0.8, zorder=3))
        for i, lbl in enumerate(in_labels):
            py = y + h * 0.68 - i * h * 0.36
            ax.add_patch(patches.Circle((x - 1.5, py), 0.5, facecolor="#d9d9d9",
                                         edgecolor="black", lw=0.5, zorder=4))
            ax.text(x - 3.5, py, lbl, ha="right", va="center", fontsize=6.5, fontweight="bold", zorder=5)
            pins[f"in_{i}"] = (x - 3, py)
        # RIGHT edge: output terminal block (stacked, 2 pins)
        ax.add_patch(patches.Rectangle((x + w, y + h * 0.2), 3, h * 0.6, facecolor="#1e5e2b",
                                        edgecolor="black", lw=0.8, zorder=3))
        for i, lbl in enumerate(out_labels):
            py = y + h * 0.68 - i * h * 0.36
            ax.add_patch(patches.Circle((x + w + 1.5, py), 0.5, facecolor="#d9d9d9",
                                         edgecolor="black", lw=0.5, zorder=4))
            ax.text(x + w + 3.5, py, lbl, ha="left", va="center", fontsize=6.5, fontweight="bold", zorder=5)
            pins[f"out_{i}"] = (x + w + 3, py)
        ax.text(x + w / 2, y + h + 5, f"{tag}\n{part}", ha="center", va="bottom",
                fontsize=8.5, fontweight="bold", zorder=5)
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=7, zorder=5)
        pins["bbox"] = (x, y, w, h)
        return pins

    def draw_relay_module(self, x, y, w, h, tag, part="", func="", channels=2,
                           conn_labels=("COM", "NO", "NC")):
        """PCB-style relay/USB module icon: green FR4 board with silkscreen text, a micro-USB
        connector, blue/black relay bodies, LED indicators, mounting holes, and green
        screw-terminal blocks for power-in (left) and switched output (right)."""
        ax = self.ax
        _shadow(ax, lambda: patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4"))
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4",
                     facecolor="#1a6b3a", edgecolor="#0d3d20", lw=1.6, zorder=1))
        # faint PCB trace lines for texture
        for i in range(4):
            ax.plot([x + 2, x + w - 2], [y + 3 + i * (h - 8) / 4] * 2,
                    color="#2c8250", lw=0.5, alpha=0.6, zorder=2)
        # mounting holes
        for cx_, cy_ in ((x + 2, y + 2), (x + w - 2, y + 2), (x + 2, y + h - 2), (x + w - 2, y + h - 2)):
            ax.add_patch(patches.Circle((cx_, cy_), 0.7, facecolor="#0d3d20", edgecolor="#c9c9c9",
                                         lw=0.6, zorder=3))
        ax.text(x + w / 2, y + h - 2.5, "NUMATO LAB", ha="center", va="top", fontsize=6.5,
                fontweight="bold", color="white", zorder=3)
        # micro-USB connector (top-left)
        ax.add_patch(patches.Rectangle((x + 2, y + h - 6.5), 4, 2.6, facecolor="#b0b0b0",
                                        edgecolor="#444444", lw=0.8, zorder=3))
        ax.add_patch(patches.Rectangle((x + 2.6, y + h - 6), 2.8, 1.6, facecolor="#4a4a4a", zorder=4))
        ax.text(x + 2, y + h - 7.2, "USB Control\n(to PC)", ha="left", va="top", fontsize=6.5, zorder=3)
        # relay bodies with LED + polarity marking
        n = min(channels, 4)
        relay_w, relay_h = w * 0.28, min(7, (h - 12) / max(n, 1) - 1)
        for c in range(n):
            ry = y + h - 11 - c * (relay_h + 2)
            ax.add_patch(patches.FancyBboxPatch((x + w * 0.4, ry), relay_w, relay_h,
                         boxstyle="round,pad=0.15", facecolor="#1c1c1c", edgecolor="#3a3a3a",
                         lw=0.8, zorder=3))
            ax.text(x + w * 0.4 + relay_w / 2, ry + relay_h / 2, f"K{c + 1}\n5V", ha="center",
                    va="center", fontsize=5, color="white", zorder=4)
            ax.add_patch(patches.Circle((x + w * 0.4 - 1.2, ry + relay_h - 1), 0.5,
                                         facecolor="#e53935", zorder=4))  # status LED
        # power input connector (green, left edge) - labeled GND (lower) / +5V (upper)
        ax.add_patch(patches.Rectangle((x - 3, y + 1), 3, 6, facecolor="#1e5e2b",
                                        edgecolor="black", lw=0.8, zorder=3))
        pwr_pins = []
        for i, lbl in enumerate(("GND", "+5V")):
            py = y + 2 + i * 3
            ax.add_patch(patches.Circle((x - 1.5, py), 0.4, facecolor="#d9d9d9",
                                         edgecolor="black", lw=0.5, zorder=4))
            ax.text(x - 3.5, py, lbl, ha="right", va="center", fontsize=6, fontweight="bold", zorder=5)
            pwr_pins.append((x - 3, py))
        ax.text(x - 3.5, y + 9.5, "Power Input\nConnector", ha="right", va="bottom", fontsize=6.5, zorder=5)
        # relay-1 output connector (green, right edge) with COM/NO/NC
        conn_h = 3.6 * len(conn_labels)
        conn_y0 = y + h / 2 - conn_h / 2
        ax.add_patch(patches.Rectangle((x + w, conn_y0), 3, conn_h, facecolor="#1e5e2b",
                                        edgecolor="black", lw=0.8, zorder=3))
        conn_pins = {}
        for i, lbl in enumerate(conn_labels):
            cy = conn_y0 + conn_h - 1.8 - i * 3.6
            ax.add_patch(patches.Circle((x + w + 1.5, cy), 0.4, facecolor="#d9d9d9",
                                         edgecolor="black", lw=0.5, zorder=4))
            ax.text(x + w + 4, cy, lbl, ha="left", va="center", fontsize=6.5, fontweight="bold", zorder=5)
            conn_pins[lbl] = (x + w + 3, cy)
        ax.text(x + w / 2, y + h + 4, f"{tag}\n{part}", ha="center", va="bottom",
                fontsize=8.5, fontweight="bold", zorder=5)
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=6.5, zorder=5)
        return {"bbox": (x, y, w, h), "pwr_gnd": pwr_pins[0], "pwr_5v": pwr_pins[1], **conn_pins}

    def draw_din_rail_terminal_strip(self, x, y, n=4, tag="TB"):
        """DIN-rail mounted terminal block strip: hat-profile rail + n individual gray
        terminal blocks, each with a numbered screw top and separator dividers."""
        ax = self.ax
        w = 7.0 * n + 4
        # DIN rail hat profile (top lip + main body)
        ax.add_patch(patches.Rectangle((x - 3, y + 3.6), w + 2, 1.0, facecolor="#8f8f8f",
                                        edgecolor="black", lw=0.8, zorder=1))
        ax.add_patch(patches.Rectangle((x - 3, y), w + 2, 3.6, facecolor="#b5b5b5",
                                        edgecolor="black", lw=1, zorder=1))
        terminals = []
        for i in range(n):
            cx = x + 3.5 + i * 7.0
            ax.add_patch(patches.Rectangle((cx - 3, y + 4.6), 6, 11, facecolor="#f0f0f0",
                                            edgecolor="#555555", lw=1, zorder=2))
            if i > 0:
                ax.plot([cx - 3.5, cx - 3.5], [y + 4.6, y + 15.6], color="#999999", lw=0.8, zorder=3)
            ax.add_patch(patches.Circle((cx, y + 13.2), 1.9, facecolor="#d0d0d0",
                                         edgecolor="black", lw=0.9, zorder=4))
            ax.plot([cx - 1.2, cx + 1.2], [y + 13.2, y + 13.2], color="#222222", lw=1.0, zorder=5)
            ax.text(cx, y + 16.3, str(i + 1), ha="center", va="bottom", fontsize=7.5,
                    fontweight="bold", zorder=5)
            terminals.append((cx, y + 13.2))
        ax.text(x + w / 2 - 1.5, y + 23.5, tag, ha="center", va="bottom", fontsize=8.5,
                fontweight="bold", zorder=5)
        return {"bbox": (x, y, w, 20), "terminals": terminals}

    def draw_generic_pcb(self, x, y, w, h, tag, part="", func=""):
        """Fallback icon for any module without a dedicated shape: green PCB silhouette
        with dark chip-outline blocks, still visually distinct from the other categories."""
        ax = self.ax
        _shadow(ax, lambda: patches.Rectangle((x, y), w, h))
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor="#1e5e2b", edgecolor="#0d3d20", lw=1.5, zorder=1))
        for i in range(3):
            ax.add_patch(patches.Rectangle((x + 2 + i * (w / 3), y + 2), w / 3 - 2, h - 4,
                                            facecolor="#1c1c1c", edgecolor="#444444", lw=0.5, zorder=2))
        ax.text(x + w / 2, y + h + 4, f"{tag}\n{part}", ha="center", va="bottom",
                fontsize=8.5, fontweight="bold", zorder=3)
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=6.5, zorder=3)
        return {"bbox": (x, y, w, h)}

    # --- wiring & legend ---------------------------------------------------
    def wire(self, x1, y1, x2, y2, color, lw=2.2, label="", label_side="above"):
        """Strictly orthogonal 3-segment route (horizontal-vertical-horizontal). Assign each
        signal a consistent y across the whole diagram so parallel wires never cross."""
        ax = self.ax
        if abs(y1 - y2) < 0.05:
            ax.plot([x1, x2], [y1, y2], color=color, lw=lw, solid_capstyle="round", zorder=6)
        else:
            mid = (x1 + x2) / 2
            ax.plot([x1, mid, mid, x2], [y1, y1, y2, y2], color=color, lw=lw,
                    solid_capstyle="round", solid_joinstyle="round", zorder=6)
        if label:
            ly = max(y1, y2) + 1 if label_side == "above" else min(y1, y2) - 2
            va = "bottom" if label_side == "above" else "top"
            ax.text((x1 + x2) / 2, ly, label, ha="center", va=va, fontsize=7.5,
                    fontweight="bold", color=color, zorder=6)

    def add_legend_item(self, color, label):
        if not self._legend_started:
            self.ax.add_patch(patches.Rectangle((2, 2), 46, 14, facecolor="white", edgecolor="black", lw=1.2, zorder=5))
            self._legend_started = True
            self._legend_y = 12
        self.ax.plot([4, 8], [self._legend_y, self._legend_y], color=color, lw=3, zorder=6)
        self.ax.text(9, self._legend_y, label, va="center", fontsize=7.5, zorder=6)
        self._legend_y -= 3.4

    def save(self, filename, dpi=220):
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")
        plt.close(self.fig)


def _demo():
    d = IllustratedDiagrammer("System Block Diagram: SMPS, Numato Relay, and Terminal Block Connection",
                              width=185, height=90)

    outlet = d.draw_ac_outlet(6, 45, w=16, h=20)
    smps = d.draw_power_module(36, 50, 28, 16, "SMPS", "Mean Well LRS-35-5",
                                in_labels=("AC L", "AC N"), out_labels=("+5VDC", "V-"))
    numato = d.draw_relay_module(88, 48, 30, 20, "Numato Lab 2 Channel", "USB Relay Module", channels=2)
    tb = d.draw_din_rail_terminal_strip(140, 50, n=4, tag="Terminal Block Strip (DIN Rail Mounted)")

    # outlet -> SMPS (AC L / AC N) - exact icon pin coordinates, no guessing.
    # No mid-wire label needed: the SMPS terminal pin labels (AC L / AC N) already
    # identify each conductor per conventions.md "label every conductor at least once".
    d.wire(*outlet["line_out"], *smps["in_0"], "#a00000")
    d.wire(*outlet["neutral_out"], *smps["in_1"], "black")

    # SMPS -> Numato (+5VDC / GND) - both ends already pin-labeled (+5VDC/V- on the SMPS,
    # +5V/GND on the Numato power connector), so no redundant mid-wire label either.
    d.wire(*smps["out_0"], *numato["pwr_5v"], "#1e8f3e")
    d.wire(*smps["out_1"], *numato["pwr_gnd"], "black")

    # Numato relay-1 (COM/NO) -> terminal block 1/2
    d.wire(*numato["COM"], *tb["terminals"][0], "#a00000", label="Switched Output")
    d.wire(*numato["NO"], *tb["terminals"][1], "#a00000")

    d.add_legend_item("#a00000", "Switched 120VAC output")
    d.add_legend_item("black", "120VAC N / GND")
    d.add_legend_item("#1e8f3e", "+5VDC")

    d.save("illustrated_demo.png")
    print("wrote illustrated_demo.png")


if __name__ == "__main__":
    _demo()
