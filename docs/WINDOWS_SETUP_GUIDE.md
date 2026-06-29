# Windows Setup Guide — C:\Fixtures\engineering-docs

**Complete step-by-step guide for Windows users.**

---

## 📂 Your Folder Location

You've created: `C:\Fixtures\engineering-docs\`

This is your **main project folder**.

---

## Step 1: Create Subfolders

Open Command Prompt and run these commands:

```cmd
cd C:\Fixtures\engineering-docs
mkdir docs
mkdir scripts
mkdir outputs
```

Or use File Explorer:
1. Open `C:\Fixtures\engineering-docs\`
2. Right-click in empty space → **New → Folder**
3. Create 3 folders:
   - `docs`
   - `scripts`
   - `outputs`

**Result:**
```
C:\Fixtures\engineering-docs\
├── docs\
├── scripts\
└── outputs\
```

---

## Step 2: Download All Files

All files are in `/mnt/user-data/outputs/` (download from your Claude interface).

You need **14 files total**:

### **Main Folder Files** (11 files)
1. `orchestrator.py`
2. `wiring-block-diagrams.skill`
3. `.env.example`
4. `START_HERE.md`
5. `README.md`
6. `MASTER.md`
7. `WORKFLOW.md`
8. `MCP-SETUP.md`
9. `MCP_QUICK_REFERENCE.md`
10. `FILES_CHECKLIST.md`
11. `FOLDER_STRUCTURE.md`

### **Supporting Files** (3 files)
12. `DELIVERY_SUMMARY.txt`
13. `FINAL_SUMMARY.txt`
14. `QUICK_SETUP_COMMANDS.txt`

### **From Prior Session** (1 file)
15. `wiring-block-diagrams.skill` (already in list above)

---

## Step 3: Copy Files to Correct Locations

### Method A: Using File Explorer (GUI)

1. Open `C:\Fixtures\engineering-docs\` in File Explorer
2. Open your Downloads folder in another window
3. For each file below, drag it to the correct folder

**Copy to main folder:**
- `orchestrator.py`
- `wiring-block-diagrams.skill`
- `.env.example`
- `START_HERE.md`
- `README.md`
- `MASTER.md`
- `WORKFLOW.md`
- `MCP-SETUP.md`
- `MCP_QUICK_REFERENCE.md`
- `FILES_CHECKLIST.md`
- `FOLDER_STRUCTURE.md`

**Copy to `docs\` subfolder:**
- `DELIVERY_SUMMARY.txt`
- `FINAL_SUMMARY.txt`
- `QUICK_SETUP_COMMANDS.txt`

---

### Method B: Using Command Prompt (Faster)

Assuming files are in `C:\Users\YourName\Downloads\`:

Open Command Prompt and run:

```cmd
cd C:\Fixtures\engineering-docs

REM Copy main files
copy C:\Users\YourName\Downloads\orchestrator.py .
copy C:\Users\YourName\Downloads\wiring-block-diagrams.skill .
copy C:\Users\YourName\Downloads\.env.example .
copy C:\Users\YourName\Downloads\START_HERE.md .
copy C:\Users\YourName\Downloads\README.md .
copy C:\Users\YourName\Downloads\MASTER.md .
copy C:\Users\YourName\Downloads\WORKFLOW.md .
copy C:\Users\YourName\Downloads\MCP-SETUP.md .
copy C:\Users\YourName\Downloads\MCP_QUICK_REFERENCE.md .
copy C:\Users\YourName\Downloads\FILES_CHECKLIST.md .
copy C:\Users\YourName\Downloads\FOLDER_STRUCTURE.md .

REM Copy docs files
copy C:\Users\YourName\Downloads\DELIVERY_SUMMARY.txt docs\
copy C:\Users\YourName\Downloads\FINAL_SUMMARY.txt docs\
copy C:\Users\YourName\Downloads\QUICK_SETUP_COMMANDS.txt docs\

echo ✓ All files copied!
```

---

## Step 4: Verify Folder Structure

Your folder should now look like:

```
C:\Fixtures\engineering-docs\
├── orchestrator.py
├── wiring-block-diagrams.skill
├── .env.example
├── START_HERE.md
├── README.md
├── MASTER.md
├── WORKFLOW.md
├── MCP-SETUP.md
├── MCP_QUICK_REFERENCE.md
├── FILES_CHECKLIST.md
├── FOLDER_STRUCTURE.md
│
├── docs\
│   ├── DELIVERY_SUMMARY.txt
│   ├── FINAL_SUMMARY.txt
│   └── QUICK_SETUP_COMMANDS.txt
│
├── scripts\
│   (empty — will be auto-populated)
│
└── outputs\
    (empty — will be auto-populated)
```

**Verify in Command Prompt:**

```cmd
cd C:\Fixtures\engineering-docs
dir
dir docs\
```

You should see all files listed.

---

## Step 5: Create .env File

1. In `C:\Fixtures\engineering-docs\`, copy `.env.example` to `.env`

**Using Command Prompt:**
```cmd
cd C:\Fixtures\engineering-docs
copy .env.example .env
```

**Or using File Explorer:**
1. Right-click `.env.example`
2. Click **Copy**
3. Right-click in empty space
4. Click **Paste**
5. Rename the copy to `.env`

---

## Step 6: Edit .env with Your API Key

Get your API key from: https://console.anthropic.com/api-keys

**Using Notepad:**
1. Right-click `.env` in `C:\Fixtures\engineering-docs\`
2. Click **Open with → Notepad**
3. You'll see:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_DRIVE_PARENT_FOLDER_ID=
   ```
4. Replace `sk-ant-...` with your **actual API key** (copy from https://console.anthropic.com/api-keys)
5. Save (Ctrl+S)
6. Close

**Example after editing:**
```
ANTHROPIC_API_KEY=sk-ant-abc123def456ghi789...
GOOGLE_DRIVE_PARENT_FOLDER_ID=
```

⚠️ **Important:** Keep this file SECRET. Never share your API key.

---

## Step 7: Install Python Dependencies

Open Command Prompt:

```cmd
cd C:\Fixtures\engineering-docs
pip install anthropic python-dotenv
```

Wait for installation to complete. You should see:
```
Successfully installed anthropic python-dotenv
```

---

## Step 8: Test Your Setup

In Command Prompt:

```cmd
cd C:\Fixtures\engineering-docs
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

✓ **Setup is working!**

Type `done` and press Enter to exit.

---

## Step 9: Enable Google Drive MCP in Claude Code

1. Open Claude Code
2. Click **Customize** (bottom left or account menu)
3. Click **Connectors**
4. Find **Google Drive** → Click **Connect**
5. A browser window opens → Sign in with your Google account
6. Click **Allow**
7. Back in Claude Code → You should see **"Connected"** next to Google Drive

✓ **MCP is now active!**

---

## Step 10: Open Claude Code in Your Project Folder

Open Command Prompt:

```cmd
cd C:\Fixtures\engineering-docs
claude code
```

Claude Code should open with your project folder as the working directory.

---

## ✅ Final Verification

Check that everything is in place:

```cmd
cd C:\Fixtures\engineering-docs

REM List main folder files
dir

REM List docs folder
dir docs\

REM Verify .env exists
type .env

REM Test Python script
python orchestrator.py
```

Expected output:
- ✓ All files present
- ✓ .env shows your API key
- ✓ orchestrator.py shows prompt

---

## 🚀 You're Ready!

Run your first engineering documentation task:

```cmd
cd C:\Fixtures\engineering-docs
python orchestrator.py
```

Paste a task description and watch Haiku analyze it, then Opus create the diagrams!

---

## Windows-Specific Troubleshooting

### "python: command not found"

**Solution:** Python is not in your PATH.

Option 1: Download Python from https://www.python.org/downloads/
- During installation, CHECK: "Add Python to PATH"
- Then restart Command Prompt

Option 2: Use full path to python:
```cmd
C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe orchestrator.py
```

### "pip: command not found"

**Solution:** Same as above — Python not in PATH. Install/reinstall Python with "Add to PATH" option checked.

### "ModuleNotFoundError: No module named 'anthropic'"

**Solution:** Install dependencies again:
```cmd
cd C:\Fixtures\engineering-docs
pip install --upgrade anthropic python-dotenv
```

### "The system cannot find the path specified"

**Solution:** Make sure you're in the right folder:
```cmd
cd C:\Fixtures\engineering-docs
dir
```

Should show all your files. If not, check the path is correct.

### ".env file not found"

**Solution:** You created `.env.example` but not `.env`.

```cmd
cd C:\Fixtures\engineering-docs
copy .env.example .env
notepad .env
```

Then paste your API key and save.

---

## Folder Structure Reference

Your final structure should be:

```
C:\Fixtures\engineering-docs\
│
├── orchestrator.py                    ← Main script
├── wiring-block-diagrams.skill        ← Bundled skill
├── .env                               ← Your API key (created from .env.example)
├── START_HERE.md                      ← Entry point
├── README.md
├── MASTER.md
├── WORKFLOW.md
├── MCP-SETUP.md
├── MCP_QUICK_REFERENCE.md
├── FILES_CHECKLIST.md
├── FOLDER_STRUCTURE.md
│
├── docs\                              ← Documentation subfolder
│   ├── DELIVERY_SUMMARY.txt
│   ├── FINAL_SUMMARY.txt
│   └── QUICK_SETUP_COMMANDS.txt
│
├── scripts\                           ← Auto-created, helper scripts
│
└── outputs\                           ← Auto-created, generated files
```

---

## Quick Command Reference

All commands assume you're in `C:\Fixtures\engineering-docs\`:

```cmd
# Navigate to project
cd C:\Fixtures\engineering-docs

# Create subfolders
mkdir docs scripts outputs

# Copy files (adjust path to your Downloads)
copy %USERPROFILE%\Downloads\orchestrator.py .

# Create .env
copy .env.example .env

# Edit .env
notepad .env

# Install dependencies
pip install anthropic python-dotenv

# Test setup
python orchestrator.py

# Open Claude Code
claude code
```

---

## Next Steps

1. ✓ Create folders (Step 1)
2. ✓ Download all files (Step 2)
3. ✓ Copy files to correct locations (Step 3)
4. ✓ Create .env with API key (Steps 5-6)
5. ✓ Install dependencies (Step 7)
6. ✓ Test setup (Step 8)
7. ✓ Enable Google Drive MCP (Step 9)
8. ✓ Open Claude Code (Step 10)
9. → Run your first task!

---

**Good luck! 🚀**

If you get stuck, check the Windows-Specific Troubleshooting section above.
