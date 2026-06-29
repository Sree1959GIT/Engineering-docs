"""
fixture_diagrammer.py - Matplotlib-based Fixture & Block Diagram Engine

Provides tools for drawing system block diagrams with:
- Color-coded signal paths (power, DC, signal, RF, harness)
- Zoned layout (power-left, switching-center, instruments-right)
- Orthogonal routing
- Professional PDF output

Usage:
    from fixture_diagrammer import FixtureDiagrammer
    
    diag = FixtureDiagrammer(width=14, height=10)
    diag.add_block("AC Source", "Power", 1, 5, width=2, height=1.5)
    diag.add_block("K1 Relay", "Switching", 5, 5, width=2, height=1.5)
    diag.add_block("Motor M", "Load", 9, 5, width=2, height=1.5)
    diag.draw_connection((3, 5.5), (5, 5.5), "power", "AC 3ph")
    diag.draw_connection((7, 5.5), (9, 5.5), "power", "Motor")
    diag.save("diagram.pdf")
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

class FixtureDiagrammer:
    """
    Professional fixture and system block diagram generator.
    """
    
    def __init__(self, width=14, height=10, title="System Block Diagram"):
        """Initialize diagram"""
        self.width = width
        self.height = height
        self.title = title
        
        # Create figure with equal aspect ratio
        self.fig, self.ax = plt.subplots(1, 1, figsize=(width, height), dpi=100)
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        
        # Remove axes
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        
        # Set title
        self.fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # Color scheme for signal types
        self.colors = {
            'power': '#FF0000',      # Red for AC/DC power
            'dc': '#FF6600',         # Orange for DC
            'signal': '#0066FF',     # Blue for signal/logic
            'rf': '#FF00FF',         # Magenta for RF
            'harness': '#333333',    # Dark gray for harness
        }
    
    def add_block(self, label, zone, x, y, width=2, height=1.5, color='lightgray'):
        """
        Add a block/component to diagram
        
        Args:
            label: Block name
            zone: "Power", "Switching", "Instruments", "Load"
            x, y: Center position
            width, height: Block dimensions
            color: Fill color
        """
        # Create fancy box
        box = FancyBboxPatch(
            (x - width/2, y - height/2), width, height,
            boxstyle="round,pad=0.1", 
            linewidth=2, 
            edgecolor='black',
            facecolor=color, 
            alpha=0.8
        )
        self.ax.add_patch(box)
        
        # Add label
        self.ax.text(x, y - 0.3, label, ha='center', va='center', 
                    fontsize=10, fontweight='bold')
        self.ax.text(x, y + 0.5, zone, ha='center', va='center',
                    fontsize=8, style='italic', color='gray')
    
    def draw_connection(self, start, end, signal_type='signal', label=''):
        """
        Draw connection line between blocks
        
        Args:
            start: (x, y) tuple for start point
            end: (x, y) tuple for end point
            signal_type: 'power', 'dc', 'signal', 'rf', 'harness'
            label: Connection label
        """
        color = self.colors.get(signal_type, '#000000')
        linewidth = 3 if signal_type == 'power' else 2
        
        # Draw line
        self.ax.plot([start[0], end[0]], [start[1], end[1]], 
                    color=color, linewidth=linewidth, zorder=1)
        
        # Add label if provided
        if label:
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            self.ax.text(mid_x, mid_y - 0.3, label, ha='center', va='bottom',
                        fontsize=8, bbox=dict(boxstyle='round', 
                        facecolor='white', alpha=0.8))
    
    def draw_orthogonal_route(self, points, signal_type='signal', label=''):
        """
        Draw orthogonal (L-shaped) routing with right angles
        
        Args:
            points: List of (x, y) waypoints
            signal_type: Signal type for color
            label: Connection label
        """
        color = self.colors.get(signal_type, '#000000')
        linewidth = 3 if signal_type == 'power' else 2
        
        # Draw segments
        for i in range(len(points) - 1):
            self.ax.plot([points[i][0], points[i+1][0]], 
                        [points[i][1], points[i+1][1]],
                        color=color, linewidth=linewidth, zorder=1)
    
    def add_legend(self):
        """Add signal type legend"""
        legend_x = 0.5
        legend_y = self.height - 0.8
        
        self.ax.text(legend_x, legend_y, "Signal Types:", 
                    fontsize=9, fontweight='bold')
        
        for i, (sig_type, color) in enumerate(self.colors.items()):
            y_offset = legend_y - 0.5 - (i * 0.4)
            self.ax.plot([legend_x, legend_x + 0.3], 
                        [y_offset, y_offset],
                        color=color, linewidth=2)
            self.ax.text(legend_x + 0.5, y_offset, sig_type.capitalize(),
                        fontsize=8, va='center')
    
    def save(self, filename):
        """Save diagram to file"""
        self.add_legend()
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Diagram saved: {filename}")
        plt.close()

# Example usage
if __name__ == "__main__":
    # Create diagram
    diag = FixtureDiagrammer(width=12, height=8, 
                            title="GCF Motor Control System")
    
    # Add blocks
    diag.add_block("AC Source\n380V 50Hz", "Power", 1.5, 4, color='lightcoral')
    diag.add_block("K1 Contactor\n5A 220V", "Switching", 6, 4, color='lightyellow')
    diag.add_block("Motor M\n2.2kW 3ph", "Load", 10.5, 4, color='lightblue')
    
    diag.add_block("RTD Sensors\nT1, T2, T3", "Instruments", 6, 1, color='lightgreen')
    diag.add_block("DMM Controller\nCU1", "Instruments", 10.5, 1, color='lightcyan')
    
    # Draw connections
    diag.draw_connection((2.5, 4), (5, 4), 'power', 'AC 3-phase')
    diag.draw_connection((7, 4), (9.5, 4), 'power', 'Motor phases')
    
    diag.draw_orthogonal_route([(6, 2.5), (6, 2.5), (10.5, 2.5)], 
                              'signal', 'RTD → DMM')
    
    # Save
    diag.save("system_diagram.png")
