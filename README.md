# 🧠 Skills

Personal collection of custom AI agent skills for Claude, Codex, and other AI assistants.

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

## Usage

### Claude (claude.ai / Claude Desktop)
Upload skill folders to your project or reference them in your workspace.

### Claude Code
```bash
# Copy skills to your project
cp -r skills/clean-code-reviewer /path/to/project/.claude/skills/
```

### Codex CLI
```bash
# Copy to Codex skills directory
cp -r skills/clean-code-reviewer ~/.codex/skills/
```

## Skills

| Skill | Description |
|-------|-------------|
| [clean-code-reviewer](./clean-code-reviewer/) | Reviews code against Robert C. Martin's *Clean Code* principles with heuristic codes (C1–C5, G1–G36, N1–N7, T1–T9) |

## License

MIT