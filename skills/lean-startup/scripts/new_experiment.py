#!/usr/bin/env python3
"""
Lean Startup — MVP Experiment Document Generator.

Usage (interactive):  python new_experiment.py
Usage (one-shot):     python new_experiment.py --name "X" --hypothesis "Y" \
                        --mvp-type landing-page --metric "signups" \
                        --threshold "100 signups" --duration "2 weeks" \
                        --output experiment.md
"""

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

MVP_TYPES = ["concierge", "wizard-of-oz", "landing-page", "smoke-test"]

MVP_DESCRIPTIONS = {
    "concierge": (
        "Manually deliver the service to early customers without automation. "
        "You act as the 'product' to learn what customers actually want before building."
    ),
    "wizard-of-oz": (
        "Present a working product interface to customers, but fulfil requests manually "
        "behind the scenes. Validates demand without engineering the full solution."
    ),
    "landing-page": (
        "Publish a description and sign-up form for a product that does not yet exist. "
        "Measures intent-to-use at near-zero cost."
    ),
    "smoke-test": (
        "Run a small paid-acquisition experiment (e.g., Google Ads) to a landing page. "
        "Measures real purchase intent before building anything."
    ),
}

WHY_NOT_BUILD = {
    "concierge": (
        "Building the full automated product before understanding the exact workflow "
        "customers need risks expensive re-work. Manual delivery surfaces the real "
        "job-to-be-done faster and cheaper."
    ),
    "wizard-of-oz": (
        "Engineering the back-end automation is costly and time-consuming. "
        "Validating that customers use and value the front-end experience first "
        "eliminates the biggest unknown before we invest in automation."
    ),
    "landing-page": (
        "Writing code for a product nobody wants is pure waste. "
        "A landing page lets us measure whether the value proposition resonates "
        "with the target segment in days, not months."
    ),
    "smoke-test": (
        "Acquiring real paying customers validates both the value hypothesis and "
        "the growth hypothesis simultaneously. Building first would delay this "
        "signal by weeks and obscure whether demand is organic or forced."
    ),
}

PIVOT_OPTIONS = [
    "Zoom-in pivot: narrow scope to the single highest-value feature",
    "Customer-segment pivot: target a different customer segment with the same product",
    "Value-capture pivot: change the monetisation model (subscription vs. one-time)",
    "Channel pivot: switch acquisition channel (e.g., outbound sales → content marketing)",
    "Technology pivot: solve the same problem with a different underlying technology",
    "Platform pivot: move from application to platform or vice versa",
]


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default:
            return default
        print("  (required — please enter a value)")


def prompt_choice(label: str, choices: list[str]) -> str:
    print(f"\n{label}")
    for i, c in enumerate(choices, 1):
        print(f"  {i}. {c}")
    while True:
        raw = input("Enter number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1]
        print(f"  Please enter a number between 1 and {len(choices)}.")


def gather_interactive() -> dict:
    print("\n=== Lean Startup — New MVP Experiment ===\n")
    print("Answer each prompt. Press Enter to accept the default.\n")
    data: dict = {}
    data["name"] = prompt("Product / feature name")
    data["value_hypothesis"] = prompt(
        "Value hypothesis (customers will value X because Y)"
    )
    data["growth_hypothesis"] = prompt(
        "Growth hypothesis (new customers will find us via ...)"
    )
    data["mvp_type"] = prompt_choice("MVP type", MVP_TYPES)
    data["metric"] = prompt("Primary metric to track (e.g., 'weekly active users')")
    data["baseline"] = prompt("Current baseline for this metric (e.g., '0', 'unknown')", "0")
    data["threshold"] = prompt("Success threshold (e.g., '50 sign-ups in 2 weeks')")
    data["duration"] = prompt("Experiment duration (e.g., '2 weeks')", "2 weeks")
    data["team"] = prompt("Team / owner", "Product team")
    return data


def parse_duration_weeks(duration_str: str) -> int:
    """Very simple heuristic: look for a number before 'week'."""
    import re
    m = re.search(r"(\d+)\s*week", duration_str, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*day", duration_str, re.IGNORECASE)
    if m:
        return max(1, int(m.group(1)) // 7)
    return 2  # default


def render_document(data: dict) -> str:
    today = date.today()
    weeks = parse_duration_weeks(data["duration"])
    decision_date = today + timedelta(weeks=weeks)
    mvp_type = data["mvp_type"]

    lines = [
        f"# MVP Experiment: {data['name']}",
        "",
        f"**Date created:** {today}  ",
        f"**Owner:** {data['team']}  ",
        f"**Pivot/Persevere decision by:** {decision_date}  ",
        f"**Duration:** {data['duration']}  ",
        "",
        "---",
        "",
        "## 1. Leap-of-Faith Assumptions",
        "",
        "### Value Hypothesis",
        f"> {data['value_hypothesis']}",
        "",
        "This is the core belief we are testing. If customers do not behave as",
        "predicted, we learn this assumption is false and must pivot.",
        "",
        "### Growth Hypothesis",
        f"> {data['growth_hypothesis']}",
        "",
        "---",
        "",
        "## 2. Why NOT Build the Full Product Yet",
        "",
        WHY_NOT_BUILD[mvp_type],
        "",
        "Building the full solution before validating these assumptions would be",
        "**premature scaling** — one of the most common causes of startup failure",
        "according to the Lean Startup framework.",
        "",
        "---",
        "",
        f"## 3. MVP Design — {mvp_type.replace('-', ' ').title()}",
        "",
        f"**Type:** {mvp_type}",
        "",
        MVP_DESCRIPTIONS[mvp_type],
        "",
        "### What we will build / do",
        "",
        "- [ ] Define the exact customer action we want to observe",
        "- [ ] Set up measurement (analytics, tracking, manual log)",
        "- [ ] Recruit initial participants / drive initial traffic",
        "- [ ] Execute the experiment and collect data",
        "- [ ] Analyse results against the success threshold below",
        "",
        "### What we will NOT build",
        "",
        "- Full back-end automation",
        "- Production-quality UI beyond what is needed to trigger the measured action",
        "- Scalability infrastructure",
        "",
        "---",
        "",
        "## 4. Innovation Accounting",
        "",
        "| Metric | Baseline | Target | How We Measure |",
        "|--------|----------|--------|----------------|",
        f"| {data['metric']} | {data['baseline']} | {data['threshold']} | [instrument] |",
        "| Retention (week 2) | — | >30% | Cohort analysis |",
        "| NPS / qualitative | — | Positive themes | Customer interviews |",
        "",
        "Measurements should be **actionable, accessible, auditable** (Three A's).",
        "Avoid vanity metrics (total page views, total registered users).",
        "",
        "---",
        "",
        "## 5. Pivot / Persevere Criteria",
        "",
        f"**Decision date:** {decision_date}  ",
        f"**Decision owner:** {data['team']}",
        "",
        "### Persevere if",
        f"- The primary metric reaches or exceeds **{data['threshold']}** by {decision_date}.",
        "- Customer interviews reveal consistent, strong pull — not polite feedback.",
        "- At least one customer takes an unexpected high-engagement action.",
        "",
        "### Pivot if",
        f"- The primary metric is below **{data['threshold']}** with no strong upward trend.",
        "- Qualitative feedback reveals the problem is not painful enough to act on.",
        "- A significantly different customer segment shows stronger signal.",
        "",
        "### Pre-populated Pivot Options",
        "",
    ]
    for opt in PIVOT_OPTIONS:
        lines.append(f"- {opt}")

    lines += [
        "",
        "---",
        "",
        "## 6. References",
        "",
        "- Ries, E. (2011). *The Lean Startup*. Crown Business.",
        "- Build-Measure-Learn loop: build the smallest thing that generates the",
        "  most learning, not the smallest shippable product.",
        "",
        "---",
        "",
        "*Generated by `new_experiment.py` — Lean Startup skill.*",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Lean Startup MVP experiment doc.")
    parser.add_argument("--name", help="Product or feature name")
    parser.add_argument("--hypothesis", help="Value hypothesis")
    parser.add_argument("--mvp-type", choices=MVP_TYPES, dest="mvp_type")
    parser.add_argument("--metric", help="Primary metric")
    parser.add_argument("--threshold", help="Success threshold")
    parser.add_argument("--duration", default="2 weeks", help="Experiment duration")
    parser.add_argument("--output", type=Path, help="Output file (default: stdout)")
    args = parser.parse_args()

    # Determine mode: fully specified vs interactive
    required = ["name", "hypothesis", "mvp_type", "metric", "threshold"]
    if all(getattr(args, f.replace("-", "_"), None) for f in required):
        data = {
            "name": args.name,
            "value_hypothesis": args.hypothesis,
            "growth_hypothesis": "To be determined after initial validation.",
            "mvp_type": args.mvp_type,
            "metric": args.metric,
            "baseline": "0",
            "threshold": args.threshold,
            "duration": args.duration,
            "team": "Product team",
        }
    else:
        if any(getattr(args, f.replace("-", "_"), None) for f in required):
            print(
                "WARNING: Some flags provided but not all required flags are set. "
                "Falling back to interactive mode.",
                file=sys.stderr,
            )
        try:
            data = gather_interactive()
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.", file=sys.stderr)
            sys.exit(1)

    document = render_document(data)

    if args.output:
        args.output.write_text(document)
        print(f"\nExperiment document written to: {args.output}")
        print(f"Next: schedule the pivot/persevere meeting for the decision date shown in the doc.")
    else:
        sys.stdout.write(document)


if __name__ == "__main__":
    main()
