# Google Drive MCP Setup for Claude Code

This guide shows how to connect Google Drive to Claude Code so the orchestrator can automatically create project folders and save engineering documentation.

## What is MCP?

**Model Context Protocol (MCP)** is a standard that lets Claude connect to external services. Google Drive MCP lets Claude:
- List files and folders
- Create new folders
- Upload files (PDFs, CSVs, images)
- Set sharing permissions
- Manage folder structure

---

## Setup Steps

### Step 1: Open Claude Code

Launch Claude Code from the terminal:
```bash
claude code
```

Or from the web: https://claude.ai (if using Claude Code web version).

### Step 2: Access Connectors

In the Claude Code interface:

**Desktop / Web:**
1. Click **Customize** (usually bottom-left sidebar, or account menu).
2. Click **Connectors**.
3. You should see a list of available connectors.

**Screenshot hint:** You'll see connectors like Gmail, Google Calendar, Google Drive, Airtable, etc. listed with "Connect" buttons.

### Step 3: Find and Enable Google Drive

1. In the Connectors list, find **Google Drive**.
2. Click the **Connect** button next to it.
3. A browser tab will open to Google's OAuth consent screen.

### Step 4: Authorize Claude Code

On the Google OAuth screen:

1. **Sign in** with the Google account that owns the Drive folder where you want to save documentation.
2. **Review permissions:**
   - "See, edit, create, and delete all your Google Drive files"
   - "Manage Google Drive folder and file sharing for those files and folders created by Claude"
3. Click **Allow** (or **Continue**).
4. The browser redirects back to Claude Code. You should see a **"Connected"** status next to Google Drive.

**Screenshot hint:** A green checkmark or "Connected" label appears next to Google Drive in the Connectors list.

### Step 5: Verify the Connection

In Claude Code, test the connection by asking:

```
"Create a folder called 'test-engineering-docs' in my Google Drive."
```

Claude Code should:
1. Use the Google Drive MCP to create the folder.
2. Return the folder ID or shareable link.
3. Show "✓ Folder created" or similar confirmation.

If you see an error like `"Permission denied"` or `"Google Drive not connected"`, repeat Step 4.

---

## Using Google Drive MCP in the Orchestrator

Once connected, the orchestrator script can use Google Drive MCP automatically.

### In Phase 3 (Save to Drive)

The orchestrator will:

```python
# Pseudocode (happens automatically)
folder_name = f"Engineering-{project_name}_{timestamp}"

# MCP call: Create folder
drive_mcp.create_folder(
    name=folder_name,
    parent_folder_id=None  # Creates in root; set parent_folder_id to nest it
)

# MCP call: Upload PDF
drive_mcp.upload_file(
    file_path="output.pdf",
    folder_id=folder_id,
    name=f"{project_name}_Schematic.pdf"
)

# MCP call: Upload connection table CSV
drive_mcp.upload_file(
    file_path="connections.csv",
    folder_id=folder_id,
    name=f"{project_name}_ConnectionTable.csv"
)

# MCP call: Set sharing (optional)
drive_mcp.share_folder(
    folder_id=folder_id,
    email="team-member@example.com",
    role="editor"
)
```

### Configuration (Optional)

If you want to specify a **parent folder** for all engineering documentation projects, edit `orchestrator.py`:

```python
# In orchestrator.py, around line 150:
GOOGLE_DRIVE_PARENT_FOLDER = os.getenv("GOOGLE_DRIVE_PARENT_FOLDER_ID", None)

# Then in phase_3_save_to_drive():
folder = drive_mcp.create_folder(
    name=folder_name,
    parent_folder_id=GOOGLE_DRIVE_PARENT_FOLDER
)
```

Then set the environment variable:

```bash
export GOOGLE_DRIVE_PARENT_FOLDER_ID="1a2b3c4d5e6f7g8h..."
```

(Get the folder ID from a Google Drive URL: `https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h/` → the ID is the long string.)

---

## MCP Connector URLs

For reference, here are the MCP server URLs used:

| Service | URL | Used For |
|---------|-----|----------|
| **Google Drive** | `https://drivemcp.googleapis.com/mcp/v1` | Create folders, upload files, set permissions |
| Google Calendar | `https://calendarmcp.googleapis.com/mcp/v1` | (Optional) Schedule documentation reviews |
| Gmail | `https://gmailmcp.googleapis.com/mcp/v1` | (Optional) Email completion notifications |
| Airtable | `https://mcp.airtable.com/mcp` | (Optional) Store connection tables as database |

**You only need Google Drive.** Calendar, Gmail, and Airtable are optional for extended workflows.

---

## Troubleshooting

### Error: "Google Drive MCP not connected"

**Solution:**
1. Go to **Customize → Connectors**.
2. Check if Google Drive shows **"Connected"** or **"Connect"**.
3. If it says **"Connect"**, click it and re-authorize.
4. If still failing, try:
   - Clear browser cache.
   - Log out of all Google accounts, then log back in with the correct account.
   - Use Incognito mode for the OAuth flow.

### Error: "Permission denied" when uploading

**Solution:**
- The Google account you authorized may not own the Drive folder.
- Go to `https://drive.google.com` and check that you're logged into the correct account.
- Reconnect the MCP using that account.

### Error: "Folder already exists"

**Solution:**
- The orchestrator tries to create `Engineering-{project_name}_{timestamp}`.
- If a folder with that exact name exists, you'll see this error.
- Either delete the old folder or use a different project name.

### Claude Code says "MCP not available"

**Solution:**
- Ensure you're using Claude Code (not just claude.ai chat).
- MCP connectors only work in Claude Code (desktop app or claude.ai/code).
- If using claude.ai chat, connectors have limited support; upgrade to Claude Code for full MCP.

---

## Advanced: Custom MCP Servers

If you want to **host your own Google Drive MCP server** (for fine-grained permission control or on-premise usage):

1. Clone the Anthropic MCP server repo:
   ```bash
   git clone https://github.com/anthropics/mcp-servers.git
   cd mcp-servers/src/gdrive
   ```

2. Install and configure:
   ```bash
   npm install
   # Set up OAuth credentials (see README in gdrive folder)
   node index.js
   ```

3. In Claude Code, configure a custom MCP connector pointing to your server.

This is advanced and usually not necessary; the official Google Drive MCP (via Customize → Connectors) is the easiest path.

---

## Summary

After following these steps:

✓ Google Drive MCP is enabled  
✓ Claude Code can create folders  
✓ Claude Code can upload files  
✓ The orchestrator can save outputs automatically  

**Next:** Run `python orchestrator.py` and test with a small engineering task. You should see a new folder in Google Drive after the workflow completes.

---

**More Help:**
- Google Drive MCP Docs: https://github.com/anthropics/mcp-servers
- Claude Code Docs: https://docs.claude.com/en/docs/claude-code/overview
- Anthropic MCP Docs: https://modelcontextprotocol.io/introduction
