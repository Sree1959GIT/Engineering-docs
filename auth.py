#!/usr/bin/env python3
"""
auth.py — Authentication check for orchestrator.py.

Uses the Claude Code OAuth session that is already active.
No API key required — authentication is handled by `claude` CLI.
"""

import sys
import subprocess


def verify_claude_auth() -> None:
    """
    Verify that the `claude` CLI is available and authenticated.
    Exits with a clear message if not.
    """
    try:
        result = subprocess.run(
            ["claude", "-p", "ping", "--output-format", "text"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            return  # Authenticated and working
        # CLI ran but returned an error — likely not logged in
        print("\n" + "=" * 70)
        print("AUTHENTICATION ERROR")
        print("=" * 70)
        print("\nClaude CLI is installed but not authenticated.")
        print("\nFix: Open the Claude Code desktop app and sign in with your")
        print("Claude subscription. Then re-run this script.\n")
        print(f"Details: {result.stderr.strip()}")
        print("=" * 70 + "\n")
        sys.exit(1)

    except FileNotFoundError:
        print("\n" + "=" * 70)
        print("CLAUDE CLI NOT FOUND")
        print("=" * 70)
        print("\nThe `claude` CLI is not installed or not on your PATH.")
        print("\nFix: Install Claude Code from https://claude.ai/code")
        print("     Then sign in with your Claude subscription.")
        print("=" * 70 + "\n")
        sys.exit(1)

    except subprocess.TimeoutExpired:
        print("\n⚠ Authentication check timed out. Check your internet connection.")
        sys.exit(1)


if __name__ == "__main__":
    if "--status" in sys.argv:
        try:
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True, text=True, timeout=10
            )
            print("\nAuthentication Status:")
            print(f"  claude CLI:    {'found' if result.returncode == 0 else 'not found'}")
            print(f"  version:       {result.stdout.strip()}")
            print(f"  auth method:   Claude Code OAuth (subscription)")
            print(f"  API key needed: No\n")
        except FileNotFoundError:
            print("\nStatus: claude CLI not found. Install Claude Code.\n")
    else:
        verify_claude_auth()
        print("\n✓ Claude Code OAuth authentication is active.\n")
