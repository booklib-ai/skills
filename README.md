# 🧠 Skills

Book knowledge distilled into structured AI skills — each skill packages expert practices from a specific book into a reusable prompt that AI agents can apply to code generation, code review, and design decisions.

Each skill is a self-contained folder with a `SKILL.md` file containing instructions and metadata that AI agents use to perform specialized tasks.

## Structure

```
skills/
├── README.md
├── LICENSE
├── clean-code-reviewer/          # Code review using Clean Code principles
│   ├── SKILL.md
│   └── evals/
│       └── evals.json
├── [future-skill]/
│   ├── SKILL.md
│   ├── scripts/                  # Executable code (Python/Bash)
│   ├── references/               # Documentation loaded into context as needed
│   ├── assets/                   # Templates, icons, fonts
│   └── evals/                    # Test cases for the skill
│       ├── evals.json
│       └── files/                # Input files for evals
└── ...
```

## Skill Format

Each skill follows the [Agent Skills standard](https://agentskills.io):

```
skill-name/
├── SKILL.md          # Required — YAML frontmatter + markdown instructions
├── scripts/          # Optional — deterministic code for repeated tasks
├── references/       # Optional — docs loaded into context as needed
├── assets/           # Optional — templates, fonts, images
└── evals/            # Optional — test cases for skill evaluation
```

### SKILL.md Structure

```markdown
---
name: skill-name
description: When to trigger this skill and what it does
---

# Skill Title

Instructions for the AI agent...
```

## Installation

### via npm (recommended)

```bash
# Add a single skill to your current project
npx @booklib/skills add effective-kotlin

# Add all skills to your current project
npx @booklib/skills add --all

# Add globally (available in all projects)
npx @booklib/skills add --all --global

# List available skills
npx @booklib/skills list
```

Skills are installed to `.claude/skills/` in your project (or `~/.claude/skills/` with `--global`).

### Manual

```bash
# Clone and copy a skill directly
git clone https://github.com/ZLStas/skills.git
cp -r skills/effective-kotlin /path/to/project/.claude/skills/
```

## Skills

| Skill | Description |
|-------|-------------|
| [animation-at-work](./animation-at-work/) | Apply web animation principles from Rachel Nabors' *Animation at Work* — human perception of motion, 12 principles of animation, and performance |
| [clean-code-reviewer](./clean-code-reviewer/) | Reviews code against Robert C. Martin's *Clean Code* principles with heuristic codes (C1–C5, G1–G36, N1–N7, T1–T9) |
| [data-intensive-patterns](./data-intensive-patterns/) | Patterns for reliable, scalable, and maintainable systems from Martin Kleppmann's *Designing Data-Intensive Applications* — storage engines, replication, partitioning, and transactions |
| [data-pipelines](./data-pipelines/) | Data pipeline practices from James Densmore's *Data Pipelines Pocket Reference* — ingestion, streaming, transformation, and orchestration |
| [design-patterns](./design-patterns/) | Apply and review GoF design patterns from *Head First Design Patterns* — creational, structural, and behavioral patterns |
| [domain-driven-design](./domain-driven-design/) | Design and review software using patterns from Eric Evans' *Domain-Driven Design* — tactical and strategic patterns, and Ubiquitous Language |
| [effective-java](./effective-java/) | Java best practices from Joshua Bloch's *Effective Java* (3rd Edition) — object creation, generics, enums, lambdas, and concurrency |
| [effective-kotlin](./effective-kotlin/) | Best practices from Marcin Moskała's *Effective Kotlin* (2nd Ed) — safety, readability, reusability, and abstraction |
| [kotlin-in-action](./kotlin-in-action/) | Practices from *Kotlin in Action* (2nd Ed) — functions, classes, lambdas, nullability, and coroutines |
| [lean-startup](./lean-startup/) | Practices from Eric Ries' *The Lean Startup* — MVP testing, validated learning, Build-Measure-Learn loop, and pivots |
| [microservices-patterns](./microservices-patterns/) | Expert guidance on microservices patterns from Chris Richardson's *Microservices Patterns* — decomposition, sagas, API gateways, event sourcing, CQRS, and service mesh |
| [refactoring-ui](./refactoring-ui/) | UI design principles from *Refactoring UI* by Adam Wathan & Steve Schoger — visual hierarchy, layout, typography, and color |
| [storytelling-with-data](./storytelling-with-data/) | Data visualization and storytelling from Cole Nussbaumer Knaflic's *Storytelling with Data* — effective visuals, decluttering, and narrative structure |
| [system-design-interview](./system-design-interview/) | System design principles from Alex Xu's *System Design Interview* — scaling, estimation, and real-world system designs |
| [using-asyncio-python](./using-asyncio-python/) | Asyncio practices from Caleb Hattingh's *Using Asyncio in Python* — coroutines, event loop, tasks, and signal handling |
| [web-scraping-python](./web-scraping-python/) | Web scraping practices from Ryan Mitchell's *Web Scraping with Python* — BeautifulSoup, Scrapy, and data storage |

## License

MIT
