# Files Checklist — What You Need to Copy & Setup

This file tells you exactly what to download/copy and where to put it in your Claude Code project.

---

## Files Created for You (In This Session)

### Core Scripts & Config

| File | Source | Destination | Purpose |
|------|--------|-------------|---------|
| `orchestrator.py` | `/home/claude/engineering-docs-orchestrator.py` | `~/engineering-docs/orchestrator.py` | Main routing script (Haiku + Opus) |
| `MASTER.md` | `/home/claude/MASTER.md` | `~/engineering-docs/MASTER.md` | System instructions for Claude Code |
| `README.md` | `/home/claude/README.md` | `~/engineering-docs/README.md` | Quick start & overview |
| `.env.example` | `/home/claude/.env.example` | `~/engineering-docs/.env.example` | Config template |
| `MCP-SETUP.md` | `/home/claude/MCP-SETUP.md` | `~/engineering-docs/MCP-SETUP.md` | Google Drive MCP connection guide |
| `WORKFLOW.md` | `/home/claude/WORKFLOW.md` | `~/engineering-docs/WORKFLOW.md` | Detailed example execution |

### From Prior Session (You Already Have)

| File | Location | Destination | Purpose |
|------|----------|-------------|---------|
| `wiring-block-diagrams.skill` | `/mnt/user-data/outputs/wiring-block-diagrams.skill` | `~/engineering-docs/wiring-block-diagrams.skill` | Engineering diagram skill |
| `schematic_lib.py` | (bundled in skill) | `~/engineering-docs/scripts/schematic_lib.py` | SVG schematic primitives |
| `fixture_diagrammer.py` | (bundled in skill) | `~/engineering-docs/scripts/fixture_diagrammer.py` | Matplotlib diagram engine |
| `render_pdf.js` | (bundled in skill) | `~/engineering-docs/scripts/render_pdf.js` | HTML→PDF renderer |

---

## Step-by-Step Setup

### Step 1: Create Your Project Directory

```bash
mkdir -p ~/engineering-docs
cd ~/engineering-docs
```

### Step 2: Copy Core Files (From This Session)

Copy these files from `/home/claude/` to `~/engineering-docs/`:

```bash
# Copy the orchestrator and documentation
cp /home/claude/engineering-docs-orchestrator.py orchestrator.py
cp /home/claude/MASTER.md .
cp /home/claude/README.md .
cp /home/claude/MCP-SETUP.md .
cp /home/claude/WORKFLOW.md .
cp /home/claude/.env.example .
```

### Step 3: Copy Skill File (From Prior Session)

```bash
# Copy the skill from your outputs
cp /mnt/user-data/outputs/wiring-block-diagrams.skill .
```

### Step 4: Extract Skill Scripts

The `.skill` file is a ZIP. Extract it to get the bundled scripts:

```bash
# Unzip the skill (it's a ZIP archive)
unzip wiring-block-diagrams.skill -d ./skill-contents

# Copy the scripts folder to your project
mkdir -p scripts
cp ./skill-contents/scripts/* ./scripts/

# Clean up temp folder (optional)
rm -rf ./skill-contents
```

### Step 5: Create `.env` File

```bash
# Copy the template
cp .env.example .env

# Edit .env with your API key
nano .env
# Paste your Anthropic API key: ANTHROPIC_API_KEY=sk-ant-...
# Save and exit (Ctrl+O, Enter, Ctrl+X)
```

### Step 6: Install Python Dependencies

```bash
pip install anthropic python-dotenv
```

### Step 7: Enable Google Drive MCP in Claude Code

**Follow steps in `MCP-SETUP.md`** (see below for quick version).

---

## Final Project Structure

After all steps, your `~/engineering-docs/` should look like:

```
engineering-docs/
├── orchestrator.py                    ✓ (Main script)
├── wiring-block-diagrams.skill        ✓ (Bundled skill — Claude Code loads this)
├── MASTER.md                          ✓ (System instructions)
├── README.md                          ✓ (Quick start)
├── MCP-SETUP.md                       ✓ (MCP connection guide)
├── WORKFLOW.md                        ✓ (Example execution)
├── .env.example                       ✓ (Config template)
├── .env                               ✓ (Your config — DO NOT COMMIT)
├── scripts/
│   ├── schematic_lib.py               ✓ (SVG library)
│   ├── fixture_diagrammer.py          ✓ (Matplotlib engine)
│   ├── schemdraw_example.py           ✓ (Example)
│   └── render_pdf.js                  ✓ (PDF renderer)
└── outputs/                           (Auto-created on first run)
    ├── GCF-TestRig_Schematic.pdf
    ├── GCF-TestRig_ConnectionTable.csv
    └── ...
```

**✓ = File exists**

---

## Quick Test

To verify everything is set up correctly, run:

```bash
cd ~/engineering-docs
python orchestrator.py
```

You should see:

```
================================================================================
ENGINEERING DOCUMENTATION ORCHESTRATOR (Haiku → Opus → Drive)
================================================================================

[Step 1] Describe your engineering task:
(Paste sketch description, CSV path, or wiring requirements)
---
```

If you get this prompt, you're ready to go! ✓

---

## Important Notes

### `.env` Security

- **DO NOT commit `.env` to version control** — it contains your API key.
- Add `.env` to `.gitignore` if using Git:
  ```bash
  echo ".env" >> .gitignore
  ```
- **Keep your API key secret** — anyone with it can call the Claude API on your dime.

### Skill File

- The `wiring-block-diagrams.skill` file is a bundled package (ZIP format).
- Claude Code automatically recognizes `.skill` files in your project and loads them into Opus's context.
- **You don't need to unzip it manually** — Claude Code does this for you.
- However, the Python scripts inside are also useful as standalone tools (see `scripts/` directory).

### MCP Connector

- You must enable **Google Drive MCP** in Claude Code for the orchestrator to save outputs.
- See `MCP-SETUP.md` for detailed steps.
- Quick check: in Claude Code, can you ask "List my Google Drive folders"? If yes, MCP is connected.

---

## What to Do Next

1. **Complete the setup above** — Copy files, set `.env`, install dependencies.
2. **Enable Google Drive MCP** — Follow `MCP-SETUP.md`.
3. **Run your first task:**
   ```bash
   python orchestrator.py
   ```
4. **Describe a simple engineering task** — e.g., 3-phase motor control with relays.
5. **Review the output** — Check Google Drive for the generated PDF and tables.
6. **Iterate** — If [VERIFY] items appear, correct them and re-run.

---

## Checklist (Copy & Paste)

Use this to track your setup progress:

```
[ ] Step 1: Create ~/engineering-docs directory
[ ] Step 2: Copy 6 files from /home/claude/ to ~/engineering-docs/
[ ] Step 3: Copy wiring-block-diagrams.skill from /mnt/user-data/outputs/
[ ] Step 4: Extract skill scripts to scripts/ folder
[ ] Step 5: Create .env with your ANTHROPIC_API_KEY
[ ] Step 6: pip install anthropic python-dotenv
[ ] Step 7: Enable Google Drive MCP in Claude Code (see MCP-SETUP.md)
[ ] Step 8: Test: python orchestrator.py (should show prompt)
[ ] Step 9: Run first task with sample description
[ ] Step 10: Check Google Drive for outputs
```

---

## File Sizes (For Reference)

| File | Size |
|------|------|
| orchestrator.py | ~8 KB |
| MASTER.md | ~15 KB |
| README.md | ~12 KB |
| wiring-block-diagrams.skill | ~18.5 KB (ZIP) |
| Total | ~53.5 KB |

All files are lightweight and fast to download.

---

## Support

- **Setup issues?** Check the file names and paths above.
- **Claude Code issues?** See `README.md` troubleshooting section.
- **MCP not connecting?** See `MCP-SETUP.md` troubleshooting.
- **Script errors?** Check `orchestrator.py` comments — they explain each phase.

---

**Ready to set up?** Start with Step 1 above and work through the checklist. You'll be running your first engineering documentation in ~10 minutes.
