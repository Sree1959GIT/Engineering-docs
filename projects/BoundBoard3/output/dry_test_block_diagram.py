"""
BoundBoard3 dry-test block diagram (3-component Phase 4/5 walkthrough).

Draws the three components confirmed in the Gate 2 packaging report as
category-distinguishable blocks (see wiring-block-diagrams/references/conventions.md,
"Block differentiation"): a power supply (rounded, red), a relay/switching module
(dashed, blue), and an interface/adapter module (rounded, gray).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..",
                                 "wiring-block-diagrams", "scripts"))
from fixture_diagrammer import FixtureDiagrammer  # noqa: E402

d = FixtureDiagrammer("BoundBoard3 - Dry Test Block Diagram (3 components, Phase 4/5)", width=100, height=70)

# SMPS1 - power supply (left, per zoning convention)
d.draw_categorized_block(
    6, 40, 22, 16,
    tag="B3SMPS1",
    category="power",
    part="MEAN WELL RT-125D",
    func="AC-DC supply, 5V/12V/24V out",
)

# Numato 32ch relay board - relay/switching module (centre)
d.draw_categorized_block(
    40, 40, 24, 16,
    tag="B3RL1",
    category="relay",
    part="Numato 32-ch Relay [VERIFY interface]",
    func="Relay matrix - top-probe switching",
)

# TI UCD interface adapter - interface/adapter module (right)
d.draw_categorized_block(
    76, 40, 20, 16,
    tag="JF3 / UCD",
    category="interface",
    part="TI USB-to-I2C [VERIFY model]",
    func="USB<->I2C/PMBus bridge to UCD IC",
)

# Connectivity (topological, not to scale)
d.route_orthogonal(28, 48, 40, 48, cls="power", label="12VDC")
d.route_orthogonal(64, 48, 76, 48, cls="signal", label="SCL/SDA/GND")

d.add_legend_item("power", "12VDC power rail")
d.add_legend_item("signal", "I2C / control signal")

d.save(os.path.join(os.path.dirname(__file__), "dry_test_block_diagram.png"))
print("wrote dry_test_block_diagram.png")
