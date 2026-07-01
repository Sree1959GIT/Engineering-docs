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
DIN-rail terminal-block worked example used to validate this tier against a reference sample).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

GREEN_TERM = "#3f8f4a"


def _shadow(ax, patch_fn, dx=0.5, dy=-0.5, alpha=0.15):
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


def _screw(ax, cx, cy, r=0.85, facecolor="#e8e8e8", zorder=4):
    """A screw-terminal head: circle + Phillips (+) cross slot."""
    ax.add_patch(patches.Circle((cx, cy), r, facecolor=facecolor, edgecolor="black", lw=0.8, zorder=zorder))
    ax.plot([cx - r * 0.6, cx + r * 0.6], [cy, cy], color="#333333", lw=1.0, zorder=zorder + 1)
    ax.plot([cx, cx], [cy - r * 0.6, cy + r * 0.6], color="#333333", lw=1.0, zorder=zorder + 1)


class IllustratedDiagrammer:
    def __init__(self, title, width=185, height=90):
        self.fig, self.ax = plt.subplots(figsize=(width / 10, height / 10))
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.ax.text(width / 2, height * 0.97, title, ha="center", va="center",
                     fontsize=15, fontweight="bold")
        self._legend_started = False
        self._legend_y = 2

    # --- component icons -------------------------------------------------
    def draw_ac_outlet(self, x, y, label="AC Power Outlet\n(120VAC Input)", w=18, h=28):
        """NEMA 5-15 duplex receptacle wall plate: two non-overlapping outlet faces, each
        with polarized blade slots and a round ground hole, plus a centre mounting screw."""
        ax = self.ax
        _shadow(ax, lambda: patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5"))
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5",
                     facecolor="#eeeeee", edgecolor="#555555", lw=1.4, zorder=1))
        ax.add_patch(patches.Circle((x + w / 2, y + h / 2), 0.5, facecolor="#888888", zorder=2))
        cx = x + w / 2
        for dy in (h * 0.74, h * 0.26):
            cy = y + dy
            ax.add_patch(patches.FancyBboxPatch((cx - w * 0.30, cy - w * 0.30), w * 0.6, w * 0.6,
                         boxstyle="round,pad=0.05", facecolor="#fdfdfd", edgecolor="#333333",
                         lw=1.1, zorder=2))
            ax.add_patch(patches.Rectangle((cx - w * 0.14, cy + 0.5), w * 0.10, w * 0.20,
                                            facecolor="#1a1a1a", zorder=3))
            ax.add_patch(patches.Rectangle((cx + w * 0.04, cy + 0.5), w * 0.10, w * 0.20,
                                            facecolor="#1a1a1a", zorder=3))
            ax.add_patch(patches.Circle((cx, cy - w * 0.16), w * 0.05, facecolor="#1a1a1a", zorder=3))
        ax.text(x + w / 2, y - 2.5, label, ha="center", va="top", fontsize=8.5, fontweight="bold")
        return {"bbox": (x, y, w, h),
                "line_out": (x + w, y + h * 0.74),
                "neutral_out": (x + w, y + h * 0.26)}

    def draw_power_module(self, x, y, w, h, tag, part="", func="",
                           in_labels=("AC L", "AC N"), out_labels=("+5VDC", "V-")):
        """Enclosed power-supply icon matching a real SMPS product photo: white/light body,
        a chassis ground screw, and green screw-terminal blocks protruding from the LEFT
        edge (input) and RIGHT edge (output) - so lane-based wiring never crosses the body."""
        ax = self.ax
        _shadow(ax, lambda: patches.Rectangle((x, y), w, h))
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor="#fafafa", edgecolor="black", lw=1.5, zorder=1))
        # chassis ground screw (bottom-left)
        ax.add_patch(patches.Circle((x + 2.5, y + 2.2), 1.1, facecolor=GREEN_TERM, edgecolor="black", lw=0.8, zorder=3))
        ax.plot([x + 1.7, x + 3.3], [y + 2.2, y + 2.2], color="#0d3d20", lw=0.9, zorder=4)
        ax.plot([x + 2.5, x + 2.5], [y + 1.4, y + 3.0], color="#0d3d20", lw=0.9, zorder=4)
        pins = {}
        term_w, term_h = 4.5, h * 0.62
        # LEFT edge: input terminal block (green, protruding), 2 stacked screws
        ax.add_patch(patches.FancyBboxPatch((x - term_w, y + h * 0.19), term_w, term_h,
                     boxstyle="round,pad=0.1", facecolor=GREEN_TERM, edgecolor="black", lw=1, zorder=2))
        for i, lbl in enumerate(in_labels):
            py = y + h * 0.19 + term_h * (0.78 - i * 0.56)
            _screw(ax, x - term_w / 2, py, r=1.0)
            ax.text(x + 1.2, py, lbl, ha="left", va="center", fontsize=8, fontweight="bold", zorder=5)
            pins[f"in_{i}"] = (x - term_w, py)
        # RIGHT edge: output terminal block (green, protruding), 2 stacked screws, +/- marked
        ax.add_patch(patches.FancyBboxPatch((x + w, y + h * 0.19), term_w, term_h,
                     boxstyle="round,pad=0.1", facecolor=GREEN_TERM, edgecolor="black", lw=1, zorder=2))
        for i, lbl in enumerate(out_labels):
            py = y + h * 0.19 + term_h * (0.78 - i * 0.56)
            _screw(ax, x + w + term_w / 2, py, r=1.0)
            ax.text(x + w - 1.2, py, ("+" if i == 0 else "-"), ha="right", va="center",
                    fontsize=8, fontweight="bold", color="white", zorder=5)
            # label sits ABOVE the pin's y (not at py) so a same-color wire routed out of the
            # pin at py never runs directly under/through the label text (e.g. a black "-" on
            # a black wire would otherwise visually disappear into it).
            ax.text(x + w + term_w + 2.2, py + 1.4, lbl, ha="left", va="center", fontsize=8,
                    fontweight="bold", zorder=8)
            pins[f"out_{i}"] = (x + w + term_w, py)
        ax.text(x + w / 2, y + h + 5, f"{tag}\n{part}", ha="center", va="bottom",
                fontsize=9, fontweight="bold", zorder=5)
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=7.5, zorder=5)
        pins["bbox"] = (x, y, w, h)
        return pins

    def draw_relay_module(self, x, y, w, h, tag, part="", func="", channels=2,
                           conn_labels=("COM", "NO", "NC")):
        """PCB-style relay/USB module icon matching a real relay-board product photo: white
        board, blue silkscreen logo, a micro-USB connector on the left edge, black relay
        bodies with small support-component dots, and green screw-terminal blocks for
        power-in (left) and switched output (right)."""
        ax = self.ax
        _shadow(ax, lambda: patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4"))
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4",
                     facecolor="#fcfcfc", edgecolor="black", lw=1.5, zorder=1))
        # mounting holes
        for cx_, cy_ in ((x + 2.2, y + 2.2), (x + w - 2.2, y + 2.2),
                          (x + 2.2, y + h - 2.2), (x + w - 2.2, y + h - 2.2)):
            ax.add_patch(patches.Circle((cx_, cy_), 0.8, facecolor="white", edgecolor="#888888",
                                         lw=0.8, zorder=3))
        ax.text(x + 4, y + h - 4, "numato", ha="left", va="center", fontsize=11,
                fontweight="bold", style="italic", color="#2e6da4", zorder=3)
        # micro-USB connector (left edge, mid-height). Label extends LEFTWARD/outside the
        # board (like "Power Input Connector" below) so it never collides with the logo or
        # relay bodies, which are further right on the board face.
        usb_y = y + h * 0.62
        ax.add_patch(patches.Rectangle((x - 2.5, usb_y - 1.6), 2.5, 3.2, facecolor="#b0b0b0",
                                        edgecolor="#444444", lw=0.8, zorder=3))
        ax.add_patch(patches.Rectangle((x - 2.0, usb_y - 1.0), 1.6, 2.0, facecolor="#4a4a4a", zorder=4))
        ax.text(x - 3, usb_y, "USB Control\n(to PC)", ha="right", va="center", fontsize=7, zorder=5)
        # relay bodies (black) with small support-component dot clusters to their left
        n = min(channels, 4)
        relay_w, relay_h = w * 0.34, min(8, (h - 14) / max(n, 1) - 1.5)
        for c in range(n):
            ry = y + h * 0.44 - c * (relay_h + 2.5)
            for k in range(3):
                ax.add_patch(patches.Rectangle((x + w * 0.30 + k * 1.3, ry + relay_h * 0.3), 0.9, 0.9,
                                                facecolor="#333333", zorder=3))
            ax.add_patch(patches.FancyBboxPatch((x + w * 0.45, ry), relay_w, relay_h,
                         boxstyle="round,pad=0.15", facecolor="#1c1c1c", edgecolor="#3a3a3a",
                         lw=0.8, zorder=3))
            ax.text(x + w * 0.45 + relay_w / 2, ry + relay_h / 2, f"K{c + 1}\n5V", ha="center",
                    va="center", fontsize=5.5, color="white", zorder=4)
        pins = {}
        # power input connector (green, left edge, protruding) - GND (lower) / +5V (upper)
        pw_h = 6.4
        pw_y0 = y + h * 0.2
        ax.add_patch(patches.FancyBboxPatch((x - 4, pw_y0), 4, pw_h, boxstyle="round,pad=0.08",
                     facecolor=GREEN_TERM, edgecolor="black", lw=1, zorder=3))
        for i, lbl in enumerate(("GND", "+5V")):
            py = pw_y0 + 1.6 + i * 3.2
            _screw(ax, x - 2, py, r=0.85)
            # label lifted above py (see draw_power_module out_labels comment - avoids a
            # same-color wire visually erasing the label, e.g. black "GND" on a black wire)
            ax.text(x - 5.5, py + 1.4, lbl, ha="right", va="center", fontsize=7.5,
                    fontweight="bold", zorder=8)
            pins[f"pwr_{'gnd' if i == 0 else '5v'}"] = (x - 4, py)
        ax.text(x - 4.5, pw_y0 + pw_h + 1.5, "Power Input\nConnector", ha="right", va="bottom",
                fontsize=7, zorder=5)
        # relay-1 output connector (green, right edge, protruding) with COM/NO/NC
        conn_h = 4.2 * len(conn_labels)
        conn_y0 = y + h / 2 - conn_h / 2
        ax.add_patch(patches.FancyBboxPatch((x + w, conn_y0), 4, conn_h, boxstyle="round,pad=0.08",
                     facecolor=GREEN_TERM, edgecolor="black", lw=1, zorder=3))
        conn_pins = {}
        for i, lbl in enumerate(conn_labels):
            cy = conn_y0 + conn_h - 2.1 - i * 4.2
            _screw(ax, x + w + 2, cy, r=0.85)
            ax.text(x + w + 5.5, cy + 1.4, lbl, ha="left", va="center", fontsize=7.5,
                    fontweight="bold", zorder=8)
            conn_pins[lbl] = (x + w + 4, cy)
        ax.text(x + w / 2, y + h + 4, f"{tag}\n{part}", ha="center", va="bottom",
                fontsize=9, fontweight="bold", zorder=5)
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=7, zorder=5)
        return {"bbox": (x, y, w, h), **pins, **conn_pins}

    def draw_din_rail_terminal_strip(self, x, y, n=4, tag="TB"):
        """DIN-rail mounted terminal block strip: perforated gray rail + n individual
        terminal blocks, each with a large Phillips-head screw and a numbered label."""
        ax = self.ax
        w = 8.0 * n + 4
        ax.add_patch(patches.Rectangle((x - 3, y), w + 2, 5.5, facecolor="#c2c2c2",
                                        edgecolor="black", lw=1, zorder=1))
        for i in range(int((w + 2) / 3)):
            ax.add_patch(patches.Circle((x - 2 + i * 3, y + 2.75), 0.5, facecolor="#9a9a9a",
                                         edgecolor="none", zorder=2))
        terminals = []
        for i in range(n):
            cx = x + 4 + i * 8.0
            ax.add_patch(patches.Rectangle((cx - 3.4, y + 5.5), 6.8, 13, facecolor="#f2f2f2",
                                            edgecolor="#555555", lw=1, zorder=3))
            if i > 0:
                ax.plot([cx - 4, cx - 4], [y + 5.5, y + 18.5], color="#999999", lw=0.8, zorder=4)
            _screw(ax, cx, y + 15.5, r=2.1, facecolor="#d8d8d8", zorder=5)
            ax.text(cx, y + 19.5, str(i + 1), ha="center", va="bottom", fontsize=8.5,
                    fontweight="bold", zorder=6)
            terminals.append((cx, y + 15.5))
        ax.text(x + w / 2 - 1.5, y + 27, tag, ha="center", va="bottom", fontsize=9,
                fontweight="bold", zorder=6)
        return {"bbox": (x, y, w, 24), "terminals": terminals}

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
                fontsize=9, fontweight="bold", zorder=3)
        if func:
            ax.text(x + w / 2, y - 2.5, func, ha="center", va="top", fontsize=7, zorder=3)
        return {"bbox": (x, y, w, h)}

    # --- wiring & legend ---------------------------------------------------
    def wire(self, x1, y1, x2, y2, color, lw=2.4, label="", label_side="above"):
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
            ly = max(y1, y2) + 1.2 if label_side == "above" else min(y1, y2) - 2.2
            va = "bottom" if label_side == "above" else "top"
            ax.text((x1 + x2) / 2, ly, label, ha="center", va=va, fontsize=8,
                    fontweight="bold", color=color, zorder=6)

    def add_legend_item(self, color, label):
        if not self._legend_started:
            self.ax.add_patch(patches.Rectangle((2, 2), 50, 15, facecolor="white", edgecolor="black", lw=1.2, zorder=5))
            self._legend_started = True
            self._legend_y = 13
        self.ax.plot([4, 8.5], [self._legend_y, self._legend_y], color=color, lw=3.5, zorder=6)
        self.ax.text(9.5, self._legend_y, label, va="center", fontsize=8, zorder=6)
        self._legend_y -= 3.6

    def save(self, filename, dpi=240):
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")
        plt.close(self.fig)


def _demo():
    d = IllustratedDiagrammer("System Block Diagram: SMPS, Numato Relay, and Terminal Block Connection",
                              width=220, height=100)

    outlet = d.draw_ac_outlet(6, 40, w=18, h=28)
    smps = d.draw_power_module(42, 48, 32, 20, "SMPS", "Mean Well LRS-35-5",
                                in_labels=("AC L", "AC N"), out_labels=("+5VDC", "V-"))
    numato = d.draw_relay_module(118, 42, 34, 32, "Numato Lab 2 Channel", "USB Relay Module", channels=2)
    tb = d.draw_din_rail_terminal_strip(178, 48, n=4, tag="Terminal Block Strip (DIN Rail Mounted)")

    # outlet -> SMPS (AC L / AC N) - exact icon pin coordinates, no guessing.
    d.wire(*outlet["line_out"], *smps["in_0"], "#a00000")
    d.wire(*outlet["neutral_out"], *smps["in_1"], "black")

    # SMPS -> Numato (+5VDC / GND)
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
