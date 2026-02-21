#!/usr/bin/env python3
"""
chart_review.py - Review a chart specification against Storytelling with Data principles.

Usage:
    python chart_review.py <spec-file.json>

Spec file format (JSON):
    {
      "title": "Sales by Region Q4",
      "chart_type": "pie",
      "data_points": 8,
      "colors": ["#ff0000", "#00ff00"],
      "has_gridlines": true,
      "has_legend": true,
      "has_direct_labels": false,
      "is_3d": false,
      "y_axis_starts_at_zero": true
    }

All fields are optional. Unrecognised fields are ignored.

Based on "Storytelling with Data" by Cole Nussbaumer Knaflic.
Each finding references the relevant chapter.
"""

import argparse
import json
import pathlib
import sys
from typing import Any

# Severity ordering for output
PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

CHART_TYPE_ALIASES: dict[str, str] = {
    "pie": "pie",
    "donut": "pie",
    "doughnut": "pie",
    "bar": "bar",
    "column": "bar",
    "horizontal bar": "bar",
    "stacked bar": "bar",
    "line": "line",
    "area": "line",
    "scatter": "scatter",
    "bubble": "scatter",
    "table": "table",
    "heatmap": "table",
}

# Action verbs that indicate a title states a finding rather than just labelling axes.
INSIGHT_VERBS = {
    "grew", "declined", "increased", "decreased", "outperformed", "underperformed",
    "surpassed", "dropped", "rose", "fell", "exceeded", "missed", "reached",
    "shows", "reveals", "demonstrates", "highlights", "indicates", "confirms",
    "beats", "lags", "leads", "trails", "spikes", "dips",
}


def load_spec(path: pathlib.Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: Cannot read file: {exc}")
        sys.exit(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON in {path}: {exc}")
        sys.exit(1)


def normalize_chart_type(raw: str) -> str:
    return CHART_TYPE_ALIASES.get(raw.lower().strip(), raw.lower().strip())


def title_is_action_oriented(title: str) -> bool:
    """Return True if the title starts with or contains an insight verb."""
    first_word = title.strip().split()[0].lower().rstrip(".,;:") if title.strip() else ""
    if first_word in INSIGHT_VERBS:
        return True
    # Also accept titles where an insight verb appears early (within first 4 words)
    words = [w.lower().rstrip(".,;:") for w in title.strip().split()[:4]]
    return any(w in INSIGHT_VERBS for w in words)


def check_spec(spec: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def add(priority: str, chapter: str, principle: str, detail: str, recommendation: str) -> None:
        findings.append({
            "priority": priority,
            "chapter": chapter,
            "principle": principle,
            "detail": detail,
            "recommendation": recommendation,
        })

    chart_type_raw = spec.get("chart_type", "")
    chart_type = normalize_chart_type(chart_type_raw) if chart_type_raw else ""
    data_points = spec.get("data_points")
    colors = spec.get("colors", [])
    has_gridlines = spec.get("has_gridlines", False)
    has_legend = spec.get("has_legend", False)
    has_direct_labels = spec.get("has_direct_labels", False)
    is_3d = spec.get("is_3d", False)
    y_axis_zero = spec.get("y_axis_starts_at_zero", True)
    title = spec.get("title", "")

    # Check 1: Pie charts with more than 4 slices
    if chart_type == "pie" and data_points is not None and data_points > 4:
        add(
            priority="HIGH",
            chapter="Chapter 2 - Choosing an Effective Visual",
            principle="Avoid pie charts with many slices",
            detail=f"Pie chart has {data_points} slices. Humans cannot accurately compare non-adjacent arc lengths.",
            recommendation=(
                "Use a horizontal bar chart sorted by value. "
                "Bars make magnitude comparison trivial and scale to many categories."
            ),
        )

    # Check 2: More than 5 colors
    if len(colors) > 5:
        add(
            priority="HIGH",
            chapter="Chapter 4 - Focus Your Audience's Attention",
            principle="Use color strategically, not decoratively",
            detail=f"{len(colors)} colors used. More than 5 colors overwhelm the eye and dilute emphasis.",
            recommendation=(
                "Grey out all categories except the one(s) you want to highlight. "
                "Use a single accent color to draw the eye to the key insight."
            ),
        )

    # Check 3: Gridlines present
    if has_gridlines:
        add(
            priority="MEDIUM",
            chapter="Chapter 3 - Clutter Is Your Enemy",
            principle="Remove chart junk and non-data ink",
            detail="Gridlines are present. They add visual noise without adding information.",
            recommendation=(
                "Remove gridlines entirely, or replace with light grey (#e0e0e0) hairlines. "
                "If reference values matter, use direct annotations on the data instead."
            ),
        )

    # Check 4: Legend without direct labels
    if has_legend and not has_direct_labels:
        add(
            priority="MEDIUM",
            chapter="Chapter 5 - Think Like a Designer",
            principle="Label data directly to reduce cognitive load",
            detail=(
                "A legend forces the reader to look away from the data to decode colors. "
                "This interrupts the reading flow."
            ),
            recommendation=(
                "Place labels directly next to each data series or bar. "
                "Remove the legend. Direct labelling reduces eye travel and speeds comprehension."
            ),
        )

    # Check 5: 3D charts
    if is_3d:
        add(
            priority="HIGH",
            chapter="Chapter 2 - Choosing an Effective Visual",
            principle="Never use 3D visualisations",
            detail=(
                "3D perspective distorts relative bar/slice sizes due to foreshortening. "
                "Viewers cannot accurately read values from a 3D chart."
            ),
            recommendation=(
                "Switch to a flat 2D version of the same chart type. "
                "If depth is meant to encode a third variable, use facets or bubble size instead."
            ),
        )

    # Check 6: Title not action-oriented
    if title:
        if not title_is_action_oriented(title):
            add(
                priority="LOW",
                chapter="Chapter 6 - Dissecting Model Visuals",
                principle="Title should state the insight, not label the axes",
                detail=(
                    f"Title '{title}' describes what the chart shows but does not communicate "
                    "the key takeaway. Readers must infer the insight themselves."
                ),
                recommendation=(
                    "Rewrite the title as a one-sentence finding: e.g., "
                    "'APAC revenue grew 34% year-over-year, outpacing all other regions.' "
                    "This tells readers what to think before they look at the data."
                ),
            )
    else:
        add(
            priority="MEDIUM",
            chapter="Chapter 6 - Dissecting Model Visuals",
            principle="Every chart needs a title",
            detail="No title field found in the spec. Untitled charts require readers to form their own interpretation.",
            recommendation=(
                "Add a descriptive, insight-oriented title that states the key finding directly."
            ),
        )

    # Check 7: Bar chart not starting at zero
    if chart_type == "bar" and y_axis_zero is False:
        add(
            priority="HIGH",
            chapter="Chapter 2 - Choosing an Effective Visual",
            principle="Bar charts must start at zero",
            detail=(
                "The y-axis does not start at zero. Because bar length encodes value, "
                "a truncated axis makes small differences appear dramatically large."
            ),
            recommendation=(
                "Set the y-axis baseline to zero. "
                "If the differences are genuinely small, switch to a line chart, "
                "which does not rely on bar length to encode magnitude."
            ),
        )

    # Check 8: Pie chart for proportional data — general advisory
    if chart_type == "pie":
        add(
            priority="LOW",
            chapter="Chapter 2 - Choosing an Effective Visual",
            principle="Pie charts are rarely the best choice",
            detail=(
                "Even well-formed pie charts are harder to read than bar charts "
                "because humans are poor at judging angles and arc lengths."
            ),
            recommendation=(
                "Consider a single stacked bar (for part-to-whole) or a simple bar chart. "
                "Use a pie only when: (a) there are 2-3 slices and (b) the exact proportions matter less than the part-to-whole story."
            ),
        )

    return findings


def print_findings(findings: list[dict[str, str]]) -> None:
    sorted_findings = sorted(findings, key=lambda f: PRIORITY_ORDER.get(f["priority"], 99))

    if not sorted_findings:
        print("No issues found. The chart spec looks good against Storytelling with Data principles.")
        return

    print(f"Found {len(sorted_findings)} issue(s):\n")
    for i, finding in enumerate(sorted_findings, start=1):
        priority = finding["priority"]
        priority_display = f"[{priority}]"
        print(f"{i}. {priority_display} {finding['principle']}")
        print(f"   Chapter      : {finding['chapter']}")
        print(f"   Detail       : {finding['detail']}")
        print(f"   Recommended  : {finding['recommendation']}")
        print()

    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in findings:
        counts[f["priority"]] = counts.get(f["priority"], 0) + 1

    print("=" * 60)
    print("PRIORITY SUMMARY")
    print("=" * 60)
    for level in ("HIGH", "MEDIUM", "LOW"):
        if counts[level]:
            print(f"  {counts[level]:2d}  {level}")
    print(f"  --")
    print(f"  {sum(counts.values()):2d}  Total")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Review a chart specification against Storytelling with Data principles."
    )
    parser.add_argument(
        "spec_file",
        help="Path to a JSON chart specification file.",
    )
    args = parser.parse_args()

    spec_path = pathlib.Path(args.spec_file)
    if not spec_path.exists():
        print(f"ERROR: File not found: {spec_path}")
        sys.exit(1)

    spec = load_spec(spec_path)
    findings = check_spec(spec)
    print_findings(findings)

    has_high = any(f["priority"] == "HIGH" for f in findings)
    sys.exit(2 if has_high else (1 if findings else 0))


if __name__ == "__main__":
    main()
