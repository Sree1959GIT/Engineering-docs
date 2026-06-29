"""
schemdraw_example.py - Standard Electrical Schematic using Schemdraw

Demonstrates drawing electrical schematics with proper IEC symbols.
Requires: pip install schemdraw

Usage:
    python schemdraw_example.py
    
    Generates: schematic.svg (editable) and schematic.png (preview)
"""

try:
    import schemdraw
    import schemdraw.elements as elm
except ImportError:
    print("schemdraw not installed. Install with: pip install schemdraw")
    print("This is optional - the orchestrator can work without it")
    exit(1)

def create_motor_control_schematic():
    """
    Create a 3-phase motor control schematic with:
    - AC source (3-phase, 380V)
    - Relay K1 (5A contactor)
    - Motor M (2.2kW)
    - Control circuit
    """
    
    # Create drawing
    with schemdraw.Drawing() as d:
        d.config(fontsize=10, font='sans-serif')
        
        # Title
        d += (title := schemdraw.elements.Label().label('3-Phase Motor Control Schematic\n380V 50Hz'))
        
        # ===== MAIN POWER CIRCUIT =====
        
        # AC Source (left side)
        d += (src := elm.SourceV().label('AC Source\n380V 3ph'))
        d += elm.Line().right(0.5)
        
        # Main disconnect
        d += (disc := elm.Switch().label('Q1\nDisconnect', loc='top'))
        d += elm.Line().right(0.5)
        
        # K1 Relay Contactor (3 poles)
        d += elm.Line().right(0.3)
        d.push()  # Save position
        
        # Phase 1
        d += (k1_1 := elm.Relay2(box=False).label('K1.1', loc='bottom'))
        d += elm.Line().at((k1_1.end[0] + 0.5, k1_1.end[1]))
        d += elm.Gap().label('Motor\nPhase 1', loc='center')
        d += elm.Line().right(0.5)
        
        # Phase 2
        d.pop()
        d += elm.Line().down(1.5)
        d += (k1_2 := elm.Relay2(box=False).label('K1.2', loc='bottom'))
        d += elm.Line().at((k1_2.end[0] + 0.5, k1_2.end[1]))
        d += elm.Gap().label('Motor\nPhase 2', loc='center')
        
        # Phase 3
        d.pop()
        d += elm.Line().down(3)
        d += (k1_3 := elm.Relay2(box=False).label('K1.3', loc='bottom'))
        d += elm.Line().at((k1_3.end[0] + 0.5, k1_3.end[1]))
        d += elm.Gap().label('Motor\nPhase 3', loc='center')
        
        # ===== CONTROL CIRCUIT =====
        # (Simplified - shows K1 coil control)
        
        d.pop()
        d += elm.Line().down(5)
        d += elm.Line().left(3)
        
        # Control transformer (optional)
        d.push()
        d += elm.Transformer().label('T1\n380V→24V', loc='bottom')
        d.pop()
        
        d += elm.Line().right(4)
        
        # K1 Coil (220V control)
        d += elm.Coil().label('K1 Coil\n220V', loc='bottom')
        d += elm.Line().right(0.5)
        d += elm.Line().down(0.5)
        
        # Return to source
        d += elm.Line().at((src.start[0], src.start[1] - 5))
        
        # Add legend
        d += elm.Label().at((8, -1)).label(
            'K1: 5A Contactor (3 poles + 2 aux contacts)\n'
            'Q1: Main Disconnect Switch\n'
            'T1: Control Transformer (optional)'
        )
    
    return d

def create_simple_schematic():
    """Create a simpler example: Single relay circuit"""
    
    with schemdraw.Drawing() as d:
        d.config(fontsize=9)
        
        # AC Source
        d += (src := elm.SourceV().label('AC 220V'))
        d += elm.Line().right(0.5)
        
        # Switch
        d += (sw := elm.Switch().label('S1'))
        d += elm.Line().right(0.5)
        
        # Relay K1
        d += (k1 := elm.Relay()).label('K1')
        d += elm.Line().right(0.5)
        
        # Load (Motor or lamp)
        d += elm.Gap().label('Load')
        d += elm.Line().down(1)
        d += elm.Line().left(3)
        d += elm.Line().at(src.start)
        
        # Add auxiliary circuit (K1 NO contact to indicator lamp)
        d.move(0, -3)
        d.push()
        d += elm.SourceV().label('DC 24V\nControl')
        d += elm.Line().right(0.5)
        
        # K1 Auxiliary NO contact
        d += elm.Contact(action='close').label('K1 NO', loc='bottom')
        d += elm.Line().right(0.5)
        
        # Indicator lamp
        d += elm.Gap().label('Green Lamp\n(K1 Active)')
    
    return d

if __name__ == "__main__":
    print("Generating electrical schematics...")
    
    # Create motor control schematic
    print("✓ Creating motor control schematic...")
    try:
        d1 = create_motor_control_schematic()
        d1.save('motor_control_schematic.svg')
        d1.draw()
        print("✓ Motor control schematic saved: motor_control_schematic.svg")
    except Exception as e:
        print(f"⚠ Could not create motor control schematic: {e}")
    
    # Create simple schematic
    print("✓ Creating simple relay circuit...")
    try:
        d2 = create_simple_schematic()
        d2.save('simple_relay_circuit.svg')
        d2.draw()
        print("✓ Simple circuit saved: simple_relay_circuit.svg")
    except Exception as e:
        print(f"⚠ Could not create simple circuit: {e}")
    
    print("\nDone! SVG files can be edited in any vector editor (Inkscape, etc.)")
