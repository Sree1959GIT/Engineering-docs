#!/usr/bin/env python3
"""
orchestrator.py — Multi-model engineering documentation workflow for Claude Code.

Route: User input → Haiku 4.5 (scope + tool decision) → Opus 4.8 (full engineering work)
Saves outputs to Google Drive (MCP) in a project-specific folder.

Install: pip install anthropic google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
Usage: python orchestrator.py
"""

import os
import json
import sys
from typing import Optional
from datetime import datetime
import anthropic

# ============================================================================
# CONFIGURATION
# ============================================================================

HAIKU_MODEL = "claude-haiku-4-5-20251001"
OPUS_MODEL = "claude-opus-4-8"
API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not API_KEY:
    print("Error: ANTHROPIC_API_KEY environment variable not set.")
    sys.exit(1)

client = anthropic.Anthropic(api_key=API_KEY)

HAIKU_SYSTEM = """You are an engineering triage specialist. Your job is to:
1. Understand the user's wiring/block diagram task.
2. Identify what standard they need (IEC 60617, ANSI, house style).
3. List what reference documents or inputs are required.
4. Suggest the best drawing tool/approach (schemdraw, SVG, matplotlib, QElectroTech, etc.).
5. Estimate scope and complexity (quick sketch vs. manufacturing-grade).

Be concise and structured. Output as JSON with keys:
  - task_type (schematic, block_diagram, layout, other)
  - standard (IEC, ANSI, custom, etc.)
  - required_inputs (list of items to gather)
  - recommended_tool (schemdraw, svg_custom, matplotlib, qelectrotech, kicad, etc.)
  - complexity (low, medium, high)
  - questions_for_user (list of clarifications needed)
  - estimated_time_hours (rough estimate)
"""

OPUS_SYSTEM = """You are an expert hardware engineer and technical documentarian.
You have access to a skill called 'wiring-block-diagrams' that knows:
  - SVG/schemdraw/matplotlib for drawing electrical schematics and block diagrams
  - Connection table building from raw inputs
  - Professional documentation assembly with to-scale diagrams
  - Symbol conventions (IEC 60617, relay blocks, terminal symbols, etc.)
  - Adversarial source review (flag ambiguities with [VERIFY], don't guess)

Your workflow:
1. Build a connection table (From → Via → To → Notes) from user inputs.
2. Adversarially review against the source for misreads, missing components, invented details.
3. Mark uncertain readings with [VERIFY] and confirm with user.
4. Draft the diagrams using the appropriate tool.
5. Assemble the final PDF/docx with block descriptions and tables.
6. Save to Google Drive (via MCP) in the project folder.

Be meticulous about accuracy. Never invent data. Use the skill.
"""

# ============================================================================
# PHASE 1: HAIKU TRIAGE
# ============================================================================

def phase_1_haiku_triage(user_description: str) -> dict:
    """
    Use Haiku 4.5 to scope the task, identify tool needs, and gather requirements.
    Returns a structured decision object.
    """
    print("\n" + "=" * 70)
    print("PHASE 1: Triaging with Haiku 4.5 (tool selection & requirements)")
    print("=" * 70)
    
    try:
        response = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=1500,
            system=HAIKU_SYSTEM,
            messages=[
                {"role": "user", "content": user_description}
            ]
        )
        
        response_text = response.content[0].text
        print(f"\n[Haiku Response]\n{response_text}\n")
        
        # Attempt to extract JSON from Haiku's response
        try:
            # Find JSON block in response
            if "{" in response_text and "}" in response_text:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                json_str = response_text[start:end]
                triage_result = json.loads(json_str)
            else:
                # Fallback: return response as text
                triage_result = {"raw_response": response_text}
        except json.JSONDecodeError:
            triage_result = {"raw_response": response_text}
        
        return triage_result
    
    except anthropic.APIError as e:
        print(f"Haiku API error: {e}")
        return {"error": str(e)}

# ============================================================================
# PHASE 2: OPUS ENGINEERING WORKFLOW
# ============================================================================

def phase_2_opus_engineering(user_description: str, triage_context: dict) -> dict:
    """
    Use Opus 4.8 to execute the full engineering documentation workflow.
    Receives context from Haiku and produces final diagrams + tables.
    """
    print("\n" + "=" * 70)
    print("PHASE 2: Full Engineering Workflow with Opus 4.8")
    print("=" * 70)
    
    # Build a context-aware prompt that incorporates Haiku's triage
    opus_prompt = f"""
User's task:
{user_description}

Triage results from initial analysis:
{json.dumps(triage_context, indent=2)}

Now execute the full engineering documentation workflow:
1. Build a connection table from the provided inputs (sketch, CSV, description).
2. Adversarially review it for errors, omissions, and invented details.
3. Mark all uncertain readings as [VERIFY] and list them for confirmation.
4. Once confirmed, draft the diagrams using the best tool.
5. Describe each block / subsystem.
6. Assemble the final documentation.
7. Save outputs to Google Drive in a project-specific folder.

Use the wiring-block-diagrams skill. Be meticulous and never guess.
"""
    
    try:
        response = client.messages.create(
            model=OPUS_MODEL,
            max_tokens=4000,
            system=OPUS_SYSTEM,
            messages=[
                {"role": "user", "content": opus_prompt}
            ]
        )
        
        response_text = response.content[0].text
        print(f"\n[Opus Response (truncated)]\n{response_text[:2000]}...\n")
        
        return {
            "status": "success",
            "response": response_text,
            "model": OPUS_MODEL
        }
    
    except anthropic.APIError as e:
        print(f"Opus API error: {e}")
        return {"status": "error", "error": str(e)}

# ============================================================================
# PHASE 3: SAVE TO GOOGLE DRIVE (MCP)
# ============================================================================

def phase_3_save_to_drive(project_name: str, outputs: dict) -> dict:
    """
    Save the engineering documentation outputs to Google Drive.
    Uses the Google Drive MCP connector (assumed to be enabled in Claude Code).
    
    For now, returns instructions. In Claude Code, use:
      from anthropic.mcp import drive
    """
    print("\n" + "=" * 70)
    print("PHASE 3: Saving to Google Drive (via MCP)")
    print("=" * 70)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"Engineering-{project_name}_{timestamp}"
    
    print(f"\nTo complete this step in Claude Code:")
    print(f"1. Enable Google Drive MCP connector in Customize → Connectors")
    print(f"2. Create folder: {folder_name}")
    print(f"3. Upload generated PDFs, connection tables, and diagrams")
    print(f"\nAlternatively, this script would use the Google Drive MCP to automate:")
    print(f"   - Create folder '{folder_name}'")
    print(f"   - Upload all output files")
    print(f"   - Return shareable links")
    
    return {
        "status": "manual_step",
        "folder_name": folder_name,
        "note": "Use Claude Code's Google Drive MCP connector to complete this step."
    }

# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

def main():
    print("\n" + "=" * 70)
    print("ENGINEERING DOCUMENTATION ORCHESTRATOR (Haiku → Opus → Drive)")
    print("=" * 70)
    
    # Get user input
    print("\n[Step 1] Describe your engineering task:")
    print("(Paste sketch description, CSV path, or wiring requirements)")
    print("---")
    
    user_input_lines = []
    try:
        while True:
            line = input()
            if line.strip().lower() == "done":
                break
            user_input_lines.append(line)
    except EOFError:
        # Handle non-interactive mode
        user_input_lines = sys.stdin.readlines()
    
    user_description = "\n".join(user_input_lines).strip()
    if not user_description:
        print("No input provided. Exiting.")
        sys.exit(0)
    
    # Ask for project name
    project_name = input("\n[Step 2] Project name (e.g., 'TestRig-CU1'): ").strip()
    if not project_name:
        project_name = "Engineering-Doc"
    
    # Phase 1: Haiku triage
    triage = phase_1_haiku_triage(user_description)
    
    # Ask user if they want to proceed based on Haiku's analysis
    print("\n" + "-" * 70)
    proceed = input("Proceed with Opus engineering workflow? (yes/no): ").strip().lower()
    if proceed not in ("yes", "y"):
        print("Workflow cancelled.")
        sys.exit(0)
    
    # Phase 2: Opus engineering work
    opus_result = phase_2_opus_engineering(user_description, triage)
    
    if opus_result.get("status") == "success":
        print("\n✓ Opus engineering workflow completed.")
        
        # Phase 3: Save to Drive
        drive_result = phase_3_save_to_drive(project_name, opus_result)
        print(f"\n✓ Output folder: {drive_result['folder_name']}")
        
        # Summary
        print("\n" + "=" * 70)
        print("WORKFLOW SUMMARY")
        print("=" * 70)
        print(f"Task: {user_description[:100]}...")
        print(f"Project: {project_name}")
        print(f"Haiku decision: {triage.get('recommended_tool', 'N/A')}")
        print(f"Opus status: {opus_result['status']}")
        print(f"Drive folder: {drive_result['folder_name']}")
        print("=" * 70)
    else:
        print(f"\n✗ Opus workflow failed: {opus_result.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
