# Engineering Documentation Orchestrator

An AI-powered orchestrator for automating electrical wiring and block diagram documentation for fixtures engineering. Uses a tiered Claude model pipeline to cut costs while producing professional-grade outputs.

## What It Does

- Routes tasks through a **Haiku → Opus** pipeline (triage → engineering work), reducing cost ~70% vs. using Opus for everything
- Generates SVG schematics with IEC 60617 symbols, matplotlib block diagrams, connection tables, and block descriptions
- Assembles and saves professional PDFs to Google Drive via MCP connector
- Handles source document review, diagram generation, and documentation packaging end-to-end

## Project Structure

```
engineering-docs/
├── engineering-docs-orchestrator.py   # Main orchestrator script
├── wiring-block-diagrams/             # Engineering skill & references
│   ├── SKILL.md
│   └── references/
│       ├── conventions.md
│       ├── tools.md
│       └── assembly.md
├── scripts/                           # Diagram generation scripts
│   ├── fixture_diagrammer.py
│   ├── schematic_lib.py
│   └── schemdraw_example.py
├── docs/
│   └── WINDOWS_SETUP_GUIDE.md
├── MASTER.md                          # Full system instructions
├── WORKFLOW.md                        # Detailed example walkthrough
├── MCP-SETUP.md                       # Google Drive connector setup
├── MCP_QUICK_REFERENCE.md             # One-page cheat sheet
└── README_SETUP.md                    # Setup completion notes
```

## Quick Start

### Prerequisites

- Python 3.8+
- Anthropic API key (get one at https://console.anthropic.com/api-keys)

### Setup

```bash
# Windows PowerShell
cd C:\Fixtures\engineering-docs
.\venv\Scripts\Activate.ps1
python engineering-docs-orchestrator.py
```

```bash
# macOS/Linux
cd engineering-docs
source venv/bin/activate
python engineering-docs-orchestrator.py
```

On first run the script will prompt for your Anthropic API key (starts with `sk-ant-`), save it securely, and won't ask again.

### Authentication

Credentials are managed via `auth.py` — an OAuth-style credential manager that checks, in order:

1. `ANTHROPIC_API_KEY` environment variable
2. Local secure storage (`~/.claude-engineering/credentials.json`)
3. Interactive prompt on first run

No hardcoded keys; credentials are git-ignored.

## Google Drive Integration

See [MCP-SETUP.md](MCP-SETUP.md) for step-by-step instructions to connect the Google Drive MCP connector so generated PDFs are saved automatically.

## Documentation

| File | Purpose |
|------|---------|
| [MASTER.md](MASTER.md) | Full system instructions and deep-dive |
| [WORKFLOW.md](WORKFLOW.md) | Example execution walkthrough |
| [MCP-SETUP.md](MCP-SETUP.md) | Google Drive connector setup |
| [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) | One-page cheat sheet |
| [docs/WINDOWS_SETUP_GUIDE.md](docs/WINDOWS_SETUP_GUIDE.md) | Windows-specific setup |

## License

ISC
