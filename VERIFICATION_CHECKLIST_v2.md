# ✅ UPDATED VERIFICATION CHECKLIST
## Before Running orchestrator.py (OAuth + Local venv)

---

## ✅ STEP 1: VERIFY FOLDER STRUCTURE

Run in Command Prompt:
```cmd
cd C:\Fixtures\engineering-docs
dir
```

You should see:
- ✓ `orchestrator.py` (updated with auth.py)
- ✓ `auth.py` (NEW — credential manager)
- ✓ `requirements.txt` (NEW — dependencies)
- ✓ `.env` (updated)
- ✓ `.env.example` (updated)
- ✓ `.gitignore` (NEW — protects credentials)
- ✓ `SETUP_COMPLETE.md` (NEW — this setup guide)
- ✓ `START_HERE.md`
- ✓ `README.md`
- ✓ `docs\` (folder)
- ✓ `scripts\` (folder)
- ✓ `outputs\` (folder)
- ✓ `venv\` (folder) ← NEW LOCAL VENV

### Verify scripts folder:
```cmd
dir scripts\
```

Should show:
- ✓ `schematic_lib.py`
- ✓ `fixture_diagrammer.py`
- ✓ `schemdraw_example.py`
- ✓ `render_pdf.js`

**Check: [ ] Folder structure is correct**

---

## ✅ STEP 2: VERIFY LOCAL VIRTUAL ENVIRONMENT

**Activate virtual environment:**

### Windows (Command Prompt):
```cmd
cd C:\Fixtures\engineering-docs
venv\Scripts\activate
```

You should see `(venv)` at the start of your prompt:
```
(venv) C:\Fixtures\engineering-docs>
```

### Windows (PowerShell):
```powershell
cd C:\Fixtures\engineering-docs
.\venv\Scripts\Activate.ps1
```

### macOS/Linux:
```bash
cd C:\Fixtures\engineering-docs
source venv/bin/activate
```

### Verify Python packages:
```bash
pip list
```

Should show:
- ✓ `anthropic` (≥0.28.0)
- ✓ `python-dotenv` (≥1.0.0)
- ✓ `requests` (≥2.31.0)
- ✓ (and their dependencies)

### Verify Python version:
```bash
python --version
```

Should show: `Python 3.x.x` (3.9 or higher)

**Check: [ ] Virtual environment is working and packages are installed**

---

## ✅ STEP 3: VERIFY AUTHENTICATION SETUP

The new `auth.py` handles credentials with three methods (in priority order):

### Method 1: Environment Variable (if you prefer)
```bash
# Optional: set this if you want
set ANTHROPIC_API_KEY=sk-ant-...
```

### Method 2: Local Credentials File
The script will check for: `~/.claude-engineering/credentials.json`

You can pre-setup credentials with:
```bash
python auth.py --setup
```

### Method 3: Interactive Prompt (default)
First run will prompt you to paste your API key.

### Get your API key:
1. Go to: https://console.anthropic.com/api-keys
2. Sign in with your Claude subscription
3. Create or copy your API key
4. Should start with `sk-ant-`

### Check authentication status:
```bash
python auth.py --status
```

Should show something like:
```
Authentication Status:
  env_var_set: False
  local_creds_exist: True
  api_key_loaded: True
  config_dir: C:\Users\YourUsername\.claude-engineering
```

**Check: [ ] Authentication is set up (interactive or pre-configured)**

---

## ✅ STEP 4: VERIFY PYTHON SCRIPT SYNTAX

Make sure venv is activated first:
```bash
venv\Scripts\activate
```

Then compile and check syntax:
```bash
python -m py_compile orchestrator.py
python -m py_compile auth.py
python -m py_compile scripts\schematic_lib.py
python -m py_compile scripts\fixture_diagrammer.py
python -m py_compile scripts\schemdraw_example.py
```

Should show no errors. If there are errors, let me know!

**Check: [ ] All Python files have valid syntax**

---

## ✅ STEP 5: VERIFY OUTPUTS FOLDER

The `outputs/` folder exists for saving generated diagrams:
```bash
dir outputs\
```

Should show empty (or previously generated files).

**Check: [ ] Outputs folder exists**

---

## ✅ STEP 6: READY TO RUN!

Make sure:
- [ ] Virtual environment is activated (shows `(venv)` in prompt)
- [ ] Folder structure is correct
- [ ] Venv packages are installed (`pip list` shows anthropic, etc.)
- [ ] Authentication is ready (env var, local file, or interactive)
- [ ] Scripts are in `scripts\` folder
- [ ] `outputs\` folder exists
- [ ] All syntax is valid (no errors from `py_compile`)

Then run:
```bash
python orchestrator.py
```

---

## 🚀 FIRST TEST RUN

When you run `python orchestrator.py`, you'll see:

```
======================================================================
ENGINEERING DOCUMENTATION ORCHESTRATOR (Haiku → Opus → Drive)
======================================================================

[Step 1] Describe your engineering task:
(Paste sketch description, CSV path, or wiring requirements)
---
```

### Example input:
```
AC 3-phase motor control via 5A relay K1.
RTD sensors T1, T2, T3 on CU1 to DMM.
Wattmeter on motor phases.
done
```

Then press Enter and:
1. **Step 2:** Haiku analyzes (15 seconds)
2. **Step 3:** Opus creates (3-4 minutes)
3. **Step 4:** Google Drive saves (if MCP enabled)

You'll see output like:
```
======================================================================
PHASE 1: Triaging with Haiku 4.5 (tool selection & requirements)
======================================================================

[Haiku Response]
{
  "task_type": "schematic",
  "standard": "IEC 60617",
  ...
}
```

Results will be saved to: `outputs/` folder

---

## 📝 QUICK CHECKLIST

Before running:

- [ ] `cd C:\Fixtures\engineering-docs`
- [ ] `venv\Scripts\activate` (shows `(venv)` in prompt)
- [ ] `python auth.py --status` (verify auth is ready)
- [ ] `pip list` (shows anthropic, python-dotenv, requests)
- [ ] `dir scripts\` (shows 4 files)
- [ ] `python orchestrator.py` (start workflow)
- [ ] Paste engineering task description
- [ ] Wait 4-5 minutes
- [ ] Check `outputs/` folder for results

---

## ⚠️ TROUBLESHOOTING

### Problem: `(venv)` doesn't show in prompt
**Solution:**
```bash
# Windows Command Prompt
venv\Scripts\activate

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### Problem: "ModuleNotFoundError: No module named 'anthropic'"
**Solution:**
```bash
# Make sure venv is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: "ModuleNotFoundError: No module named 'auth'"
**Solution:**
- Make sure you're in the `C:\Fixtures\engineering-docs` directory
- Check that `auth.py` exists in the root folder
- Make sure venv is activated

### Problem: "No API key found, would you like to set one up?"
**Solution (do one of these):**
```bash
# Option 1: Interactive setup
python auth.py --setup

# Option 2: Set environment variable
set ANTHROPIC_API_KEY=sk-ant-...
python orchestrator.py

# Option 3: Get your key and paste on first run
# Script will prompt you if not found
python orchestrator.py
```

### Problem: "Invalid API key format"
**Solution:**
- Your API key should start with `sk-ant-`
- Go to: https://console.anthropic.com/api-keys
- Get your REAL key (not the placeholder `sk-ant-...`)
- Try again

### Problem: "scripts folder files not found"
**Solution:**
- Verify all 4 files are in `C:\Fixtures\engineering-docs\scripts\`
- Run: `dir scripts\`

### Problem: Credentials not persisting between runs
**Solution:**
```bash
# Check if credentials are stored
dir %USERPROFILE%\.claude-engineering\

# If file exists, it's working
# If not, run auth.py --setup to create it
python auth.py --setup
```

### Problem: Certificate/SSL error when installing packages
**Solution:**
```bash
# Upgrade pip, setuptools, wheel
venv\Scripts\pip install --upgrade pip setuptools wheel

# Retry installation
pip install -r requirements.txt
```

---

## 🔐 SECURITY REMINDERS

- ✓ API keys are stored locally in `~/.claude-engineering/credentials.json`
- ✓ File permissions are restricted to user-only access
- ✓ `.gitignore` prevents accidental credential commits
- ✓ No hardcoded API keys in source code
- ✓ Environment variable takes priority (good for CI/CD)

### If credentials are compromised:
```bash
# Revoke locally stored credentials
python auth.py --revoke

# Get a new API key from console.anthropic.com
# Run setup again
python auth.py --setup
```

---

## 📚 ADDITIONAL RESOURCES

- **Anthropic API Docs:** https://docs.anthropic.com
- **Claude Console:** https://console.anthropic.com/api-keys
- **Project Guide:** See `SETUP_COMPLETE.md`
- **Quick Start:** See `START_HERE.md`

---

**You're ready to go! Follow the steps above and let me know if you hit any issues.** 🚀

---

## Changes from Previous Checklist

| Feature | Before | After |
|---------|--------|-------|
| **Virtual Environment** | User/AppData (system-wide) | Local venv folder (isolated) |
| **API Key** | Required in .env (hardcoded) | OAuth-style credential manager |
| **Authentication** | Environment variable only | 3 methods: env var, local file, interactive |
| **Credentials Storage** | In .env (tracked) | Secure local file (git-ignored) |
| **Dependencies** | No requirements.txt | `requirements.txt` (reproducible) |
| **Security** | API key in repo | Credentials protected, git-ignored |
| **Setup Complexity** | Manual key management | Interactive setup on first run |

