#!/usr/bin/env python3
"""
audit_css.py — Audit CSS/SCSS/HTML files for Refactoring UI anti-patterns.
Usage: python audit_css.py <file_or_directory>

Detects:
  1. One-off hex colors (likely not from a design scale)
  2. Arbitrary pixel values not on a standard spacing scale
  3. Flat visual hierarchy (too many elements sharing the same font-size)
  4. Inline styles in HTML (maintainability anti-pattern)
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SPACING_SCALE = {4, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48, 56, 64, 80, 96, 112, 128}
FLAT_HIERARCHY_THRESHOLD = 3   # more than N elements sharing same font-size
EXTENSIONS = {".css", ".scss", ".html", ".htm"}

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

RE_HEX_COLOR = re.compile(r"#([0-9a-fA-F]{3,8})\b")
RE_PX_VALUE = re.compile(r"\b(\d+)px\b")
RE_FONT_SIZE_PX = re.compile(r"font-size\s*:\s*(\d+)px", re.IGNORECASE)
RE_INLINE_STYLE = re.compile(r'\bstyle\s*=\s*["\'][^"\']*["\']', re.IGNORECASE)
RE_CSS_VAR = re.compile(r"var\(--[^)]+\)")
RE_SCSS_VAR = re.compile(r"\$[a-zA-Z_][\w-]*")

# Pixel properties where arbitrary values matter (spacing/sizing, not borders)
SPACING_PROPERTIES = re.compile(
    r"(margin|padding|top|right|bottom|left|width|height|gap|"
    r"border-radius|letter-spacing|line-height)\s*:",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

Issue = dict  # {"line": int, "col": int, "code": str, "message": str, "suggestion": str}


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        print(f"Warning: cannot read {path}: {exc}")
        return []


def is_in_comment(line: str, col: int) -> bool:
    """Rough check: is the match inside a CSS/HTML comment on this line?"""
    before = line[:col]
    return "/*" in before or "<!--" in before or "//" in before


# ---------------------------------------------------------------------------
# Detectors
# ---------------------------------------------------------------------------

def detect_one_off_hex_colors(lines: list[str], filepath: Path) -> list[Issue]:
    """Flag hex colors that appear only once in the file — likely not from a scale."""
    color_locations: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for lineno, line in enumerate(lines, 1):
        for m in RE_HEX_COLOR.finditer(line):
            # Skip if preceded by var( or $ (already a token)
            prefix = line[max(0, m.start() - 10):m.start()]
            if "var(" in prefix or "$" in prefix[-1:]:
                continue
            normalized = m.group(0).upper()
            color_locations[normalized].append((lineno, m.start()))

    issues = []
    for color, locations in color_locations.items():
        if len(locations) == 1:
            lineno, col = locations[0]
            issues.append({
                "line": lineno, "col": col + 1,
                "code": "RUI-C01",
                "message": f"One-off color {color} — not reused anywhere in this file",
                "suggestion": f"Extract to a CSS variable: --color-name: {color}; and reference via var(--color-name)",
            })
    return issues


def detect_arbitrary_px_values(lines: list[str], filepath: Path) -> list[Issue]:
    """Flag pixel values on spacing properties that fall outside the spacing scale."""
    issues = []
    in_spacing_context = False
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if SPACING_PROPERTIES.search(stripped):
            for m in RE_PX_VALUE.finditer(stripped):
                value = int(m.group(1))
                if value == 0 or value in SPACING_SCALE:
                    continue
                if is_in_comment(line, m.start()):
                    continue
                nearest = min(SPACING_SCALE, key=lambda s: abs(s - value))
                issues.append({
                    "line": lineno, "col": m.start() + 1,
                    "code": "RUI-S01",
                    "message": f"Arbitrary pixel value {value}px not on spacing scale",
                    "suggestion": f"Nearest scale value: {nearest}px. Consider using a spacing token.",
                })
    return issues


def detect_flat_hierarchy(lines: list[str], filepath: Path) -> list[Issue]:
    """Flag when many rules share the same font-size — suggests flat visual hierarchy."""
    size_locations: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for lineno, line in enumerate(lines, 1):
        for m in RE_FONT_SIZE_PX.finditer(line):
            size = int(m.group(1))
            size_locations[size].append((lineno, m.start()))

    issues = []
    for size, locations in size_locations.items():
        if len(locations) > FLAT_HIERARCHY_THRESHOLD:
            # Report at the first occurrence
            lineno, col = locations[0]
            issues.append({
                "line": lineno, "col": col + 1,
                "code": "RUI-H01",
                "message": (
                    f"font-size: {size}px used {len(locations)} times — "
                    f"indicates flat visual hierarchy"
                ),
                "suggestion": (
                    "Refactoring UI: vary font sizes more aggressively to create "
                    "clear hierarchy. Use a type scale (e.g. 12, 14, 16, 20, 24, 32, 48px)."
                ),
            })
    return issues


def detect_inline_styles(lines: list[str], filepath: Path) -> list[Issue]:
    """Flag inline style= attributes in HTML files."""
    if filepath.suffix.lower() not in {".html", ".htm"}:
        return []
    issues = []
    for lineno, line in enumerate(lines, 1):
        for m in RE_INLINE_STYLE.finditer(line):
            issues.append({
                "line": lineno, "col": m.start() + 1,
                "code": "RUI-M01",
                "message": f"Inline style attribute — hard to maintain and override",
                "suggestion": "Move styles to a CSS class. Inline styles defeat cascade and make theming impossible.",
            })
    return issues


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_file(path: Path) -> list[Issue]:
    lines = read_lines(path)
    if not lines:
        return []
    issues = []
    issues.extend(detect_one_off_hex_colors(lines, path))
    issues.extend(detect_arbitrary_px_values(lines, path))
    issues.extend(detect_flat_hierarchy(lines, path))
    issues.extend(detect_inline_styles(lines, path))
    return sorted(issues, key=lambda i: (i["line"], i["col"]))


def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() in EXTENSIONS else []
    return sorted(p for p in target.rglob("*") if p.suffix.lower() in EXTENSIONS)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(results: dict[Path, list[Issue]]) -> int:
    total = sum(len(v) for v in results.values())
    files_with_issues = sum(1 for v in results.values() if v)

    print("=" * 72)
    print("REFACTORING UI CSS AUDIT REPORT")
    print("=" * 72)

    # Group by code across all files for summary
    by_code: dict[str, list[tuple[Path, Issue]]] = defaultdict(list)

    for path, issues in results.items():
        if not issues:
            continue
        print(f"\n{path}")
        print("-" * 72)
        for issue in issues:
            print(f"  Line {issue['line']:>4}:{issue['col']:<4} [{issue['code']}] {issue['message']}")
            print(f"           -> {issue['suggestion']}")
            by_code[issue["code"]].append((path, issue))

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    CODE_LABELS = {
        "RUI-C01": "One-off colors (not from a scale)",
        "RUI-S01": "Arbitrary pixel values",
        "RUI-H01": "Flat visual hierarchy",
        "RUI-M01": "Inline styles in HTML",
    }
    for code, label in CODE_LABELS.items():
        count = len(by_code.get(code, []))
        marker = "[!]" if count else "[OK]"
        print(f"  {marker} {label}: {count} issue(s)")

    print(f"\nFiles scanned : {len(results)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total issues  : {total}")
    print("=" * 72)
    return total


def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_css.py <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Error: path not found: {target}")
        sys.exit(1)

    files = collect_files(target)
    if not files:
        print(f"No CSS/SCSS/HTML files found in: {target}")
        sys.exit(0)

    results = {f: scan_file(f) for f in files}
    total = print_report(results)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
