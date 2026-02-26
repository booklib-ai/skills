#!/usr/bin/env python3
"""
audit_animations.py - Audit CSS/SCSS for animation anti-patterns.

Usage:
    python audit_animations.py <file_or_directory>

Scans .css and .scss files for animation anti-patterns documented in
"Animation at Work" by Rachel Nabors.

Checks performed:
  1. Animating layout-triggering properties (use transform instead)
  2. transition: all (too broad)
  3. Transitions > 500ms or animations > 1000ms (too slow)
  4. Durations < 100ms (too fast to perceive)
  5. linear easing on UI transitions (use ease-out or cubic-bezier)
  6. Missing prefers-reduced-motion in files that animate
  7. infinite animations without a pause mechanism

Outputs: file, line, offending CSS, and recommended fix.
Summary at end: total issues by category.
"""

import argparse
import pathlib
import re
import sys
from collections import defaultdict
from typing import NamedTuple


class Issue(NamedTuple):
    file: str
    line: int
    category: str
    snippet: str
    advice: str


# Properties that trigger layout recalculation — animating them is expensive.
LAYOUT_TRIGGERING = [
    "width", "height", "top", "left", "right", "bottom",
    "margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
    "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
]

CATEGORIES = {
    "layout_property": "Layout-triggering property animated",
    "transition_all": "transition: all used",
    "too_slow": "Duration too long (sluggish UI)",
    "too_fast": "Duration too short (imperceptible)",
    "linear_easing": "Linear easing on UI transition",
    "no_reduced_motion": "Missing prefers-reduced-motion",
    "infinite_no_pause": "Infinite animation without pause mechanism",
}


def parse_duration_ms(value: str) -> float | None:
    """Convert a CSS duration string (e.g. '0.3s', '300ms') to milliseconds."""
    value = value.strip()
    if value.endswith("ms"):
        try:
            return float(value[:-2])
        except ValueError:
            return None
    if value.endswith("s"):
        try:
            return float(value[:-1]) * 1000
        except ValueError:
            return None
    return None


def find_css_files(path: pathlib.Path) -> list[pathlib.Path]:
    if path.is_file():
        if path.suffix in {".css", ".scss"}:
            return [path]
        print(f"WARNING: {path} is not a .css or .scss file — skipping.")
        return []
    return sorted(path.rglob("*.css")) + sorted(path.rglob("*.scss"))


def audit_file(filepath: pathlib.Path) -> list[Issue]:
    issues: list[Issue] = []
    try:
        lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        print(f"ERROR reading {filepath}: {exc}")
        return []

    file_str = filepath.as_posix()
    full_text = "\n".join(lines)

    has_animation = bool(
        re.search(r"\b(transition|animation)\s*:", full_text)
    )
    has_reduced_motion = "prefers-reduced-motion" in full_text

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("//") or line.startswith("/*"):
            continue

        # 1. Animating layout-triggering properties
        transition_match = re.match(r"transition\s*:\s*(.+)", line, re.IGNORECASE)
        if transition_match:
            props_part = transition_match.group(1)
            for prop in LAYOUT_TRIGGERING:
                if re.search(r"\b" + re.escape(prop) + r"\b", props_part, re.IGNORECASE):
                    issues.append(Issue(
                        file=file_str,
                        line=lineno,
                        category="layout_property",
                        snippet=line[:120],
                        advice=(
                            f"Animating '{prop}' triggers layout recalculation on every frame. "
                            "Use 'transform: translate/scale' or 'opacity' instead — "
                            "these are compositor-only and do not cause reflow."
                        ),
                    ))

        # 2. transition: all
        if re.search(r"transition\s*:\s*all\b", line, re.IGNORECASE):
            issues.append(Issue(
                file=file_str,
                line=lineno,
                category="transition_all",
                snippet=line[:120],
                advice=(
                    "'transition: all' animates every animatable property, including "
                    "layout-triggering ones you may not intend. List specific properties: "
                    "e.g., 'transition: opacity 0.2s ease-out, transform 0.2s ease-out'."
                ),
            ))

        # 3 & 4. Duration checks — transition and animation shorthand
        duration_patterns = [
            re.compile(r"transition\s*:[^;]+", re.IGNORECASE),
            re.compile(r"animation\s*:[^;]+", re.IGNORECASE),
            re.compile(r"transition-duration\s*:\s*([^;]+)", re.IGNORECASE),
            re.compile(r"animation-duration\s*:\s*([^;]+)", re.IGNORECASE),
        ]
        for pat in duration_patterns:
            m = pat.search(line)
            if not m:
                continue
            value_str = m.group(0)
            is_animation = "animation" in value_str.lower() and "transition" not in value_str.lower()
            for dur_match in re.finditer(r"\d+(?:\.\d+)?(?:ms|s)\b", value_str):
                dur_ms = parse_duration_ms(dur_match.group(0))
                if dur_ms is None:
                    continue
                slow_limit = 1000 if is_animation else 500
                if dur_ms > slow_limit:
                    issues.append(Issue(
                        file=file_str,
                        line=lineno,
                        category="too_slow",
                        snippet=line[:120],
                        advice=(
                            f"Duration {dur_ms:.0f}ms feels sluggish for UI feedback. "
                            f"Keep UI transitions under {slow_limit}ms. "
                            "Aim for 200-300ms for most interactions."
                        ),
                    ))
                elif dur_ms < 100 and dur_ms > 0:
                    issues.append(Issue(
                        file=file_str,
                        line=lineno,
                        category="too_fast",
                        snippet=line[:120],
                        advice=(
                            f"Duration {dur_ms:.0f}ms is below the human perception threshold (~100ms). "
                            "The animation will not be noticed. Use 100-200ms for snappy transitions."
                        ),
                    ))

        # 5. Linear easing on transitions
        if re.search(r"transition\s*:", line, re.IGNORECASE):
            if re.search(r"\blinear\b", line, re.IGNORECASE):
                issues.append(Issue(
                    file=file_str,
                    line=lineno,
                    category="linear_easing",
                    snippet=line[:120],
                    advice=(
                        "Linear easing feels mechanical and unnatural for UI elements. "
                        "Use 'ease-out' for elements entering the screen, 'ease-in' for "
                        "elements leaving, or a custom cubic-bezier for branded motion."
                    ),
                ))

        # 7. Infinite animation without pause mechanism
        if re.search(r"animation-iteration-count\s*:\s*infinite\b", line, re.IGNORECASE):
            # Check nearby lines (±10) for a paused state or play-state control
            start = max(0, lineno - 10)
            end = min(len(lines), lineno + 10)
            context_block = "\n".join(lines[start:end])
            if "animation-play-state" not in context_block and "paused" not in context_block:
                issues.append(Issue(
                    file=file_str,
                    line=lineno,
                    category="infinite_no_pause",
                    snippet=line[:120],
                    advice=(
                        "Infinite animations can be distracting and drain battery on mobile. "
                        "Add 'animation-play-state: paused' controlled via :hover, :focus, "
                        "or a JS toggle so users can pause it."
                    ),
                ))

    # 6. Missing prefers-reduced-motion
    if has_animation and not has_reduced_motion:
        issues.append(Issue(
            file=file_str,
            line=0,
            category="no_reduced_motion",
            snippet="(entire file)",
            advice=(
                "This file contains animations but no '@media (prefers-reduced-motion: reduce)' "
                "block. Add one to disable or reduce motion for users who request it — "
                "required for WCAG 2.1 AA compliance."
            ),
        ))

    return issues


def print_issues(issues: list[Issue]) -> None:
    for issue in issues:
        loc = f"{issue.file}:{issue.line}" if issue.line else issue.file
        category_label = CATEGORIES.get(issue.category, issue.category)
        print(f"\n[{category_label}]")
        print(f"  Location : {loc}")
        print(f"  CSS      : {issue.snippet}")
        print(f"  Fix      : {issue.advice}")


def print_summary(issues: list[Issue]) -> None:
    counts: dict[str, int] = defaultdict(int)
    for issue in issues:
        counts[issue.category] += 1
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if not counts:
        print("No issues found.")
        return
    for cat, label in CATEGORIES.items():
        count = counts.get(cat, 0)
        if count:
            print(f"  {count:3d}  {label}")
    print(f"  ---")
    print(f"  {sum(counts.values()):3d}  Total issues")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit CSS/SCSS files for animation anti-patterns."
    )
    parser.add_argument(
        "path",
        help="A .css/.scss file or directory to scan recursively.",
    )
    args = parser.parse_args()

    target = pathlib.Path(args.path)
    if not target.exists():
        print(f"ERROR: Path not found: {target}")
        sys.exit(1)

    files = find_css_files(target)
    if not files:
        print("No .css or .scss files found.")
        sys.exit(0)

    print(f"Scanning {len(files)} file(s) ...\n")

    all_issues: list[Issue] = []
    for f in files:
        file_issues = audit_file(f)
        all_issues.extend(file_issues)

    if all_issues:
        print_issues(all_issues)
    else:
        print("No animation anti-patterns detected.")

    print_summary(all_issues)

    sys.exit(1 if all_issues else 0)


if __name__ == "__main__":
    main()
