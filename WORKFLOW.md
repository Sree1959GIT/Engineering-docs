# Engineering Documentation Workflow — Detailed Example

This document walks through a complete end-to-end execution: from user input through final Google Drive output.

---

## Scenario

**Task:** Document the GCF (Generator Control Frame) module for a bench test rig. The user has a hand-sketched schematic and a notes file. They need a professional PDF with proper relay symbols, connection tables, and block descriptions.

**Project:** "GCF-TestRig-Rev2"

---

## Full Execution Walk-Through

### Phase 1: User Input

```bash
$ python orchestrator.py
```

The script prompts:

```
================================================================================
ENGINEERING DOCUMENTATION ORCHESTRATOR (Haiku → Opus → Drive)
================================================================================

[Step 1] Describe your engineering task:
(Paste sketch description, CSV path, or wiring requirements)
---
```

User pastes the task description (could be prose, a CSV, or a file path):

```
GCF Module Control Schematic:

Source: AC 3-phase (380V, 50Hz) + DC 24V supply
Relays:
  K1: 5-pole contactor (3 AC poles + 2 aux), 220V coil (N.O. contacts to motor M)
  K2: 1-pole 24VDC relay (1 N.O. to auxiliary load)

Instruments:
  DMM on A3± for fault signal (0-10V from controller)
  Wattmeter W across motor phases
  Fan Motor M: 3-phase, ~2 kW

Connections (from sketch):
  AC Source → [AC disconnect] → K1 main contacts → Motor M
  K1 coil ← [Controller relay output 24VDC]
  K2 N.O. → Auxiliary circuit (to be determined)
  DC Source 24V → K2 coil
  RTD temp sensors (T1, T2, T3) → CU1-P1 (4-wire configuration)
  Fault line: DMM A3± ← [Controller output]

Questions:
  - RTD is 4-wire PT100 (to confirm)
  - K2 auxiliary load TBD (placeholder: 24VDC LED indicator)
  - AC phase count: R/Y/B or R/Y/N? Assume R/Y/B
done

[Step 2] Project name (e.g., 'TestRig-CU1'): GCF-TestRig-Rev2
```

---

### Phase 2a: Haiku Triage (Automated)

The orchestrator calls Haiku 4.5:

```
================================================================================
PHASE 1: Triaging with Haiku 4.5 (tool selection & requirements)
================================================================================
```

**Haiku system prompt:** "You are an engineering triage specialist..."

**Haiku response (simulated):**

```json
{
  "task_type": "schematic",
  "standard": "IEC 60617",
  "required_inputs": [
    "relay specification sheet (K1 & K2: datasheet with terminal layouts)",
    "motor nameplate (kW, voltage, phase, P.F.)",
    "RTD calibration (Pt100 4-wire, ohm ranges)",
    "controller output specs (DMM input impedance, 0-10V range)",
    "AC source phase order (confirm R/Y/B vs R/Y/N)"
  ],
  "recommended_tool": "schemdraw",
  "complexity": "medium",
  "questions_for_user": [
    "Is the 24VDC relay (K2) directly driven by the controller or via a separate driver circuit?",
    "What is the motor contactor coil voltage: 220V AC, 110V AC, or 24VDC?",
    "Are there any protection devices (fuses, circuit breakers) in the schematic?"
  ],
  "estimated_time_hours": 2.5
}
```

Terminal output:

```
[Haiku Response]
{
  "task_type": "schematic",
  "standard": "IEC 60617",
  "required_inputs": [
    "relay specification sheet (K1 & K2: datasheet with terminal layouts)",
    ...
  ],
  "recommended_tool": "schemdraw",
  "complexity": "medium",
  "questions_for_user": [
    "Is the 24VDC relay (K2) directly driven by the controller or via a separate driver circuit?",
    ...
  ],
  "estimated_time_hours": 2.5
}

Proceed with Opus engineering workflow? (yes/no): 
```

User reviews Haiku's triage output and approves:

```
Proceed with Opus engineering workflow? (yes/no): yes
```

---

### Phase 2b: Opus Engineering Workflow (Automated)

The orchestrator calls Opus 4.8 with:
- **Model:** `claude-opus-4-8`
- **System prompt:** "You are an expert hardware engineer and technical documentarian..."
- **User prompt:** Full task description + Haiku triage context + instruction to use wiring-block-diagrams skill

```
================================================================================
PHASE 2: Full Engineering Workflow with Opus 4.8
================================================================================

[Calling Opus 4.8...]
```

**Opus internal workflow (not shown to user, but happens):**

1. **Parse inputs:**
   - Task: 3-phase AC + DC relays, motor control, RTD + DMM
   - Standard: IEC 60617
   - Tool: schemdraw (Haiku recommended)

2. **Build connection table:**
   ```
   From             | Via               | To               | Notes
   ---|---
   AC Source (R)    | K1 main pole 1    | Motor M (Ph1)    | 5A contactor
   AC Source (Y)    | K1 main pole 2    | Motor M (Ph2)    | Phase sequence critical
   AC Source (B)    | K1 main pole 3    | Motor M (Ph3)    | [VERIFY: confirm R/Y/B]
   Controller 24V   | [isolation relay]  | K1 coil (220V)   | [VERIFY: 220V? 110V? 24V?]
   DC 24V Source    | K2 coil (N.O.)    | Auxiliary load   | [VERIFY: auxiliary load spec]
   RTD T1 (4-wire)  | +/- wires         | CU1-P1 DMM input | Pt100, 100Ω @ 0°C
   RTD T2 (4-wire)  | +/- wires         | CU1-P1 DMM input | Pt100, 100Ω @ 0°C
   RTD T3 (4-wire)  | +/- wires         | CU1-P1 DMM input | Pt100, 100Ω @ 0°C
   Controller fault | 0-10V out         | DMM A3± input    | Signal to monitoring
   Wattmeter W      | R/Y/B inputs      | Motor phases     | Monitors real power
   ```

3. **Adversarial source review:**
   - ✓ All major components present (relays, motor, sensors, instruments).
   - ✓ No omissions detected.
   - ⚠ **Three [VERIFY] items flagged:**
     - K1 coil voltage (inferred 220V AC, but could be 110V AC or 24VDC).
     - AC phase order (assumed R/Y/B, but some systems use R/Y/N).
     - K2 auxiliary load specification.
   - ✓ No invented details (no guessed part numbers, lengths, loom types).

4. **Generate diagrams using schemdraw:**
   - Draws proper relay/contactor symbols (IEC 60617).
   - Ganged contacts for each phase.
   - Coil blocks with A1/A2 terminals.
   - Motor load symbol.
   - Wattmeter and DMM symbols.
   - Terminal labels and signal paths.
   - Exports to: `gcf_schematic.png` (preview), `gcf_schematic.svg` (editable).

5. **Block descriptions:**
   ```
   BLOCK 1: AC Source (380V, 3-phase, 50Hz)
   Supplies the main contactor K1 for motor drive. Phase sequence: R, Y, B.
   
   BLOCK 2: K1 (5-pole Contactor, 220V Coil)
   Main switching device. 3 main poles control motor phases; 2 auxiliary contacts
   feed the control circuit and pilot lamp. Coil is energized by the controller.
   [VERIFY: Confirm coil voltage is 220V AC.]
   
   BLOCK 3: Motor M (~2 kW, 3-phase)
   Load. Fed via K1 main contacts. Phase sequence must match source to prevent
   reverse rotation.
   
   BLOCK 4: Wattmeter W
   Measures real power consumption (kW) across motor phases for diagnostics.
   
   BLOCK 5: RTD Temperature Sensors (T1, T2, T3)
   Three 4-wire Pt100 sensors (100Ω @ 0°C). Wired to CU1-P1 for temperature
   monitoring. 4-wire configuration compensates for lead resistance.
   
   BLOCK 6: DMM (Data Monitoring Module, CU1-P1)
   Accepts RTD inputs (via bridge or transmitter) and fault signal (0-10V).
   A3± terminals are differential input for fault monitoring.
   
   BLOCK 7: K2 (1-pole 24VDC Relay)
   Auxiliary switching device. Coil fed from 24VDC supply. N.O. contact feeds
   an auxiliary circuit (e.g., pilot lamp or solenoid).
   [VERIFY: Specify auxiliary load.]
   
   BLOCK 8: DC 24V Supply
   Coil power for K2 relay. Separate from motor power to avoid transients.
   ```

6. **Assemble documentation (PDF):**
   ```
   ┌─────────────────────────────────────────┐
   │ GCF (Generator Control Frame)            │
   │ Power & Control Schematic                │
   │ Project: TestRig-Rev2                    │
   │ Date: 2026-06-24                         │
   │ Scale: Not to physical scale             │
   │ Source: Hand sketch (Rev 2) + notes      │
   │ [See Items to Verify below]              │
   └─────────────────────────────────────────┘
   
   [SVG Schematic: AC source → K1 → Motor, with RTD/DMM, K2 relay]
   
   ─── CONNECTIONS ───
   [Connection table in CSV format, embedded in PDF]
   
   ─── BLOCK DESCRIPTIONS ───
   [7 blocks described, with [VERIFY] callouts]
   
   ─── ITEMS TO VERIFY ───
   1. K1 coil voltage: Is it 220V AC, 110V AC, or 24VDC?
   2. AC phase sequence: Confirm R/Y/B (vs. R/Y/N for 2-phase systems).
   3. K2 auxiliary load: Specify the device/circuit fed by K2 N.O. contact.
   4. RTD transmitter: Is there an RTD-to-analog converter, or direct resistance bridge?
   5. DMM A3± impedance: Confirm that the 0-10V fault signal can drive this input.
   ```

7. **Save to temporary outputs folder:**
   ```
   ~/outputs/
   ├── GCF-TestRig-Rev2_Schematic.pdf
   ├── GCF-TestRig-Rev2_Schematic.svg
   ├── GCF-TestRig-Rev2_ConnectionTable.csv
   └── GCF-TestRig-Rev2_BlockDescriptions.txt
   ```

**Terminal output (abbreviated):**

```
[Opus Response (truncated)]
Building connection table from task description...
✓ Connection table built (8 rows, all major paths)

Adversarial review against source...
✓ No omissions detected
⚠ 3 items flagged [VERIFY]:
  - K1 coil voltage
  - AC phase sequence
  - K2 auxiliary load

Drafting schematic with schemdraw...
✓ Schematic rendered (proper relay blocks, IEC 60617)

Generating block descriptions...
✓ 7 block descriptions written

Assembling PDF...
✓ PDF generated: GCF-TestRig-Rev2_Schematic.pdf

Opus engineering workflow completed.
```

---

### Phase 3: Save to Google Drive (Automated, via MCP)

The orchestrator uses the Google Drive MCP connector:

```
================================================================================
PHASE 3: Saving to Google Drive (via MCP)
================================================================================

Creating folder: Engineering-GCF-TestRig-Rev2_2026-06-24_14-35-22
Uploading: GCF-TestRig-Rev2_Schematic.pdf
Uploading: GCF-TestRig-Rev2_ConnectionTable.csv
Uploading: GCF-TestRig-Rev2_BlockDescriptions.txt
Setting sharing: Anyone with link can view

✓ Output folder: Engineering-GCF-TestRig-Rev2_2026-06-24_14-35-22
✓ Drive link: https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h/
```

**Google Drive after upload:**

```
My Drive
├── Engineering-GCF-TestRig-Rev2_2026-06-24_14-35-22/
│   ├── GCF-TestRig-Rev2_Schematic.pdf
│   ├── GCF-TestRig-Rev2_Schematic.svg
│   ├── GCF-TestRig-Rev2_ConnectionTable.csv
│   └── GCF-TestRig-Rev2_BlockDescriptions.txt
```

---

## Summary Output

```
================================================================================
WORKFLOW SUMMARY
================================================================================
Task: GCF Module: 3-phase AC (380V, 50Hz) + DC 24V relays, motor control...
Project: GCF-TestRig-Rev2
Haiku decision: schemdraw
Opus status: success
Drive folder: Engineering-GCF-TestRig-Rev2_2026-06-24_14-35-22

Total execution time:
  - Haiku triage: ~15 sec
  - Opus work: ~3 min 20 sec
  - Google Drive upload: ~10 sec
  - TOTAL: ~3 min 45 sec

Cost breakdown:
  - Haiku: ~$0.002
  - Opus: ~$0.15
  - TOTAL: ~$0.152

Next steps:
  1. Review the PDF and [VERIFY] items.
  2. Share the Drive folder with your team.
  3. Confirm the three [VERIFY] items with hardware leads.
  4. Run orchestrator again with corrected inputs (if needed) to regenerate diagrams.
================================================================================
```

---

## What User Does Next

1. **Download the PDF** from Google Drive and review in a PDF reader.
2. **Check the [VERIFY] items:**
   - Contact hardware team for K1 coil voltage (220V? 110V? 24V?).
   - Confirm AC phase order (R/Y/B or R/Y/N?).
   - Get spec for K2 auxiliary load.
3. **Share the folder** with teammates via Google Drive sharing.
4. **(Optional) Iterate:** If K1 coil is actually 24VDC, ask the user to provide the corrected spec, and re-run the orchestrator. Opus will regenerate a corrected schematic.

---

## Cost & Time Analysis

| Phase | Model | Input Tokens | Output Tokens | Time | Cost |
|-------|-------|--------------|---------------|------|------|
| Triage | Haiku 4.5 | 1,200 | 350 | 15 sec | $0.002 |
| Engineering | Opus 4.8 | 4,500 | 2,800 | 3:20 min | $0.150 |
| Drive upload | (MCP) | — | — | 10 sec | $0.000 |
| **TOTAL** | | | | **~3:45 min** | **~$0.152** |

**Comparison:**
- Using Opus for both triage + work: ~$0.50 + longer execution time.
- Using Haiku + Opus: ~$0.15 + faster total execution.
- **Savings: 70% cost reduction.**

---

## Troubleshooting During Execution

### "Haiku's JSON parsing failed"

If Haiku doesn't output valid JSON, the orchestrator falls back to treating it as free text:

```python
triage_result = {"raw_response": haiku_response_text}
```

Opus can still proceed with this, though some structured routing may be lost.

### "Opus timeout after 5 minutes"

Large schematics or complex connection tables may take longer. Increase the timeout:

```python
# In orchestrator.py, Phase 2:
response = client.messages.create(
    model=OPUS_MODEL,
    max_tokens=4000,
    timeout=600  # 10 minutes instead of default 5
)
```

### "Google Drive MCP not connected"

See `MCP-SETUP.md` troubleshooting section. Quick check:

```python
# In a Claude Code session, ask:
# "List my Google Drive folders."
# If this fails, MCP is not connected.
```

---

## Next Steps After First Run

1. Verify the PDF is correct.
2. Adjust any [VERIFY] items and re-run with corrected input.
3. Extend to batch processing: create a CSV of multiple tasks and loop through them.
4. Add email notifications: use Gmail MCP to send completion summaries.
5. Store connection tables in Airtable: use Airtable MCP to persist data as a database.

---

**End of Workflow Example**
