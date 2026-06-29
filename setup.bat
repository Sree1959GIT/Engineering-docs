@echo off
REM ============================================================================
REM Windows Setup Script for Engineering Documentation Orchestrator
REM Run this in: C:\Fixtures\engineering-docs\
REM ============================================================================

echo.
echo ============================================================================
echo Creating folder structure in C:\Fixtures\engineering-docs\
echo ============================================================================
echo.

REM Create subfolders
mkdir docs
mkdir scripts
mkdir outputs

echo ✓ Created folders: docs, scripts, outputs
echo.

REM Verify structure
echo ============================================================================
echo Folder structure created:
echo ============================================================================
tree /A
echo.

REM Next steps
echo ============================================================================
echo NEXT STEPS:
echo ============================================================================
echo.
echo 1. Download all files from: /mnt/user-data/outputs/
echo.
echo 2. Copy files to these locations:
echo.
echo    MAIN FOLDER (C:\Fixtures\engineering-docs\):
echo      - orchestrator.py
echo      - wiring-block-diagrams.skill
echo      - .env.example
echo      - START_HERE.md
echo.
echo    DOCS FOLDER (C:\Fixtures\engineering-docs\docs\):
echo      - README.md
echo      - MASTER.md
echo      - WORKFLOW.md
echo      - MCP-SETUP.md
echo      - MCP_QUICK_REFERENCE.md
echo      - FILES_CHECKLIST.md
echo      - FOLDER_STRUCTURE.md
echo      - DELIVERY_SUMMARY.txt
echo      - FINAL_SUMMARY.txt
echo      - QUICK_SETUP_COMMANDS.txt
echo.
echo 3. Create .env file:
echo    - Copy .env.example to .env
echo    - Edit .env and paste your ANTHROPIC_API_KEY
echo.
echo 4. Install Python dependencies:
echo    - Open Command Prompt in C:\Fixtures\engineering-docs\
echo    - Run: pip install anthropic python-dotenv
echo.
echo 5. Enable Google Drive MCP in Claude Code
echo.
echo 6. Open Claude Code:
echo    - Run: claude code
echo.
echo 7. Test your setup:
echo    - Run: python orchestrator.py
echo.
echo ============================================================================
echo Setup ready! Follow the steps above.
echo ============================================================================
echo.
pause
