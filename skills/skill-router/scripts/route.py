#!/usr/bin/env python3
"""
route.py — CLI for skill-router

Usage:
    python route.py --task "review my Python class for code quality"
    python route.py --file path/to/file.py --task "review for correctness"
    python route.py --task "design a saga for order processing"
    python route.py --task "decompose my monolith into microservices"

Prints the recommended skill(s) with rationale.
"""

import argparse
import os

# Skill routing rules
SKILL_CATALOG = {
    "animation-at-work": {
        "domain": "Web animation, UI motion",
        "languages": [],  # language-agnostic but frontend
        "keywords": ["animation", "motion", "transition", "keyframe", "easing", "css animation", "web animation"],
        "anti_keywords": ["backend", "data processing", "api"],
    },
    "clean-code-reviewer": {
        "domain": "Code quality, readability (any language)",
        "languages": ["py", "java", "kt", "js", "ts", "go", "rs", "cpp", "cs"],
        "keywords": ["review", "code quality", "readable", "clean", "refactor", "naming", "smell", "heuristic"],
        "anti_keywords": ["architecture", "system design"],
    },
    "data-intensive-patterns": {
        "domain": "Storage internals, distributed data",
        "languages": [],
        "keywords": ["replication", "partitioning", "consistency", "cap theorem", "storage engine", "lsm", "b-tree", "acid", "base", "linearizability"],
        "anti_keywords": ["ui", "frontend", "domain model"],
    },
    "data-pipelines": {
        "domain": "ETL, data ingestion, orchestration",
        "languages": ["py", "sql"],
        "keywords": ["data pipeline", "etl", "elt", "ingestion", "airflow", "dbt", "spark", "streaming", "batch", "warehouse"],
        "anti_keywords": ["microservice", "ui"],
    },
    "design-patterns": {
        "domain": "GoF OO design patterns",
        "languages": ["java", "py", "kt", "cs"],
        "keywords": ["design pattern", "factory", "singleton", "observer", "strategy", "decorator", "facade", "command", "template method", "composite"],
        "anti_keywords": ["functional", "microservice decomposition"],
    },
    "domain-driven-design": {
        "domain": "Domain modeling, DDD tactical and strategic patterns",
        "languages": [],
        "keywords": ["ddd", "domain model", "aggregate", "value object", "bounded context", "ubiquitous language", "repository", "domain service", "anticorruption", "entity", "anemic"],
        "anti_keywords": ["simple crud", "ui", "code quality"],
    },
    "effective-java": {
        "domain": "Java best practices",
        "languages": ["java"],
        "keywords": ["java", "generics", "enum", "lambda", "stream", "builder pattern", "serialization", "checked exception"],
        "anti_keywords": [],
    },
    "effective-kotlin": {
        "domain": "Kotlin best practices",
        "languages": ["kt"],
        "keywords": ["kotlin", "kotlin best practices", "kotlin safety", "null safety", "kotlin idioms", "effective kotlin", "best practices"],
        "anti_keywords": ["learning kotlin"],
    },
    "effective-python": {
        "domain": "Python idioms and best practices",
        "languages": ["py"],
        "keywords": ["pythonic", "python best practices", "comprehension", "generator", "decorator", "metaclass"],
        "anti_keywords": ["async", "asyncio", "web scraping"],
    },
    "kotlin-in-action": {
        "domain": "Kotlin language features",
        "languages": ["kt"],
        "keywords": ["learn kotlin", "kotlin coroutines", "kotlin lambdas", "kotlin classes", "how does kotlin"],
        "anti_keywords": ["best practices"],
    },
    "lean-startup": {
        "domain": "Startup strategy, MVP, validated learning",
        "languages": [],
        "keywords": ["mvp", "validated learning", "pivot", "build-measure-learn", "lean startup", "hypothesis", "product market fit"],
        "anti_keywords": ["code", "review", "architecture", "api"],
    },
    "microservices-patterns": {
        "domain": "Service decomposition, sagas, CQRS, event sourcing",
        "languages": [],
        "keywords": ["microservice", "services", "saga", "cqrs", "event sourcing", "api gateway", "decompose monolith", "circuit breaker", "distributed transaction", "choreography", "service coordination", "inter-service", "strangle", "strangler"],
        "anti_keywords": ["monolith only", "simple crud"],
    },
    "refactoring-ui": {
        "domain": "UI design, visual hierarchy, typography",
        "languages": ["css", "html", "jsx", "tsx", "svelte"],
        "keywords": ["ui design", "visual hierarchy", "typography", "color", "spacing", "layout", "design system"],
        "anti_keywords": ["backend", "api", "animation"],
    },
    "storytelling-with-data": {
        "domain": "Data visualization, charts, narrative",
        "languages": [],
        "keywords": ["data visualization", "chart", "graph", "dashboard", "storytelling", "declutter", "bar chart", "scatter plot"],
        "anti_keywords": ["backend", "api", "code quality"],
    },
    "system-design-interview": {
        "domain": "System scalability, high-level architecture",
        "languages": [],
        "keywords": ["system design", "scale", "scalability", "rate limiting", "cdn", "load balancer", "cache", "sharding", "high availability"],
        "anti_keywords": ["code review", "domain model"],
    },
    "using-asyncio-python": {
        "domain": "Python asyncio, concurrency",
        "languages": ["py"],
        "keywords": ["asyncio", "async def", "await", "coroutine", "event loop", "aiohttp", "async python", "concurrent python"],
        "anti_keywords": [],
    },
    "web-scraping-python": {
        "domain": "Web scraping, crawling",
        "languages": ["py"],
        "keywords": ["web scraping", "beautifulsoup", "scrapy", "crawl", "parse html", "selenium scraping"],
        "anti_keywords": [],
    },
}

CONFLICT_RULES = [
    ("effective-python", "using-asyncio-python", "using-asyncio-python wins for async topics"),
    ("kotlin-in-action", "effective-kotlin", "effective-kotlin wins for best practice advice"),
    ("clean-code-reviewer", "effective-java", "effective-java wins for Java-specific items; use both for comprehensive review"),
]


def detect_language(file_path: str | None) -> str | None:
    """Detect language from file extension."""
    if not file_path:
        return None
    ext = os.path.splitext(file_path)[1].lstrip(".")
    return ext.lower() if ext else None


def score_skill(skill_name: str, skill_info: dict, task: str, language: str | None) -> float:
    """Score a skill's relevance for a task. Higher = more relevant."""
    task_lower = task.lower()
    score = 0.0

    # Keyword matching
    for keyword in skill_info["keywords"]:
        if keyword in task_lower:
            score += 2.0

    # Anti-keyword penalty
    for anti_keyword in skill_info["anti_keywords"]:
        if anti_keyword in task_lower:
            score -= 3.0

    # Language match bonus
    if language and language in skill_info["languages"]:
        score += 3.0
    elif skill_info["languages"] and language and language not in skill_info["languages"]:
        score -= 5.0  # Strong penalty for language mismatch

    return score


def route(task: str, file_path: str | None = None) -> dict:
    """Route a task to the best skill(s)."""
    language = detect_language(file_path)
    task_lower = task.lower()

    scores = {}
    keyword_hits = {}
    for skill_name, skill_info in SKILL_CATALOG.items():
        scores[skill_name] = score_skill(skill_name, skill_info, task, language)
        keyword_hits[skill_name] = any(kw in task_lower for kw in skill_info["keywords"])

    # Sort by score, descending
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Require positive score AND at least one keyword hit to prevent
    # language-match-only false positives (e.g. data-pipelines for any .py file)
    candidates = [(name, score) for name, score in ranked if score > 0 and keyword_hits[name]]

    if not candidates:
        return {
            "primary": None,
            "secondary": None,
            "dont_apply": None,
            "conflict_note": None,
            "language_detected": language,
            "rationale": "No skill matched. Try describing the task with more domain keywords, or browse the skill catalog.",
        }

    primary_name, _ = candidates[0]
    secondary = candidates[1] if len(candidates) > 1 else None
    dont_apply = candidates[2] if len(candidates) > 2 else None

    # Apply conflict resolution
    conflict_note = None
    if secondary:
        for skill_a, skill_b, note in CONFLICT_RULES:
            if (primary_name == skill_a and secondary[0] == skill_b) or \
               (primary_name == skill_b and secondary[0] == skill_a):
                conflict_note = note
                break

    return {
        "primary": primary_name,
        "primary_domain": SKILL_CATALOG[primary_name]["domain"],
        "secondary": secondary[0] if secondary else None,
        "secondary_domain": SKILL_CATALOG[secondary[0]]["domain"] if secondary else None,
        "dont_apply": dont_apply[0] if dont_apply else None,
        "dont_apply_domain": SKILL_CATALOG[dont_apply[0]]["domain"] if dont_apply else None,
        "conflict_note": conflict_note,
        "language_detected": language,
    }


def format_output(result: dict) -> str:
    """Format routing result for CLI output."""
    lines = []

    if result.get("language_detected"):
        lines.append(f"Detected language: .{result['language_detected']}")
        lines.append("")

    if not result["primary"]:
        lines.append("No matching skill found.")
        lines.append(result.get("rationale", ""))
        return "\n".join(lines)

    lines.append(f"**Primary skill:** `{result['primary']}`")
    lines.append(f"**Why:** {result['primary_domain']}")

    if result["secondary"]:
        lines.append(f"**Secondary (optional):** `{result['secondary']}` — {result['secondary_domain']}")
    else:
        lines.append("**Secondary (optional):** none")

    if result.get("dont_apply"):
        lines.append(f"**Don't apply:** `{result['dont_apply']}` — {result['dont_apply_domain']} (lower relevance for this task)")

    if result.get("conflict_note"):
        lines.append(f"**Conflict resolution:** {result['conflict_note']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Route a task to the best @booklib/skills skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  python route.py --task "review my Python class for code quality"
  python route.py --file app/orders.py --task "review for correctness"
  python route.py --task "design a saga for order processing"
  python route.py --task "decompose my monolith into microservices"
  python route.py --task "my bar chart is too cluttered"
        """,
    )
    parser.add_argument("--file", help="Path to the file being reviewed (used for language detection)")
    parser.add_argument("--task", required=True, help="Description of the task or question")
    args = parser.parse_args()

    result = route(task=args.task, file_path=args.file)
    print(format_output(result))


if __name__ == "__main__":
    main()
