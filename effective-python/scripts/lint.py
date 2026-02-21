#!/usr/bin/env python3
"""
lint.py — Ruff linter tuned to Effective Python items.
Usage: python lint.py <path>

Runs ruff with rules that map directly to Effective Python advice,
then annotates each violation with the relevant item number and title.
"""

import json
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

# Maps ruff rule code prefixes/exact codes -> (Item number, short description)
RULE_TO_ITEM = {
    "E711": ("Item 2",  "PEP 8: use 'is None' / 'is not None', not == None"),
    "E712": ("Item 2",  "PEP 8: use 'is True' / 'is False', not == True/False"),
    "B006": ("Item 24", "Avoid mutable default arguments"),
    "B007": ("Item 7",  "Unused loop variable — use _ for throwaway"),
    "B008": ("Item 24", "Do not call mutable objects as default arguments"),
    "C400": ("Item 27", "Rewrite map() as a list comprehension"),
    "C401": ("Item 27", "Rewrite set() with a comprehension"),
    "C402": ("Item 27", "Rewrite dict() with a dict comprehension"),
    "C403": ("Item 27", "Rewrite list() with a list comprehension"),
    "C404": ("Item 27", "Rewrite list of tuples as dict comprehension"),
    "C405": ("Item 27", "Rewrite set literal — unnecessary literal call"),
    "C406": ("Item 27", "Rewrite dict literal — unnecessary literal call"),
    "C408": ("Item 27", "Rewrite dict()/list()/tuple() with literal"),
    "C409": ("Item 28", "Unnecessary literal in tuple()"),
    "C410": ("Item 28", "Unnecessary literal in list()"),
    "C411": ("Item 27", "Unnecessary list() call"),
    "C413": ("Item 27", "Unnecessary list/reversed() around sorted()"),
    "C414": ("Item 27", "Unnecessary double cast in comprehension"),
    "C415": ("Item 29", "Unnecessary subscript reversal in comprehension"),
    "C416": ("Item 27", "Unnecessary list comprehension — use list()"),
    "C417": ("Item 27", "Unnecessary map() — use generator/comprehension"),
    "SIM101": ("Item 7",  "Merge duplicate isinstance() checks with tuple"),
    "SIM102": ("Item 7",  "Collapse nested if into single if"),
    "SIM103": ("Item 7",  "Return condition directly, not if/else True/False"),
    "SIM105": ("Item 35", "Use contextlib.suppress instead of try/except/pass"),
    "SIM108": ("Item 7",  "Use ternary operator instead of if/else block"),
    "SIM110": ("Item 27", "Use comprehension instead of for-loop with append"),
    "SIM115": ("Item 66", "Use context manager for open()"),
    "SIM117": ("Item 66", "Merge nested with statements"),
    "UP001": ("Item 2",  "pyupgrade: use modern Python syntax"),
    "UP003": ("Item 2",  "pyupgrade: use type() instead of deprecated form"),
    "UP006": ("Item 90", "Use 'list' instead of 'List' for type hints (3.9+)"),
    "UP007": ("Item 90", "Use 'X | Y' instead of 'Optional[X]' (3.10+)"),
    "UP008": ("Item 90", "Use 'super()' without arguments"),
    "UP009": ("Item 2",  "pyupgrade: UTF-8 encoding declaration unnecessary"),
    "UP010": ("Item 2",  "pyupgrade: unnecessary __future__ import"),
    "UP032": ("Item 4",  "Use f-string instead of .format()"),
    "UP034": ("Item 2",  "pyupgrade: extraneous parentheses"),
}

RUFF_CONFIG = textwrap.dedent("""\
    [lint]
    select = [
        "E711", "E712",
        "B006", "B007", "B008",
        "C4",
        "SIM",
        "UP",
    ]
    ignore = []
""")


def find_item(code: str):
    if code in RULE_TO_ITEM:
        return RULE_TO_ITEM[code]
    # Try prefix match (e.g. SIM, UP, C4xx)
    for prefix_len in (5, 4, 3, 2):
        prefix = code[:prefix_len]
        if prefix in RULE_TO_ITEM:
            return RULE_TO_ITEM[prefix]
    return None


def run_ruff(target: Path, config_path: Path):
    cmd = [
        "ruff", "check",
        "--config", str(config_path),
        "--output-format", "json",
        str(target),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return None, "NOT_FOUND", 1
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT", 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python lint.py <path>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Error: path not found: {target}")
        sys.exit(1)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", prefix="ruff_ep_", delete=False
    ) as tmp:
        tmp.write(RUFF_CONFIG)
        config_path = Path(tmp.name)

    try:
        stdout, stderr, returncode = run_ruff(target, config_path)
    finally:
        config_path.unlink(missing_ok=True)

    if stdout is None:
        if stderr == "NOT_FOUND":
            print("Error: ruff is not installed.")
            print("Install it with:  pip install ruff")
            print("Or globally:      pipx install ruff")
        elif stderr == "TIMEOUT":
            print("Error: ruff timed out.")
        else:
            print(f"Error running ruff: {stderr}")
        sys.exit(1)

    print(f"Effective Python lint report — {target}")
    print("-" * 70)

    try:
        violations = json.loads(stdout) if stdout.strip() else []
    except json.JSONDecodeError:
        print("Raw ruff output:")
        print(stdout)
        sys.exit(returncode)

    if not violations:
        print("No violations found. Code aligns well with Effective Python.")
        sys.exit(0)

    # Group by item
    by_item: dict[str, list] = {}
    for v in violations:
        code = v.get("code", "?")
        mapping = find_item(code)
        item_key = mapping[0] if mapping else "Other"
        by_item.setdefault(item_key, []).append((v, mapping))

    total = 0
    for item_key in sorted(by_item):
        entries = by_item[item_key]
        item_desc = entries[0][1][1] if entries[0][1] else "ruff violation"
        print(f"\n[{item_key}] {item_desc}")
        for v, _ in entries:
            loc = v.get("location", {})
            row, col = loc.get("row", "?"), loc.get("column", "?")
            filename = Path(v.get("filename", str(target))).name
            message = v.get("message", "")
            code = v.get("code", "?")
            print(f"  {filename}:{row}:{col}  [{code}] {message}")
            total += 1

    print(f"\n{'-' * 70}")
    print(f"Total violations: {total}")
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
