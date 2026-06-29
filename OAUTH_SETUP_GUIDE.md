# 🔐 OAuth Authentication Guide

## Overview

The engineering documentation orchestrator now supports **OAuth-based authentication** using your Claude subscription. This is the recommended method for secure, browser-based sign-in.

---

## What is OAuth?

OAuth is a secure authentication standard that allows you to:
- Sign in with your Claude subscription account
- Keep your credentials private (never typed into scripts)
- Browser-based authentication (more secure)
- Easy revocation if needed

---

## Authentication Methods (In Priority Order)

### 1️⃣ **OAuth via Browser** (Recommended)
- Sign in with Claude subscription
- Browser-based authentication
- Most secure
- Automatic credential handling

### 2️⃣ **Environment Variable**
- Set `ANTHROPIC_API_KEY` environment variable
- Useful for CI/CD, automated scripts
- Override local credentials

### 3️⃣ **Local Credentials File**
- Stored in `~/.claude-engineering/credentials.json`
- Restricted file permissions (0o600)
- Persistent across sessions
- Git-ignored (never committed)

### 4️⃣ **API Key (Fallback)**
- Manual entry from console.anthropic.com
- For users who prefer not to use browser-based auth
- Same security as OAuth method

---

## Quick Start with OAuth

### Step 1: Activate Virtual Environment
```bash
cd C:\Fixtures\engineering-docs
venv\Scripts\activate
```

### Step 2: Run Orchestrator (First Time)
```bash
python orchestrator.py
```

### Step 3: Choose OAuth
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

### Step 4: Browser Opens
- Automatically opens: https://console.anthropic.com/api-keys
- Browser windows appears for authentication

### Step 5: Sign In with Claude Subscription
1. If not already signed in, enter your email/password
2. Complete any 2FA (if enabled)
3. You're signed into console.anthropic.com

### Step 6: Create or Copy API Key
1. You should see "API Keys" section
2. Look for existing keys or click "Create Key"
3. Copy the API key (starts with `sk-ant-`)

### Step 7: Return to Script and Paste
```
Waiting for API key...
---
Paste your API key from console.anthropic.com: [paste here]
✓ OAuth authentication successful!
✓ API key saved to local credentials file
```

### Step 8: Orchestrator Starts
Script continues automatically with your first engineering task.

---

## Subsequent Runs (No Re-Authentication)

```bash
python orchestrator.py
```

Credentials are loaded automatically from `~/.claude-engineering/credentials.json`. No authentication needed.

---

## Manual OAuth Setup

To re-run OAuth setup without orchestrator:

```bash
python auth.py --setup
```

Then choose:
```
  Option 1: OAuth (Recommended)
  Option 2: API Key
```

---

## Check Authentication Status

```bash
python auth.py --status
```

Output:
```
Authentication Status:
  env_var_set: False
  local_creds_exist: True
  api_key_loaded: True
  config_dir: C:\Users\YourUsername\.claude-engineering
```

---

## Using Environment Variable (Override)

If you prefer to use environment variable instead of stored credentials:

### Windows CMD
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
python orchestrator.py
```

### Windows PowerShell
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
python orchestrator.py
```

### macOS/Linux
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python orchestrator.py
```

**Priority:** Environment variable takes precedence over stored credentials.

---

## Security Features

✅ **Browser-Based Authentication**
- No credentials typed into script
- Uses your browser's secure session
- More secure than copy-pasting keys

✅ **Local Credential Storage**
- Stored in home directory (not in project)
- File permissions: 0o600 (owner read/write only)
- Never committed to git
- User-only access

✅ **Credential Revocation**
- Easily remove credentials: `python auth.py --revoke`
- Supports rotating keys
- Security-first approach

✅ **Environment Variable Override**
- Useful for CI/CD pipelines
- CI systems can pass keys securely
- Project never stores production keys

---

## Troubleshooting OAuth

### Problem: Browser doesn't open automatically

**Solution 1: Manual Browser Navigation**
```
Script will show:
  ⚠ Could not open browser: [error]
  Please open manually: https://console.anthropic.com/api-keys

Just open the URL in your browser and continue.
```

**Solution 2: Check System Browser**
- Make sure you have a default browser set
- Try: `python auth.py --setup` (more verbose)

### Problem: "Invalid API key format"

The key must start with `sk-ant-`

**Solution:**
1. Go to console.anthropic.com/api-keys
2. Sign in with your Claude subscription
3. Copy the FULL API key
4. Don't modify it
5. Paste exactly as shown

### Problem: OAuth signin says "Account not found"

**Solution:**
- Verify you're using the correct email for Claude subscription
- Go to: https://console.anthropic.com/ (main dashboard)
- Verify you're logged in
- Navigate to: API Keys section

### Problem: Can't find API Keys section

**Solution:**
1. Go to: https://console.anthropic.com/
2. Look for "API Keys" in the left sidebar
3. Or visit directly: https://console.anthropic.com/api-keys
4. If not logged in, sign in with Claude subscription
5. API Keys section appears after login

### Problem: "Connection refused" or network error

**Solution:**
- Check internet connection
- Verify console.anthropic.com is accessible
- Try again: `python auth.py --setup`
- Try API Key method (Option 2) as fallback

### Problem: Already signed in, but still prompted to login

**Solution:**
- Browser cache issue
- Try: Incognito/Private browsing mode
- Or manually navigate to: https://console.anthropic.com/api-keys
- Or clear browser cookies for console.anthropic.com

---

## Relationship: Claude Subscription → API Key

You have a Claude subscription. Here's how it connects:

```
Claude Subscription Account
    ↓
    └→ console.anthropic.com (web portal)
           ↓
           └→ API Keys section
                  ↓
                  └→ Create/View API Keys (sk-ant-...)
                         ↓
                         └→ Use in orchestrator.py
```

**Key Points:**
- Your subscription account IS your authentication
- API keys are generated from your subscription account
- Multiple API keys can exist under one subscription
- Each key can be individually revoked
- Keys inherit your subscription's usage limits

---

## API Key Lifecycle

### Create
```
1. Go to console.anthropic.com/api-keys
2. Click "Create Key"
3. Choose name and permissions
4. Copy the key (shown only once)
```

### Use
```
1. Paste in orchestrator setup
2. Script saves locally
3. Used for API calls
```

### Monitor
```
1. Check console.anthropic.com for usage
2. See which keys are active
3. Monitor usage metrics
```

### Rotate (Security)
```
1. Create new key in console
2. Run: python auth.py --setup (enter new key)
3. Delete old key from console
```

### Revoke (Emergency)
```
1. Revoke key in console.anthropic.com
2. Or: python auth.py --revoke (local only)
3. Create new key
4. Re-authenticate
```

---

## Best Practices

✅ **DO:**
- Use OAuth method (Option 1) for first-time setup
- Keep your Claude subscription password secure
- Rotate API keys periodically
- Revoke keys if compromised
- Use environment variables for CI/CD
- Check console.anthropic.com for suspicious usage

❌ **DON'T:**
- Share your API key with others
- Commit API keys to version control
- Use the same key across projects
- Leave keys active if not needed
- Enable debug mode in production
- Log API keys to files

---

## Environment Variable for CI/CD

In automated environments (GitHub Actions, etc.):

```yaml
# Example: GitHub Actions
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

# In shell
python orchestrator.py
```

**Best Practices for CI/CD:**
1. Store API key in CI/CD secrets manager
2. Never hardcode in repository
3. Rotate keys regularly
4. Use separate key for CI/CD (not production)
5. Monitor usage for anomalies

---

## Help & Support

### Get Help
```bash
python auth.py --help
```

### Check Status
```bash
python auth.py --status
```

### Manual Setup
```bash
python auth.py --setup
```

### Clear Credentials
```bash
python auth.py --revoke
```

---

## Links

- **Claude Console:** https://console.anthropic.com/
- **API Keys Page:** https://console.anthropic.com/api-keys
- **Anthropic Docs:** https://docs.anthropic.com
- **Claude Subscription:** https://claude.ai/

---

## Summary

✅ **OAuth is the recommended method**
- Browser-based authentication
- Uses your Claude subscription
- Most secure approach
- Easiest setup experience

✅ **Automatic credential handling**
- Saved locally after first run
- No re-entry needed
- Easy to revoke or rotate

✅ **Multiple options available**
- OAuth (recommended)
- API Key (fallback)
- Environment variable (CI/CD)
- Local storage (persistent)

**First run with OAuth:**
```bash
python orchestrator.py
# Choose Option 1
# Browser opens
# Sign in + copy key
# Done!
```

---

*Last updated: 2026-06-28*
