#!/usr/bin/env python3
"""
pre-review.py — Pre-analysis script for Clean Code reviews.
Usage: python pre-review.py <file>

Produces a structured report covering file stats, long functions, deep nesting,
argument count violations, and linter output — ready to feed an agent as context.
"""

import ast
import os
import subprocess
import sys
from pathlib import Path


def detect_language(path: Path) -> str:
    return {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".go": "go",
        ".rb": "ruby",
        ".rs": "rust",
    }.get(path.suffix.lower(), "unknown")


def count_lines(source: str) -> int:
    return len(source.splitlines())


def measure_nesting_depth(node: ast.AST, depth: int = 0) -> int:
    nesting_nodes = (
        ast.If, ast.For, ast.While, ast.With, ast.Try,
        ast.ExceptHandler, ast.AsyncFor, ast.AsyncWith,
    )
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, nesting_nodes):
            max_depth = max(max_depth, measure_nesting_depth(child, depth + 1))
        else:
            max_depth = max(max_depth, measure_nesting_depth(child, depth))
    return max_depth


def analyze_python_ast(source: str):
    """Return function/class stats using AST. Returns list of dicts."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return None, f"AST parse failed: {exc}"

    lines = source.splitlines()
    results = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue

        kind = "class" if isinstance(node, ast.ClassDef) else "function"
        start = node.lineno
        end = node.end_lineno if hasattr(node, "end_lineno") else start
        length = end - start + 1

        arg_count = 0
        nesting = 0
        if kind == "function":
            args = node.args
            arg_count = (
                len(args.args)
                + len(args.posonlyargs)
                + len(args.kwonlyargs)
                + (1 if args.vararg else 0)
                + (1 if args.kwarg else 0)
            )
            # Don't count 'self' / 'cls'
            first = args.posonlyargs[0].arg if args.posonlyargs else (args.args[0].arg if args.args else None)
            if first in ("self", "cls"):
                arg_count = max(0, arg_count - 1)
            nesting = measure_nesting_depth(node)

        results.append({
            "kind": kind,
            "name": node.name,
            "start": start,
            "end": end,
            "length": length,
            "arg_count": arg_count,
            "nesting": nesting,
        })

    return results, None


def run_ruff(filepath: Path):
    """Run ruff on the file; return (output_lines, error_message)."""
    try:
        result = subprocess.run(
            ["ruff", "check", "--output-format", "concise", str(filepath)],
            capture_output=True, text=True, timeout=30,
        )
        output = (result.stdout + result.stderr).strip()
        return output.splitlines() if output else [], None
    except FileNotFoundError:
        return [], "ruff not installed (pip install ruff)"
    except subprocess.TimeoutExpired:
        return [], "ruff timed out"


def separator(char="-", width=70):
    return char * width


def main():
    if len(sys.argv) < 2:
        print("Usage: python pre-review.py <file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: file not found: {filepath}")
        sys.exit(1)

    source = filepath.read_text(encoding="utf-8", errors="replace")
    language = detect_language(filepath)
    total_lines = count_lines(source)
    file_size = filepath.stat().st_size

    print(separator("="))
    print(f"CLEAN CODE PRE-REVIEW REPORT")
    print(separator("="))
    print(f"File     : {filepath}")
    print(f"Language : {language}")
    print(f"Size     : {file_size:,} bytes  |  {total_lines} lines")
    print()

    # --- AST analysis (Python only) ---
    if language == "python":
        print(separator())
        print("FUNCTION / CLASS ANALYSIS (AST)")
        print(separator())
        items, err = analyze_python_ast(source)
        if err:
            print(f"  Warning: {err}")
        elif items:
            long_fns = [i for i in items if i["kind"] == "function" and i["length"] > 20]
            deep_fns = [i for i in items if i["kind"] == "function" and i["nesting"] >= 3]
            many_args = [i for i in items if i["kind"] == "function" and i["arg_count"] > 3]

            print(f"  Total functions : {sum(1 for i in items if i['kind'] == 'function')}")
            print(f"  Total classes   : {sum(1 for i in items if i['kind'] == 'class')}")
            print()

            if long_fns:
                print(f"  [!] LONG FUNCTIONS (>20 lines) — Clean Code: functions should do one thing")
                for fn in long_fns:
                    print(f"      {fn['name']}()  lines {fn['start']}-{fn['end']}  ({fn['length']} lines)")
            else:
                print("  [OK] No functions exceed 20 lines.")

            print()
            if deep_fns:
                print(f"  [!] DEEP NESTING (>=3 levels) — consider early returns or extraction")
                for fn in deep_fns:
                    print(f"      {fn['name']}()  line {fn['start']}  (max nesting: {fn['nesting']})")
            else:
                print("  [OK] No functions have excessive nesting depth.")

            print()
            if many_args:
                print(f"  [!] TOO MANY ARGUMENTS (>3) — Clean Code: prefer parameter objects")
                for fn in many_args:
                    print(f"      {fn['name']}()  line {fn['start']}  ({fn['arg_count']} args)")
            else:
                print("  [OK] All functions have 3 or fewer arguments.")
        else:
            print("  No functions or classes found.")
        print()

    # --- Linter output ---
    print(separator())
    if language == "python":
        print("RUFF LINTER OUTPUT")
        print(separator())
        ruff_lines, ruff_err = run_ruff(filepath)
        if ruff_err:
            print(f"  Note: {ruff_err}")
        elif ruff_lines:
            for line in ruff_lines:
                print(f"  {line}")
        else:
            print("  [OK] ruff found no issues.")
    else:
        print(f"LINTER")
        print(separator())
        print(f"  Automated linting not configured for '{language}'. Run language-specific tools manually.")

    print()
    print(separator("="))
    print("END OF PRE-REVIEW REPORT")
    print(separator("="))


if __name__ == "__main__":
    main()
