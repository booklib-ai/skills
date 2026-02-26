#!/usr/bin/env python3
"""
adr.py - Architecture Decision Record generator for data-intensive systems.

Usage:
    python adr.py <decision-title>
    python adr.py                    # interactive mode

Generates:
    adr-NNN-<slug>.md   - Numbered ADR file with data-intensive-specific sections
    ADR-INDEX.md        - Running index of all ADRs (appended to)

The ADR includes standard sections plus four data-intensive-specific sections:
    - Consistency model
    - Failure mode
    - Scalability impact
    - Operability

Based on patterns from "Designing Data-Intensive Applications" by Martin Kleppmann.
"""

import argparse
import datetime
import pathlib
import re
import sys


def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def next_adr_number(adr_dir: pathlib.Path) -> int:
    existing = list(adr_dir.glob("adr-[0-9][0-9][0-9]-*.md"))
    if not existing:
        return 1
    numbers = []
    for p in existing:
        m = re.match(r"adr-(\d{3})-", p.name)
        if m:
            numbers.append(int(m.group(1)))
    return max(numbers) + 1 if numbers else 1


def prompt(question: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        answer = input(f"{question}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    return answer if answer else default


def collect_options() -> list[str]:
    options = []
    print("Enter up to 4 considered options (leave blank to stop):")
    for i in range(1, 5):
        opt = prompt(f"  Option {i}")
        if not opt:
            break
        options.append(opt)
    return options


def render_adr(
    number: int,
    title: str,
    context: str,
    options: list[str],
    chosen: str,
    consequences: str,
    consistency_model: str,
    failure_mode: str,
    scalability_impact: str,
    operability: str,
    date: str,
) -> str:
    options_text = "\n".join(f"- {opt}" for opt in options) if options else "- (none listed)"
    return f"""\
# ADR-{number:03d}: {title}

**Date:** {date}
**Status:** Proposed

---

## Context

{context}

## Considered Options

{options_text}

## Decision

{chosen}

## Consequences

{consequences}

---

## Data-Intensive Considerations

### Consistency Model

> What consistency guarantees does this choice provide?

{consistency_model}

### Failure Mode

> What happens when this component fails?

{failure_mode}

### Scalability Impact

> How does this scale with data volume?

{scalability_impact}

### Operability

> How observable and maintainable is this choice?

{operability}
"""


def append_to_index(index_path: pathlib.Path, number: int, title: str, filename: str, date: str) -> None:
    header = "# ADR Index\n\n| # | Title | Date | File |\n|---|-------|------|------|\n"
    entry = f"| {number:03d} | {title} | {date} | [{filename}]({filename}) |\n"
    if not index_path.exists():
        index_path.write_text(header + entry, encoding="utf-8")
        print(f"Created: {index_path}")
    else:
        content = index_path.read_text(encoding="utf-8")
        index_path.write_text(content + entry, encoding="utf-8")
        print(f"Updated: {index_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an ADR for data-intensive systems."
    )
    parser.add_argument(
        "title",
        nargs="?",
        default="",
        help="Decision title (will prompt if omitted)",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to write ADR files (default: ./)",
    )
    args = parser.parse_args()

    output_dir = pathlib.Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    title = args.title.strip() or prompt("Decision title")
    if not title:
        print("ERROR: A title is required.")
        sys.exit(1)

    print()
    context = prompt("Context (why is this decision needed?)", default="Describe the situation and forces at play.")
    options = collect_options()
    chosen = prompt("Chosen option")
    consequences = prompt("Consequences (trade-offs, risks, next steps)", default="To be determined.")
    print()
    print("-- Data-intensive sections --")
    consistency_model = prompt("Consistency model", default="To be defined.")
    failure_mode = prompt("Failure mode", default="To be defined.")
    scalability_impact = prompt("Scalability impact", default="To be defined.")
    operability = prompt("Operability", default="To be defined.")

    number = next_adr_number(output_dir)
    date = datetime.date.today().isoformat()
    filename = f"adr-{number:03d}-{slugify(title)}.md"
    adr_path = output_dir / filename

    content = render_adr(
        number=number,
        title=title,
        context=context,
        options=options,
        chosen=chosen,
        consequences=consequences,
        consistency_model=consistency_model,
        failure_mode=failure_mode,
        scalability_impact=scalability_impact,
        operability=operability,
        date=date,
    )

    adr_path.write_text(content, encoding="utf-8")
    print(f"\nWrote: {adr_path}")

    append_to_index(output_dir / "ADR-INDEX.md", number, title, filename, date)
    print("\nDone.")


if __name__ == "__main__":
    main()
