# Engineering Documentation Workflow — Claude Code Master Instructions

## Overview

This Claude Code workspace automates end-to-end electrical wiring & block diagram documentation using a **two-stage routing strategy**:

1. **Haiku 4.5 (fast triage)** — Scope the task, identify required tools, gather requirements. ~10-30 seconds, cost ~$0.001.
2. **Opus 4.8 (deep work)** — Execute the full engineering workflow: build connection table, draft diagrams, assemble documentation. ~2-5 minutes, cost ~$0.10–0.50.

**Savings:** 95% cost reduction vs. using Opus for both stages. Example: scoping + execution costs ~$0.101 instead of $0.50+ if Opus did both.

---

## Architecture

### Three Phases

```
Phase 1: User Input
    ↓
Haiku 4.5: "What tool? What do we need? How complex?"
    ↓
[User Reviews Triage]
    ↓
Phase 2: Opus 4.8: Full engineering workflow
    ├─ Build connection table
    ├─ Adversarial source review
    ├─ Draft diagrams (schemdraw, SVG, matplotlib, etc.)
    ├─ Assemble documentation
    └─ Generate PDF/docx
    ↓
Phase 3: Google Drive MCP saves outputs
    └─ Create project folder
    └─ Upload all artifacts
```

### Key Files

- **orchestrator.py** — Main script; runs Phase 1 and Phase 2 via API calls. Use: `python orchestrator.py`
- **wiring-block-diagrams.skill** — The engineering skill; loaded into Opus's context. Contains conventions, tool routing, and bundled scripts.
- **config.json** or `.env` — API keys, model IDs, Drive folder settings.

---

## Setup (One-Time)

### Prerequisites

- Claude Code installed (see https://docs.claude.com/en/docs/claude-code/overview).
- `ANTHROPIC_API_KEY` set (create at https://console.anthropic.com/api-keys).
- Python 3.9+ with `pip`.

### Step 1: Install Dependencies

```bash
cd ~/engineering-docs-orchestrator
pip install anthropic google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 2: Set API Key

**Option A: Environment Variable (recommended)**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Option B: .env File**
Create `.env` in the orchestrator directory:
```
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_DRIVE_FOLDER_ID=optional_parent_folder_id
```

### Step 3: Enable Google Drive MCP

In Claude Code:
1. Click **Customize** (left sidebar).
2. Click **Connectors**.
3. Click **+** (top right).
4. Search for **Google Drive**.
5. Click **Connect** and follow OAuth flow.

This authorizes Claude Code to create folders and save files to your Google Drive.

### Step 4: Copy the Skill

Place the `wiring-block-diagrams.skill` file in your Claude Code project folder:
```bash
cp /path/to/wiring-block-diagrams.skill .
```

Claude Code will auto-load it and make it available to Opus 4.8 calls.

---

## Running the Workflow

### Quick Start

```bash
python orchestrator.py
```

You'll be prompted for:
1. **Task description** — sketch details, CSV path, wiring requirements, or prose description.
2. **Project name** — e.g., "TestRig-CU1", "ControlPanel-Rev2".

Then:
- **Haiku** analyzes and recommends a tool (schemdraw, SVG, matplotlib, etc.).
- You review and approve.
- **Opus** executes the full workflow: builds connection table, drafts diagrams, assembles PDF/docx, uploads to Drive.

### Example Session

```
[Step 1] Describe your engineering task:
(Paste sketch description, CSV path, or wiring requirements)
---
GCF module: 3-phase AC via 5A relay K1 to motor M. DC via 1A relay K2.
RTD sensors T1, T2, T3 on CU1-P1 to DMM A3±.
Fan fault signal to controller.
done

[Step 2] Project name (e.g., 'TestRig-CU1'): GCF-Rev1

================================================================================
PHASE 1: Triaging with Haiku 4.5 (tool selection & requirements)
================================================================================

[Haiku Response]
{
  "task_type": "schematic",
  "standard": "IEC 60617",
  "required_inputs": ["relay spec sheet", "terminal block labels", "sensor calibration"],
  "recommended_tool": "schemdraw",
  "complexity": "medium",
  "questions_for_user": ["Are RTDs 4-wire or 3-wire?", "What's the AC phase count?"],
  "estimated_time_hours": 2
}

Proceed with Opus engineering workflow? (yes/no): yes

================================================================================
PHASE 2: Full Engineering Workflow with Opus 4.8
================================================================================

[Opus Response (truncated)]
Building connection table...
GCF → [verify relay K1 specs]
RTD sensors → DMM terminal block
...
✓ Opus engineering workflow completed.

WORKFLOW SUMMARY
================================================================================
Task: GCF module: 3-phase AC via 5A relay...
Project: GCF-Rev1
Haiku decision: schemdraw
Opus status: success
Drive folder: Engineering-GCF-Rev1_2026-06-24_14-30-45
================================================================================
```

---

## Model Routing Explained

### Why Haiku First?

- **Cost:** ~200× cheaper than Opus ($0.001 vs. $0.25 per call).
- **Speed:** ~5× faster (10 sec vs. 60 sec).
- **Fit:** Triage is classification + structured output. Haiku's 200K context + reasoning are plenty.
- **Efficiency:** Saves Opus time for hard work; Haiku handles scoping, requirements gathering, and tool selection.

### When Does Opus Take Over?

Opus handles the work that needs deep reasoning:
- Building a precise connection table from ambiguous inputs.
- Adversarial source review (catch misreads, invented details, missing components).
- Choosing symbol conventions and diagram layout for a specific standard.
- Coordinating between drawing tool output and documentation assembly.
- Handling edge cases (3-wire vs. 4-wire RTD interpretation, relay pole-count inference, etc.).

### Cost Example

**Scoping + Execution with Haiku + Opus:**
- Haiku triage: 1,500 tokens input, 300 output → ~$0.001
- Opus work: 5,000 tokens input (context) + 3,000 response → ~$0.10
- **Total: ~$0.101**

**Same work with Opus alone:**
- Two Opus calls (triage + work) → ~$0.50
- **Savings: 80% cost reduction**

---

## Project Structure

```
engineering-docs-orchestrator/
├── orchestrator.py                    Main script (Haiku → Opus routing)
├── wiring-block-diagrams.skill        Bundled skill (drop this in)
├── config.json                        (Optional) Centralized config
├── .env                               (Optional) API keys
├── README.md                          This file
├── docs/
│   ├── MCP-SETUP.md                   Google Drive / Gmail MCP connection steps
│   ├── WORKFLOW.md                    Detailed workflow example
│   └── TROUBLESHOOTING.md             Common issues & fixes
├── outputs/                           (Auto-created) Local copy of diagrams & tables
└── scripts/
    ├── schematic_lib.py               SVG schematic primitives
    ├── fixture_diagrammer.py          Matplotlib block diagram engine
    ├── schemdraw_example.py           Standard-symbol schematic example
    └── render_pdf.js                  Chromium HTML→PDF renderer
```

---

## Extending the Workflow

### Add Email Notifications

Once Opus finishes, have Claude Code send a summary email via Gmail MCP:

```python
# In orchestrator.py, after Phase 2:
from anthropic.mcp import gmail

message = client.gmail.create_draft(
    to="your-email@example.com",
    subject=f"Engineering Doc Ready: {project_name}",
    body=f"Diagrams & tables saved to: {drive_url}"
)
```

### Batch Processing

Create a loop that reads a CSV of tasks:

```python
# tasks.csv:
# project_name, description
# GCF-Rev1, "GCF module: 3-phase AC via 5A relay K1..."
# CCM-Rev2, "CCM: ECU J4 via Converter to PC..."

import csv

with open("tasks.csv") as f:
    for row in csv.DictReader(f):
        project_name = row["project_name"]
        description = row["description"]
        orchestrator.main(description, project_name)
```

### Store Connection Tables in Airtable

Use Airtable MCP to persist connection tables as a database:

```python
# After Phase 2, push table to Airtable:
from anthropic.mcp import airtable

airtable.create_record(
    base_id="appXXX...",
    table_name="connections",
    fields={"From": "GCF", "To": "DMM", "Via": "K1 relay", ...}
)
```

---

## MCP Connectors Used

1. **Google Drive** — Create project folders, upload PDFs/docx.
   - URL: `https://drivemcp.googleapis.com/mcp/v1`
   - Setup: See `docs/MCP-SETUP.md`

2. **Gmail** (optional) — Send completion notifications.
   - URL: `https://gmailmcp.googleapis.com/mcp/v1`

3. **Airtable** (optional) — Store connection tables as a database.
   - URL: `https://mcp.airtable.com/mcp`

---

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for:
- "ANTHROPIC_API_KEY not found"
- "Google Drive MCP not responding"
- "Opus timeouts on large schematics"
- "Haiku's JSON parsing failed"

---

## References

- **Haiku 4.5:** Fast, cost-effective for classification & structured output. Best for triage.
- **Opus 4.8:** Deep reasoning, long-context (1M tokens). Best for complex workflows.
- **Google Drive MCP:** https://github.com/anthropics/mcp-servers/tree/main/src/gdrive
- **Anthropic API Docs:** https://docs.claude.com/en/api/overview
- **Claude Code Docs:** https://docs.claude.com/en/docs/claude-code/overview

---

## Support

- **Questions?** Check `docs/TROUBLESHOOTING.md` or the Anthropic docs.
- **Bugs?** Open an issue with logs from the last run (remove API keys).
- **Feature requests?** Submit a PR or discussion.

---

**Last updated:** June 2026  
**Tested with:** Claude Haiku 4.5, Opus 4.8, Google Drive MCP
