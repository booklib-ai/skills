#!/usr/bin/env python3
"""
check_blocking.py — Static analyser for blocking calls inside async functions.

Usage: python check_blocking.py <file_or_directory> [<file_or_directory> ...]

Flags:
  --exit-zero   Exit 0 even when issues are found (useful in CI to report only)
  --summary     Print a summary table at the end
"""

import ast
import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------
# Each rule is (description, fix_hint, matcher_function)
# matcher_function(node) -> bool


def _call_matches(node: ast.expr, *name_parts: str) -> bool:
    """True if node is a Call whose function matches the dotted name."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    # Simple name: open, sleep, etc.
    if len(name_parts) == 1 and isinstance(func, ast.Name):
        return func.id == name_parts[0]
    # Attribute: requests.get, time.sleep, etc.
    if len(name_parts) == 2 and isinstance(func, ast.Attribute):
        obj = func.value
        return isinstance(obj, ast.Name) and obj.id == name_parts[0] and func.attr == name_parts[1]
    return False


def _is_sync_open(node: ast.expr) -> bool:
    """Flags open() calls that are not preceded by 'async with'."""
    return _call_matches(node, "open")


def _is_file_rw(node: ast.expr) -> bool:
    """Flags .read() / .write() attribute calls (heuristic)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return isinstance(func, ast.Attribute) and func.attr in {"read", "write", "readlines"}


@dataclass
class Rule:
    id: str
    description: str
    fix: str
    matcher: object  # callable(node) -> bool


RULES: list[Rule] = [
    Rule(
        id="ASYNC001",
        description="requests.get() blocks the event loop",
        fix="Use aiohttp.ClientSession().get() or httpx.AsyncClient().get()",
        matcher=lambda n: _call_matches(n, "requests", "get"),
    ),
    Rule(
        id="ASYNC002",
        description="requests.post() blocks the event loop",
        fix="Use aiohttp.ClientSession().post() or httpx.AsyncClient().post()",
        matcher=lambda n: _call_matches(n, "requests", "post"),
    ),
    Rule(
        id="ASYNC003",
        description="requests.put() blocks the event loop",
        fix="Use aiohttp.ClientSession().put() or httpx.AsyncClient().put()",
        matcher=lambda n: _call_matches(n, "requests", "put"),
    ),
    Rule(
        id="ASYNC004",
        description="requests.delete() blocks the event loop",
        fix="Use aiohttp.ClientSession().delete() or httpx.AsyncClient().delete()",
        matcher=lambda n: _call_matches(n, "requests", "delete"),
    ),
    Rule(
        id="ASYNC005",
        description="time.sleep() blocks the event loop",
        fix="Use 'await asyncio.sleep(seconds)' instead",
        matcher=lambda n: _call_matches(n, "time", "sleep"),
    ),
    Rule(
        id="ASYNC006",
        description="open() is a synchronous file operation",
        fix="Use 'async with aiofiles.open(...)' from the aiofiles package",
        matcher=_is_sync_open,
    ),
    Rule(
        id="ASYNC007",
        description="subprocess.run() blocks the event loop",
        fix="Use 'await asyncio.create_subprocess_exec()' or asyncio.create_subprocess_shell()",
        matcher=lambda n: _call_matches(n, "subprocess", "run"),
    ),
    Rule(
        id="ASYNC008",
        description="subprocess.call() blocks the event loop",
        fix="Use 'await asyncio.create_subprocess_exec()' instead",
        matcher=lambda n: _call_matches(n, "subprocess", "call"),
    ),
    Rule(
        id="ASYNC009",
        description=".read()/.write()/.readlines() on a synchronous file handle",
        fix="Open the file with aiofiles and use 'await file.read()' / 'await file.write()'",
        matcher=_is_file_rw,
    ),
]


# ---------------------------------------------------------------------------
# Finding
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    file: Path
    line: int
    col: int
    async_func: str
    rule: Rule


def _collect_async_funcs(tree: ast.AST) -> Iterator[ast.AsyncFunctionDef]:
    """Yield all async def nodes in the tree, including nested ones."""
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef):
            yield node


def _nodes_inside_sync_context(func_node: ast.AsyncFunctionDef) -> set[int]:
    """
    Return the set of node ids that are inside a nested sync def or class,
    so we don't flag blocking calls that are legitimately in sync helpers.
    """
    excluded: set[int] = set()
    for node in ast.walk(func_node):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            for child in ast.walk(node):
                excluded.add(id(child))
    return excluded


def check_file(path: Path) -> list[Finding]:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"ERROR: Cannot read {path}: {exc}", file=sys.stderr)
        return []

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        print(f"ERROR: Syntax error in {path}: {exc}", file=sys.stderr)
        return []

    findings: list[Finding] = []

    for async_func in _collect_async_funcs(tree):
        excluded = _nodes_inside_sync_context(async_func)
        for node in ast.walk(async_func):
            if id(node) in excluded:
                continue
            for rule in RULES:
                if rule.matcher(node):
                    findings.append(
                        Finding(
                            file=path,
                            line=node.lineno,
                            col=node.col_offset,
                            async_func=async_func.name,
                            rule=rule,
                        )
                    )
    return findings


def iter_python_files(path: Path) -> Iterator[Path]:
    if path.is_file():
        if path.suffix == ".py":
            yield path
    elif path.is_dir():
        yield from sorted(path.rglob("*.py"))
    else:
        print(f"WARNING: {path} is not a file or directory — skipping.", file=sys.stderr)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_findings(findings: list[Finding]) -> None:
    for f in findings:
        print(
            f"{f.file}:{f.line}:{f.col}: [{f.rule.id}] "
            f"In 'async def {f.async_func}': {f.rule.description}"
        )
        print(f"  Fix: {f.rule.fix}")


def print_summary(all_findings: list[Finding]) -> None:
    if not all_findings:
        print("\nSummary: No blocking call issues found.")
        return

    from collections import Counter
    by_rule: Counter = Counter(f.rule.id for f in all_findings)
    by_file: Counter = Counter(str(f.file) for f in all_findings)

    print("\n--- Summary ---")
    print(f"Total issues: {len(all_findings)}")
    print("\nBy rule:")
    for rule_id, count in sorted(by_rule.items()):
        rule = next(r for r in RULES if r.id == rule_id)
        print(f"  {rule_id}: {count}x  ({rule.description})")
    print("\nBy file:")
    for filepath, count in sorted(by_file.items()):
        print(f"  {count:3d}  {filepath}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find blocking calls inside async functions."
    )
    parser.add_argument(
        "paths", nargs="+", type=Path, metavar="file_or_dir",
        help="Python file(s) or director(ies) to analyse"
    )
    parser.add_argument(
        "--exit-zero", action="store_true",
        help="Always exit 0 (useful for non-blocking CI report)"
    )
    parser.add_argument(
        "--summary", action="store_true",
        help="Print a summary table after the findings"
    )
    args = parser.parse_args()

    all_findings: list[Finding] = []
    for raw_path in args.paths:
        for py_file in iter_python_files(raw_path):
            findings = check_file(py_file)
            all_findings.extend(findings)
            print_findings(findings)

    if args.summary:
        print_summary(all_findings)

    if not all_findings:
        print("No blocking call issues detected.")

    if all_findings and not args.exit_zero:
        sys.exit(1)


if __name__ == "__main__":
    main()
