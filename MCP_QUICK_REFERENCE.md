# MCP Quick Reference — One-Page Connector Setup

## What Is MCP?

**Model Context Protocol** = Claude's way to connect to external services (Google Drive, Gmail, Slack, etc.).

For your engineering workflow, you need **Google Drive MCP** to save outputs. The other MCPs are optional.

---

## Required: Google Drive MCP

### What It Does
- Creates folders in your Google Drive
- Uploads PDFs, CSVs, and other files
- Sets sharing permissions
- Organizes your engineering documentation

### URLs & Credentials

| Item | Value |
|------|-------|
| **MCP Server URL** | `https://drivemcp.googleapis.com/mcp/v1` |
| **Service** | Google Drive |
| **Auth Method** | OAuth 2.0 (browser-based login) |
| **Cost** | Free (uses your existing Google Drive) |

### Setup Steps (2 Minutes)

#### In Claude Code Desktop or Web:

1. **Open Claude Code.**
   - Desktop: `claude code` (terminal)
   - Web: https://claude.ai/code

2. **Click "Customize"** (sidebar, bottom-left or account menu).

3. **Click "Connectors".**

4. **Find "Google Drive"** in the list → Click **"Connect"**.

5. **A browser tab opens** → Google OAuth screen.
   - Sign in with the Google account that owns your Drive.
   - Click **"Allow"** to grant permissions.

6. **Back in Claude Code** → You should see **"Connected"** next to Google Drive.

✓ **Done!** Google Drive MCP is now active.

### Test It Works

In Claude Code, ask:
```
"Create a folder called test-engineering in my Google Drive."
```

Expected response:
```
✓ Folder created: test-engineering
Folder ID: 1a2b3c4d5e6f7g8h...
Link: https://drive.google.com/drive/folders/...
```

If this works, **MCP is connected and ready.**

---

## Optional: Gmail MCP (For Email Notifications)

### What It Does
- Sends completion notifications
- Drafts summary emails with Drive links

### Setup
Same as Google Drive:
1. **Customize → Connectors**
2. Find **Gmail** → Click **Connect**
3. Authorize

### Use in Orchestrator
```python
# After Phase 2 completes:
gmail_mcp.send_draft(
    to="team@example.com",
    subject=f"Engineering Doc Ready: {project_name}",
    body=f"See: {drive_folder_url}"
)
```

---

## Optional: Airtable MCP (For Database Storage)

### What It Does
- Persists connection tables in Airtable
- Creates searchable database of all diagrams

### URLs & Setup

| Item | Value |
|------|-------|
| **MCP Server URL** | `https://mcp.airtable.com/mcp` |
| **Website** | https://airtable.com |
| **Setup** | Customize → Connectors → Airtable → Connect |

### Use in Orchestrator
```python
# After Phase 2, save connection table:
airtable_mcp.create_records(
    base_id="app...",
    table_name="connections",
    records=[
        {"From": "AC Source", "To": "Motor", "Via": "K1 relay"},
        {"From": "RTD T1", "To": "DMM", "Via": "4-wire"},
        ...
    ]
)
```

---

## Optional: Google Calendar MCP (For Scheduling)

### What It Does
- Schedule documentation reviews
- Create calendar reminders for [VERIFY] items

### URLs & Setup

| Item | Value |
|------|-------|
| **MCP Server URL** | `https://calendarmcp.googleapis.com/mcp/v1` |
| **Setup** | Customize → Connectors → Google Calendar → Connect |

### Use in Orchestrator
```python
# After Phase 2, create calendar event:
calendar_mcp.create_event(
    title=f"Review Engineering Docs: {project_name}",
    description="Check [VERIFY] items with hardware team",
    start_time="2026-06-25T10:00:00",
    attendees=["hardware-lead@example.com"]
)
```

---

## How Orchestrator Uses MCPs

### Phase 1: Haiku Triage
No MCP needed. (Pure API call to Claude)

### Phase 2: Opus Engineering
No MCP needed. (Pure API call to Claude)

### Phase 3: Save to Google Drive
**Uses Google Drive MCP:**
```
1. Create folder: Engineering-{project}_{timestamp}
2. Upload PDF schematic
3. Upload connection table (CSV)
4. Upload block descriptions
5. Set sharing: "Anyone with link can view"
6. Return shareable Drive URL
```

### Optional: Send Email
**Uses Gmail MCP (if enabled):**
```
Send summary to team → "Docs ready at [Drive link]"
```

---

## Troubleshooting MCPs

### "MCP not connected"

**Check:**
1. Are you using **Claude Code** (not just chat)?
   - Desktop: `claude code`
   - Web: https://claude.ai/code
2. Go to **Customize → Connectors**.
3. Does Google Drive show **"Connected"** or **"Connect"**?

**Fix:**
- If it says **"Connect"**, click it and re-authorize.
- Make sure you're signed into the correct Google account.
- Try incognito mode for the OAuth flow.

### "Permission denied" when uploading

**Cause:** The Google account you authorized doesn't own the Drive.

**Fix:**
- Log out of all Google accounts.
- Log back in with the account that owns the Drive.
- Reconnect the MCP from Claude Code.

### "MCP timeout"

**Cause:** Large file uploads can be slow.

**Fix:**
- Increase timeout in `orchestrator.py`:
  ```python
  response = client.messages.create(
      timeout=600  # 10 minutes
  )
  ```

### "Folder already exists"

**Cause:** A folder with the same name already exists.

**Fix:**
- Delete the old folder in Google Drive, OR
- Use a different project name, OR
- Modify orchestrator.py to timestamp more granularly.

---

## Summary Table

| MCP | URL | Required? | Setup Time | Cost |
|-----|-----|-----------|-----------|------|
| **Google Drive** | `https://drivemcp.googleapis.com/mcp/v1` | ✓ YES | 2 min | Free |
| Gmail | `https://gmailmcp.googleapis.com/mcp/v1` | Optional | 2 min | Free |
| Google Calendar | `https://calendarmcp.googleapis.com/mcp/v1` | Optional | 2 min | Free |
| Airtable | `https://mcp.airtable.com/mcp` | Optional | 5 min | Free (Airtable account needed) |

---

## Quick Setup Checklist

```
[ ] Google Drive MCP
    [ ] Click Customize → Connectors
    [ ] Find Google Drive → Click Connect
    [ ] Authorize with browser
    [ ] See "Connected" status
    [ ] Test: "Create a folder in my Drive"

[ ] (Optional) Gmail MCP
    [ ] Same as Google Drive
    [ ] Test: "Draft an email to me"

[ ] (Optional) Google Calendar MCP
    [ ] Same as Google Drive
    [ ] Test: "Create a calendar event"

[ ] (Optional) Airtable MCP
    [ ] Same as Google Drive
    [ ] Create Airtable account & base first
    [ ] Test: "Create a record in Airtable"
```

---

## Real-World Example

### You run:
```bash
python orchestrator.py
# Task: GCF motor control schematic
# Project: GCF-TestRig-Rev2
```

### What happens:

1. **Haiku triage** (no MCP)
   ```
   ✓ Tool: schemdraw
   ✓ Standard: IEC 60617
   ✓ Complexity: medium
   ```

2. **Opus engineering** (no MCP)
   ```
   ✓ Connection table built
   ✓ Schematic drafted
   ✓ PDF assembled
   ```

3. **Google Drive save** (uses Google Drive MCP)
   ```
   ✓ Create folder: Engineering-GCF-TestRig-Rev2_2026-06-24_14-35-22
   ✓ Upload PDF
   ✓ Upload CSV
   ✓ Set sharing
   ✓ Return link: https://drive.google.com/drive/folders/1a2b...
   ```

4. **(Optional) Send email** (uses Gmail MCP)
   ```
   ✓ Email sent: "Docs ready at [link]"
   ```

**Total time:** ~4 minutes | **Cost:** ~$0.15 | **Result:** Professional PDF + Drive folder

---

## More Help

- **Full MCP Setup Guide:** See `MCP-SETUP.md`
- **Troubleshooting:** See `MCP-SETUP.md` → Troubleshooting section
- **Anthropic Docs:** https://modelcontextprotocol.io
- **Google Drive API:** https://developers.google.com/drive/api

---

**TL;DR:** Enable Google Drive MCP (Customize → Connectors → Google Drive → Connect), then run `python orchestrator.py`. Done!
