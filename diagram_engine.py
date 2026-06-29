"""
diagram_engine.py — Extract Python diagram code blocks from Opus output and execute them.

Supports:
  • schemdraw  — electrical schematics → SVG
  • matplotlib — block / system diagrams → PNG
  • schematic_lib — raw SVG primitives → SVG
  • fixture_diagrammer — FixtureDiagrammer class → PNG / PDF

Each code block must declare its output filename in a comment header:
  # DIAGRAM: <name> | TYPE: schemdraw | OUTPUT: <filename>.svg

The engine injects OUTPUT_DIR into each script's exec namespace so code
can use  OUTPUT_DIR + "/name.svg"  without hardcoding paths.
"""

import re
import os
import sys
import traceback
import textwrap
from pathlib import Path

# ── Code-block extraction ──────────────────────────────────────────────────────

# Match fenced Python code blocks with optional diagram header comment
_FENCE_RE = re.compile(
    r"```python\s*\n"           # opening fence
    r"(.*?)"                    # code content (captured)
    r"```",                     # closing fence
    re.DOTALL,
)

_HEADER_RE = re.compile(
    r"#\s*DIAGRAM:\s*(?P<name>[^\|]+)"
    r"(?:\s*\|\s*TYPE:\s*(?P<dtype>[^\|]+))?"
    r"(?:\s*\|\s*OUTPUT:\s*(?P<output>\S+))?",
    re.IGNORECASE,
)


def extract_code_blocks(opus_text: str) -> list[dict]:
    """
    Extract all ```python ... ``` blocks from Opus output.

    Returns list of dicts:
      {name, dtype, output_file, code}
    """
    blocks = []
    for match in _FENCE_RE.finditer(opus_text):
        code = match.group(1).strip()
        if not code:
            continue

        # Parse header comment (first line)
        first_line = code.split("\n")[0]
        header     = _HEADER_RE.search(first_line)

        if header:
            name    = header.group("name").strip()
            dtype   = (header.group("dtype") or "schemdraw").strip().lower()
            outfile = (header.group("output") or f"{name}.svg").strip()
        else:
            # No header — infer from code content
            name    = f"diagram_{len(blocks)+1}"
            dtype   = _infer_type(code)
            outfile = f"{name}.{'svg' if dtype == 'schemdraw' else 'png'}"

        blocks.append({
            "name":        name,
            "dtype":       dtype,
            "output_file": outfile,
            "code":        code,
        })

    return blocks


def _infer_type(code: str) -> str:
    """Guess diagram type from import statements."""
    if "schemdraw" in code:
        return "schemdraw"
    if "matplotlib" in code or "FixtureDiagrammer" in code:
        return "matplotlib"
    if "schematic_lib" in code:
        return "schematic_lib"
    return "schemdraw"


# ── Code patching ──────────────────────────────────────────────────────────────

def _patch_save_paths(code: str, output_dir: str) -> str:
    """
    Rewrite save/savefig calls so they always land in output_dir.

    Handles:
      d.save("name.svg")              → d.save("<output_dir>/name.svg")
      plt.savefig("name.png", ...)    → same
      diag.save("name.pdf")           → same
    """
    # Replace any quoted path that looks like a filename (no directory component)
    # leaving absolute paths untouched.
    def _fix_path(m):
        quote = m.group(1)
        path  = m.group(2)
        if os.path.isabs(path) or output_dir in path:
            return m.group(0)
        basename = os.path.basename(path)
        new_path = os.path.join(output_dir, basename).replace("\\", "/")
        return f"{quote}{new_path}{quote}"

    patched = re.sub(r'(["\'])([^"\']+\.(svg|png|pdf|jpg))\1', _fix_path, code)
    # Also replace OUTPUT_PATH / OUTPUT_DIR variables if Opus used them
    patched = patched.replace("OUTPUT_PATH", repr(output_dir))
    patched = patched.replace("OUTPUT_DIR",  repr(output_dir))
    return patched


# ── Execution ──────────────────────────────────────────────────────────────────

def _run_code_block(block: dict, output_dir: str) -> dict:
    """
    Execute a single diagram code block.

    Returns:
      {"name", "output_file", "success", "error", "path"}
    """
    code      = block["code"]
    outfile   = block["output_file"]
    dtype     = block["dtype"]
    out_path  = os.path.join(output_dir, os.path.basename(outfile))

    # Patch save paths and inject output_dir
    code = _patch_save_paths(code, output_dir)

    # Add sys.path so scripts/ helpers are importable
    scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
    preamble = textwrap.dedent(f"""\
        import sys, os
        sys.path.insert(0, {repr(scripts_dir)})
        OUTPUT_DIR = {repr(output_dir)}
        OUTPUT_PATH = {repr(output_dir)}
    """)
    full_code = preamble + "\n" + code

    print(f"\n  Rendering: {block['name']}  [{dtype}]  → {os.path.basename(outfile)}")

    try:
        exec_globals = {"__name__": "__exec__"}
        exec(compile(full_code, f"<diagram:{block['name']}>", "exec"), exec_globals)

        # Verify file was created
        if os.path.exists(out_path):
            size = os.path.getsize(out_path)
            print(f"  ✓ Saved: {out_path}  ({size:,} bytes)")
            return {"name": block["name"], "output_file": outfile,
                    "path": out_path, "success": True, "error": None}
        else:
            # Maybe the code saved under a different name — search output_dir
            candidates = list(Path(output_dir).glob(f"*{Path(outfile).suffix}"))
            if candidates:
                found = str(candidates[-1])
                print(f"  ✓ Found at: {found}")
                return {"name": block["name"], "output_file": outfile,
                        "path": found, "success": True, "error": None}
            msg = f"Code ran but output file not found: {out_path}"
            print(f"  ✗ {msg}")
            return {"name": block["name"], "output_file": outfile,
                    "path": None, "success": False, "error": msg}

    except Exception as exc:
        tb = traceback.format_exc()
        print(f"  ✗ Execution error:\n{tb}")
        return {"name": block["name"], "output_file": outfile,
                "path": None, "success": False, "error": str(exc)}


# ── Public API ─────────────────────────────────────────────────────────────────

def render_diagrams(opus_text: str, output_dir: str) -> list[dict]:
    """
    Extract all diagram code blocks from Opus output, execute each, and
    return a list of result dicts with file paths for doc assembly.

    Args:
        opus_text   : Full text response from Opus.
        output_dir  : Folder where diagram files are saved.

    Returns:
        List of {"name", "path", "output_file", "success", "error"}
    """
    os.makedirs(output_dir, exist_ok=True)
    blocks = extract_code_blocks(opus_text)

    if not blocks:
        print("  [diagram_engine] No Python code blocks found in Opus output.")
        print("  → Diagrams will not be embedded in PDF/docx.")
        return []

    print(f"\n  Found {len(blocks)} diagram code block(s) to render.")

    results = []
    for block in blocks:
        result = _run_code_block(block, output_dir)
        results.append(result)

    success = sum(1 for r in results if r["success"])
    print(f"\n  Diagram rendering: {success}/{len(results)} successful.")
    return results


def successful_diagrams(results: list[dict]) -> list[str]:
    """Return just the file paths of successfully rendered diagrams."""
    return [r["path"] for r in results if r["success"] and r["path"]]
