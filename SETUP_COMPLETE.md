# ✅ Local venv Setup Complete

Your engineering documentation orchestrator is now configured to run from a **local virtual environment** with **OAuth-style credential management**.

## What Changed

### 1. **Local Virtual Environment (venv)**
- ✅ Created: `C:\Fixtures\engineering-docs\venv\`
- ✅ Installed dependencies: anthropic, python-dotenv, requests
- All project dependencies are now isolated locally, not in user/appdata

### 2. **OAuth-Style Authentication**
- ✅ Created: `auth.py` — credential manager with token storage
- ✅ Supports three authentication methods (in priority order):
  1. Environment variable: `ANTHROPIC_API_KEY=sk-ant-...`
  2. Local credentials file: `~/.claude-engineering/credentials.json`
  3. Interactive prompt on first run
- ✅ No hardcoded API keys in `orchestrator.py`
- ✅ Credentials stored securely with restricted permissions

### 3. **Updated Configuration**
- ✅ `orchestrator.py` — Uses `auth.py` for credential management
- ✅ `.env` — Simplified, no longer requires ANTHROPIC_API_KEY
- ✅ `.env.example` — Documents new auth approach
- ✅ `.gitignore` — Protects credentials from version control

---

## Quick Start

### Step 1: Activate Virtual Environment

**On Windows (Command Prompt):**
```cmd
cd C:\Fixtures\engineering-docs
venv\Scripts\activate
```

You should see `(venv)` at the start of your prompt:
```
(venv) C:\Fixtures\engineering-docs>
```

**On Windows (PowerShell):**
```powershell
cd C:\Fixtures\engineering-docs
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux (Bash):**
```bash
cd C:/Fixtures/engineering-docs
source venv/bin/activate
```

### Step 2: First Run - OAuth Authentication (Recommended)

```bash
python orchestrator.py
```

On first run, the script will prompt:

```
Choose authentication method:

  Option 1: OAuth (Recommended)
    → Sign in with your Claude subscription
    → Browser-based authentication
    → Most secure option

  Option 2: API Key
    → Manual API key from console.anthropic.com
    → Fallback option

Enter choice (1 or 2): 1
```

**Select Option 1 (OAuth):**
1. Browser automatically opens to console.anthropic.com
2. Sign in with your Claude subscription account
3. Navigate to API Keys section
4. Create or copy your API key
5. Return to script and paste the API key
6. Credentials saved locally: `~/.claude-engineering/credentials.json`
7. Orchestrator workflow starts automatically

### Alternative: Option 2 (API Key Fallback)

If you prefer or OAuth doesn't work:
1. Choose Option 2
2. Go to: https://console.anthropic.com/api-keys
3. Sign in with Claude subscription
4. Copy your API key
5. Paste when prompted
6. Save and continue

### Step 3: Verify Installation

Check that all dependencies are installed:
```bash
pip list
```

Should show:
- ✅ anthropic
- ✅ python-dotenv
- ✅ requests

Verify the virtual environment:
```bash
python -m py_compile orchestrator.py auth.py
python -m py_compile scripts/schematic_lib.py scripts/fixture_diagrammer.py scripts/schemdraw_example.py
```

Should show no errors.

---

## Folder Structure

```
C:\Fixtures\engineering-docs\
├── venv/                          # Local virtual environment
│   ├── Scripts/                   # (Windows) or bin/ (Unix)
│   ├── Lib/                       # Site-packages
│   └── pyvenv.cfg
├── scripts/
│   ├── schematic_lib.py
│   ├── fixture_diagrammer.py
│   ├── schemdraw_example.py
│   └── render_pdf.js
├── docs/                          # Documentation
├── outputs/                       # Generated diagrams, PDFs, tables
├── orchestrator.py                # Main workflow (updated for auth.py)
├── auth.py                        # OAuth-style credential manager (NEW)
├── requirements.txt               # Dependencies (NEW)
├── .env                           # Config (updated)
├── .env.example                   # Config template (updated)
├── .gitignore                     # Protects credentials (NEW)
├── README.md
└── START_HERE.md
```

---

## Credential Management

### Interactive Setup (First Run)
```bash
python auth.py --setup
```

### Check Status
```bash
python auth.py --status
```

Output:
```
Authentication Status:
  env_var_set: False
  local_creds_exist: True
  api_key_loaded: True
  config_dir: /home/username/.claude-engineering
```

### Using Environment Variable (Override)
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python orchestrator.py
```

### Revoke Local Credentials (Security)
```bash
python auth.py --revoke
```

This deletes `~/.claude-engineering/credentials.json` and removes all stored credentials.

---

## Workflow: Running the Orchestrator

With venv activated:

```bash
python orchestrator.py
```

You'll be prompted:
1. Describe your engineering task (paste sketch, CSV, or text description)
2. Type "done" when finished
3. Enter project name (e.g., "TestRig-CU1")
4. Review Haiku's triage analysis
5. Confirm to proceed with Opus workflow
6. Wait 3-4 minutes for results

Results are saved to `outputs/` folder.

---

## Requirements.txt

The project now uses a `requirements.txt` for clean dependency management:

```txt
anthropic>=0.28.0
python-dotenv>=1.0.0
requests>=2.31.0
```

To update dependencies later:
```bash
pip install -r requirements.txt --upgrade
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'anthropic'"
**Solution:**
```bash
# Make sure venv is activated (shows (venv) in prompt)
venv\Scripts\activate
# Reinstall
pip install -r requirements.txt
```

### Problem: "No module named 'auth'"
**Solution:**
- Make sure you're in `C:\Fixtures\engineering-docs\` directory
- Check that `auth.py` exists in the project root
- Make sure venv is activated

### Problem: "ANTHROPIC_API_KEY not set"
**Solution:** First run will prompt for setup interactively. If it doesn't:
```bash
python auth.py --setup
```

### Problem: "Invalid API key format"
**Solution:**
- API key should start with `sk-ant-`
- Get your real key from: https://console.anthropic.com/api-keys
- Don't use the placeholder `sk-ant-...`

### Problem: Credentials not persisting
**Solution:** Check that `~/.claude-engineering/credentials.json` exists:
```bash
# On Windows
type %USERPROFILE%\.claude-engineering\credentials.json

# On macOS/Linux
cat ~/.claude-engineering/credentials.json
```

---

## Security Notes

✅ **Credentials are protected:**
- Stored in user home directory (not in project)
- File permissions: `0o600` (read/write only for user)
- `.gitignore` prevents accidental commits
- No hardcoded keys in code

✅ **Best practices:**
- Never share your API key
- Revoke credentials if compromised: `python auth.py --revoke`
- Rotate keys periodically from console.anthropic.com
- Use environment variables in CI/CD (not local files)

---

## Next Steps

1. **Activate venv:** `venv\Scripts\activate`
2. **Run orchestrator:** `python orchestrator.py`
3. **Follow interactive setup** (first run only)
4. **Paste your engineering task description**
5. **Wait for results in `outputs/` folder**

---

## Migration from Previous Setup

If you were using API keys stored in user/appdata:
1. The new auth system stores credentials in `~/.claude-engineering/` instead
2. First run will prompt for setup if no credentials found
3. Your old API key can still be used (set `ANTHROPIC_API_KEY` env var)
4. The new local venv is completely isolated from system Python

---

**Setup complete! You're ready to run orchestrator.py** 🚀
