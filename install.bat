@echo off
REM ============================================================================
REM AUTOMATED WINDOWS INSTALLATION SCRIPT
REM Run this in: C:\Fixtures\engineering-docs\
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo Engineering Documentation Orchestrator - Windows Setup
echo ============================================================================
echo.

REM Check if we're in the right folder
if not exist "setup.bat" (
    echo ERROR: This script must be run from C:\Fixtures\engineering-docs\
    echo.
    echo Please:
    echo 1. Download this script to C:\Fixtures\engineering-docs\
    echo 2. Open Command Prompt
    echo 3. Run: cd C:\Fixtures\engineering-docs
    echo 4. Run: install.bat
    echo.
    pause
    exit /b 1
)

REM ============================================================================
REM STEP 1: Create Folder Structure
REM ============================================================================

echo Step 1: Creating folder structure...
if not exist "docs" mkdir docs
if not exist "scripts" mkdir scripts
if not exist "outputs" mkdir outputs
echo ✓ Folders created: docs\, scripts\, outputs\
echo.

REM ============================================================================
REM STEP 2: Get Downloads Folder Path
REM ============================================================================

echo Step 2: Locating Downloads folder...
set DOWNLOADS=%USERPROFILE%\Downloads

if not exist "%DOWNLOADS%" (
    echo ERROR: Could not find Downloads folder at: %DOWNLOADS%
    echo.
    echo Please download all files manually from /mnt/user-data/outputs/
    echo and place them in: C:\Fixtures\engineering-docs\
    echo.
    pause
    exit /b 1
)

echo ✓ Found: %DOWNLOADS%
echo.

REM ============================================================================
REM STEP 3: Verify All Files Exist
REM ============================================================================

echo Step 3: Checking for required files...

set MISSING=0
for %%F in (
    orchestrator.py
    wiring-block-diagrams.skill
    .env.example
    START_HERE.md
    README.md
    MASTER.md
    WORKFLOW.md
    MCP-SETUP.md
    MCP_QUICK_REFERENCE.md
    FILES_CHECKLIST.md
    FOLDER_STRUCTURE.md
    DELIVERY_SUMMARY.txt
    FINAL_SUMMARY.txt
    QUICK_SETUP_COMMANDS.txt
) do (
    if not exist "%DOWNLOADS%\%%F" (
        echo ✗ Missing: %%F
        set MISSING=1
    ) else (
        echo ✓ Found: %%F
    )
)

if !MISSING! equ 1 (
    echo.
    echo WARNING: Some files are missing from Downloads!
    echo Please download them from: /mnt/user-data/outputs/
    echo.
    pause
    exit /b 1
)

echo ✓ All files found!
echo.

REM ============================================================================
REM STEP 4: Copy Files
REM ============================================================================

echo Step 4: Copying files to project folder...
echo.

REM Copy main folder files
echo Copying to main folder...
copy "%DOWNLOADS%\orchestrator.py" . >nul 2>&1
copy "%DOWNLOADS%\wiring-block-diagrams.skill" . >nul 2>&1
copy "%DOWNLOADS%\.env.example" . >nul 2>&1
copy "%DOWNLOADS%\START_HERE.md" . >nul 2>&1
copy "%DOWNLOADS%\README.md" . >nul 2>&1
copy "%DOWNLOADS%\MASTER.md" . >nul 2>&1
copy "%DOWNLOADS%\WORKFLOW.md" . >nul 2>&1
copy "%DOWNLOADS%\MCP-SETUP.md" . >nul 2>&1
copy "%DOWNLOADS%\MCP_QUICK_REFERENCE.md" . >nul 2>&1
copy "%DOWNLOADS%\FILES_CHECKLIST.md" . >nul 2>&1
copy "%DOWNLOADS%\FOLDER_STRUCTURE.md" . >nul 2>&1
echo ✓ Main folder files copied

REM Copy docs folder files
echo Copying to docs\ folder...
copy "%DOWNLOADS%\DELIVERY_SUMMARY.txt" docs\ >nul 2>&1
copy "%DOWNLOADS%\FINAL_SUMMARY.txt" docs\ >nul 2>&1
copy "%DOWNLOADS%\QUICK_SETUP_COMMANDS.txt" docs\ >nul 2>&1
echo ✓ Docs folder files copied
echo.

REM ============================================================================
REM STEP 5: Create .env File
REM ============================================================================

echo Step 5: Creating .env file...
if exist ".env" (
    echo ⚠ Warning: .env already exists (not overwriting)
) else (
    copy ".env.example" ".env" >nul
    echo ✓ Created .env from .env.example
)
echo.

REM ============================================================================
REM STEP 6: Display Next Steps
REM ============================================================================

echo ============================================================================
echo ✓ SETUP COMPLETE!
echo ============================================================================
echo.
echo Your folder structure is now ready:
echo C:\Fixtures\engineering-docs\
echo ├── orchestrator.py
echo ├── wiring-block-diagrams.skill
echo ├── .env
echo ├── START_HERE.md
echo ├── docs\
echo ├── scripts\
echo └── outputs\
echo.

REM ============================================================================
REM STEP 7: Install Python Dependencies
REM ============================================================================

echo Step 7: Installing Python dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ⚠ WARNING: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo During installation, CHECK: "Add Python to PATH"
    echo.
    echo Then run: pip install anthropic python-dotenv
    echo.
) else (
    echo ✓ Python found
    echo Installing packages: anthropic, python-dotenv
    pip install anthropic python-dotenv
    echo ✓ Packages installed
)
echo.

REM ============================================================================
REM FINAL INSTRUCTIONS
REM ============================================================================

echo ============================================================================
echo NEXT STEPS:
echo ============================================================================
echo.
echo 1. EDIT YOUR API KEY:
echo    - Open .env in Notepad
echo    - Replace "sk-ant-..." with your ACTUAL API key
echo    - Get key from: https://console.anthropic.com/api-keys
echo    - Save the file
echo.
echo 2. ENABLE GOOGLE DRIVE MCP:
echo    - Open Claude Code
echo    - Click Customize → Connectors
echo    - Find Google Drive → Click Connect
echo    - Authorize with your Google account
echo.
echo 3. RUN YOUR FIRST TASK:
echo    - Open Command Prompt
echo    - Run: cd C:\Fixtures\engineering-docs
echo    - Run: python orchestrator.py
echo    - Paste your engineering task description
echo.
echo 4. CHECK YOUR RESULTS:
echo    - Open Google Drive
echo    - Find folder: Engineering-{project}_{timestamp}
echo    - Download PDF schematic and tables
echo.
echo ============================================================================
echo For detailed instructions, read: docs\WINDOWS_SETUP_GUIDE.md
echo For quick reference, read: START_HERE.md
echo ============================================================================
echo.

pause
