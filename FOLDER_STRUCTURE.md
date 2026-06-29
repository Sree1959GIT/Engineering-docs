# Folder Structure & File Placement Guide

**Follow this exactly to set up your project folder.**

---

## Step 1: Create the Folder Structure

Copy and paste this into your terminal:

```bash
mkdir -p ~/engineering-docs
mkdir -p ~/engineering-docs/docs
mkdir -p ~/engineering-docs/scripts
mkdir -p ~/engineering-docs/outputs
cd ~/engineering-docs
```

This creates:
```
~/engineering-docs/                 ← Main project folder (your working directory)
├── docs/                           ← Documentation subfolder
├── scripts/                        ← Helper scripts subfolder
└── outputs/                        ← Local output files subfolder
```

---

## Step 2: Download All Files from `/mnt/user-data/outputs/`

You need to download these **11 files** from `/mnt/user-data/outputs/`:

1. `START_HERE.md`
2. `README.md`
3. `MASTER.md`
4. `WORKFLOW.md`
5. `MCP-SETUP.md`
6. `MCP_QUICK_REFERENCE.md`
7. `FILES_CHECKLIST.md`
8. `engineering-docs-orchestrator.py`
9. `.env.example`
10. `DELIVERY_SUMMARY.txt`
11. `FINAL_SUMMARY.txt`

**Also download from prior session outputs:**
12. `wiring-block-diagrams.skill`

---

## Step 3: Place Files in Correct Locations

Follow this table to place each file in the right folder:

| File | Destination | Full Path |
|------|-------------|-----------|
| `START_HERE.md` | Main folder | `~/engineering-docs/START_HERE.md` |
| `README.md` | docs/ | `~/engineering-docs/docs/README.md` |
| `MASTER.md` | docs/ | `~/engineering-docs/docs/MASTER.md` |
| `WORKFLOW.md` | docs/ | `~/engineering-docs/docs/WORKFLOW.md` |
| `MCP-SETUP.md` | docs/ | `~/engineering-docs/docs/MCP-SETUP.md` |
| `MCP_QUICK_REFERENCE.md` | docs/ | `~/engineering-docs/docs/MCP_QUICK_REFERENCE.md` |
| `FILES_CHECKLIST.md` | docs/ | `~/engineering-docs/docs/FILES_CHECKLIST.md` |
| `DELIVERY_SUMMARY.txt` | docs/ | `~/engineering-docs/docs/DELIVERY_SUMMARY.txt` |
| `FINAL_SUMMARY.txt` | docs/ | `~/engineering-docs/docs/FINAL_SUMMARY.txt` |
| `engineering-docs-orchestrator.py` | Main folder | `~/engineering-docs/orchestrator.py` |
| `.env.example` | Main folder | `~/engineering-docs/.env.example` |
| `wiring-block-diagrams.skill` | Main folder | `~/engineering-docs/wiring-block-diagrams.skill` |

---

## Final Folder Structure (After All Files Placed)

```
~/engineering-docs/                                    ← YOUR MAIN PROJECT FOLDER
├── orchestrator.py                                   ← Main script (rename from engineering-docs-orchestrator.py)
├── wiring-block-diagrams.skill                       ← Bundled skill
├── .env.example                                      ← Config template
├── START_HERE.md                                     ← Entry point (READ FIRST!)
│
├── docs/                                             ← Documentation subfolder
│   ├── README.md                                     ← Quick start guide
│   ├── MASTER.md                                     ← Full architecture
│   ├── WORKFLOW.md                                   ← Detailed example
│   ├── MCP-SETUP.md                                  ← MCP setup guide
│   ├── MCP_QUICK_REFERENCE.md                        ← MCP cheat sheet
│   ├── FILES_CHECKLIST.md                            ← Setup verification
│   ├── DELIVERY_SUMMARY.txt                          ← What you got
│   └── FINAL_SUMMARY.txt                             ← Visual summary
│
├── scripts/                                          ← Helper scripts (auto-created after running)
│   ├── schematic_lib.py                              ← From .skill (SVG library)
│   ├── fixture_diagrammer.py                         ← From .skill (matplotlib engine)
│   ├── schemdraw_example.py                          ← From .skill (example)
│   └── render_pdf.js                                 ← From .skill (PDF renderer)
│
└── outputs/                                          ← Generated files (auto-created when you run)
    ├── {ProjectName}_Schematic.pdf                   ← Generated PDFs
    ├── {ProjectName}_ConnectionTable.csv             ← Generated CSVs
    └── {ProjectName}_BlockDescriptions.txt           ← Generated descriptions
```

---

## Step-by-Step File Placement Instructions

### Using Terminal (Recommended)

If you downloaded files to `~/Downloads/`, use these commands:

```bash
# Navigate to your project folder
cd ~/engineering-docs

# Copy files from Downloads to their correct locations
cp ~/Downloads/START_HERE.md .
cp ~/Downloads/engineering-docs-orchestrator.py orchestrator.py
cp ~/Downloads/.env.example .
cp ~/Downloads/wiring-block-diagrams.skill .

# Copy documentation files to docs/ subfolder
cp ~/Downloads/README.md docs/
cp ~/Downloads/MASTER.md docs/
cp ~/Downloads/WORKFLOW.md docs/
cp ~/Downloads/MCP-SETUP.md docs/
cp ~/Downloads/MCP_QUICK_REFERENCE.md docs/
cp ~/Downloads/FILES_CHECKLIST.md docs/
cp ~/Downloads/DELIVERY_SUMMARY.txt docs/
cp ~/Downloads/FINAL_SUMMARY.txt docs/

# Verify everything is in place
ls -la ~/engineering-docs/
ls -la ~/engineering-docs/docs/
```

### Using GUI (Mac/Windows)

1. Open Finder / File Explorer
2. Navigate to `~/engineering-docs/`
3. **For main folder files:**
   - Drag these 4 files to `~/engineering-docs/`:
     - `START_HERE.md`
     - `orchestrator.py` (renamed from `engineering-docs-orchestrator.py`)
     - `.env.example`
     - `wiring-block-diagrams.skill`
4. **For docs subfolder:**
   - Drag these 9 files to `~/engineering-docs/docs/`:
     - `README.md`
     - `MASTER.md`
     - `WORKFLOW.md`
     - `MCP-SETUP.md`
     - `MCP_QUICK_REFERENCE.md`
     - `FILES_CHECKLIST.md`
     - `DELIVERY_SUMMARY.txt`
     - `FINAL_SUMMARY.txt`

---

## Step 4: Create `.env` File

In your main folder (`~/engineering-docs/`):

```bash
cd ~/engineering-docs

# Copy the template
cp .env.example .env

# Edit it with your API key
nano .env
```

Or use your favorite editor. Add:

```
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_DRIVE_PARENT_FOLDER_ID=
```

Replace `sk-ant-...` with your actual API key from https://console.anthropic.com/api-keys

Save and close.

---

## Step 5: Install Python Dependencies

```bash
cd ~/engineering-docs
pip install anthropic python-dotenv
```

---

## Step 6: Open Claude Code CLI in Your Project Folder

### Option A: Open Claude Code in Your Project (Recommended)

```bash
cd ~/engineering-docs
claude code
```

This opens Claude Code with your project folder as the working directory. ✓

### Option B: Launch Claude Code and Open Folder

```bash
# Just launch Claude Code
claude code

# Then in Claude Code:
# File → Open Folder → Navigate to ~/engineering-docs/ → Open
```

### Option C: From Web

Go to https://claude.ai/code and it will open in your browser.

---

## Step 7: Verify Setup

Once Claude Code is open with your project folder:

1. **Check file structure** — Left sidebar should show:
   ```
   📁 engineering-docs
      ├── orchestrator.py
      ├── wiring-block-diagrams.skill
      ├── .env
      ├── START_HERE.md
      └── docs/
          ├── README.md
          ├── MASTER.md
          └── ...
   ```

2. **Test the script** — In Claude Code terminal:
   ```bash
   python orchestrator.py
   ```
   
   Should show:
   ```
   ================================================================================
   ENGINEERING DOCUMENTATION ORCHESTRATOR (Haiku → Opus → Drive)
   ================================================================================
   
   [Step 1] Describe your engineering task:
   ```

3. **Enable Google Drive MCP:**
   - Click **Customize** (Claude Code interface)
   - Click **Connectors**
   - Find **Google Drive** → Click **Connect**
   - Authorize with your Google account

✓ **Setup complete!**

---

## Quick Copy-Paste Bash Script

If you want to automate this, create a setup script:

```bash
#!/bin/bash

# Create folder structure
mkdir -p ~/engineering-docs/{docs,scripts,outputs}
cd ~/engineering-docs

# Download files (assumes they're in ~/Downloads/)
cp ~/Downloads/START_HERE.md .
cp ~/Downloads/engineering-docs-orchestrator.py orchestrator.py
cp ~/Downloads/.env.example .
cp ~/Downloads/wiring-block-diagrams.skill .

cp ~/Downloads/README.md docs/
cp ~/Downloads/MASTER.md docs/
cp ~/Downloads/WORKFLOW.md docs/
cp ~/Downloads/MCP-SETUP.md docs/
cp ~/Downloads/MCP_QUICK_REFERENCE.md docs/
cp ~/Downloads/FILES_CHECKLIST.md docs/
cp ~/Downloads/DELIVERY_SUMMARY.txt docs/
cp ~/Downloads/FINAL_SUMMARY.txt docs/

# Install dependencies
pip install anthropic python-dotenv

# Create .env from template
cp .env.example .env

echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and paste your ANTHROPIC_API_KEY"
echo "2. Enable Google Drive MCP in Claude Code"
echo "3. Run: claude code (to open in this folder)"
echo "4. Run: python orchestrator.py"
```

Save this as `setup.sh`, then run:
```bash
bash setup.sh
```

---

## Final Checklist

```
Folder Structure
[ ] ~/engineering-docs/ created
[ ] ~/engineering-docs/docs/ created
[ ] ~/engineering-docs/scripts/ created
[ ] ~/engineering-docs/outputs/ created

Files in Main Folder
[ ] orchestrator.py (renamed from engineering-docs-orchestrator.py)
[ ] wiring-block-diagrams.skill
[ ] .env.example
[ ] START_HERE.md

Files in docs/ Subfolder
[ ] README.md
[ ] MASTER.md
[ ] WORKFLOW.md
[ ] MCP-SETUP.md
[ ] MCP_QUICK_REFERENCE.md
[ ] FILES_CHECKLIST.md
[ ] DELIVERY_SUMMARY.txt
[ ] FINAL_SUMMARY.txt

Configuration
[ ] .env created (copied from .env.example)
[ ] .env has your ANTHROPIC_API_KEY set

Dependencies
[ ] pip install anthropic python-dotenv ran successfully

Claude Code
[ ] Opened Claude Code in ~/engineering-docs/ folder
[ ] Google Drive MCP enabled ("Connected" status)
[ ] python orchestrator.py works (shows prompt)
```

---

## Troubleshooting Folder Setup

### "File not found" error when running `python orchestrator.py`

**Check:**
- Are you in the right folder? `pwd` should show `/Users/your-name/engineering-docs` (Mac) or `C:\Users\your-name\engineering-docs` (Windows)
- Is `orchestrator.py` in that folder? `ls orchestrator.py` or `dir orchestrator.py`

**Fix:**
```bash
cd ~/engineering-docs
ls -la orchestrator.py  # Verify it's there
python orchestrator.py  # Try again
```

### "Permission denied" when opening Claude Code

```bash
# Make sure you have execute permission
chmod +x ~/engineering-docs/orchestrator.py

# Then try again
cd ~/engineering-docs
python orchestrator.py
```

### "Module not found" for anthropic

```bash
# Install in the right environment
pip install --upgrade anthropic python-dotenv

# Verify
python -c "import anthropic; print(anthropic.__version__)"
```

---

## Summary

**Your folder will look like this after setup:**

```
~/engineering-docs/
├── orchestrator.py                    ← Main script
├── wiring-block-diagrams.skill        ← Bundled skill
├── .env                               ← Your API key (created from .env.example)
├── START_HERE.md                      ← Read first!
├── docs/                              ← All documentation
│   ├── README.md
│   ├── MASTER.md
│   ├── WORKFLOW.md
│   ├── MCP-SETUP.md
│   ├── MCP_QUICK_REFERENCE.md
│   ├── FILES_CHECKLIST.md
│   ├── DELIVERY_SUMMARY.txt
│   └── FINAL_SUMMARY.txt
├── scripts/                           ← Auto-created, contains helper scripts
└── outputs/                           ← Auto-created, contains generated files
```

**To run Claude Code in this folder:**

```bash
cd ~/engineering-docs
claude code
```

Done! 🚀
