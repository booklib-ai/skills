# Contributing

Thanks for wanting to add a skill. A skill packages expert knowledge from a book into reusable instructions that AI agents can apply to real tasks.

## What makes a good skill?

A skill is worth adding when the source book:
- Contains specific, actionable advice (not just general philosophy)
- Covers a topic useful to software engineers or designers
- Has enough depth to fill a meaningful SKILL.md (300+ lines)

## Adding a new skill

### 1. Create the folder

```
skill-name/
├── SKILL.md          # Required
├── examples/
│   ├── before.md     # Code or artifact before applying the skill
│   └── after.md      # The improved version
└── evals/
    └── evals.json    # Test cases
```

The folder name must be lowercase, hyphen-separated, and match the `name` field in `SKILL.md` exactly.

### 2. Write SKILL.md

```markdown
---
name: skill-name
description: >
  What this skill does and when to trigger it. Include specific
  keywords agents should look for. Max 1024 characters.
---

# Skill Title

You are an expert in [domain] grounded in [Book Title] by [Author].

## When to use this skill

[Describe trigger conditions — what user requests or code patterns activate this skill]

## Core principles

[The key ideas from the book, organized for an AI agent to apply]

## How to apply

[Step-by-step process the agent follows]

## Examples

[At least one concrete before/after showing the skill in action]
```

**Requirements:**
- `name`: lowercase letters and hyphens only, matches folder name
- `description`: 1–1024 characters, describes what it does AND when to use it
- Body: clear instructions an AI agent can follow immediately

**Keep SKILL.md under 500 lines.** Move deep reference material to `references/` and link to it.

### 3. Add before/after examples

`examples/before.md` — code or artifact that violates the book's principles.
`examples/after.md` — the same thing improved by applying the skill.

These power the `npx @booklib/skills demo <name>` command.

### 4. Add evals

`evals/evals.json` — array of test cases verifying the skill works:

```json
{
  "evals": [
    {
      "id": "eval-01-short-description",
      "prompt": "The prompt to send to the agent (include code or a scenario)",
      "expectations": [
        "The agent should do X",
        "The agent should flag Y",
        "The agent should NOT do Z"
      ]
    }
  ]
}
```

Aim for 3–5 evals per skill covering:
1. A clear violation of the book's principles
2. A subtle or intermediate case
3. Already-good code (the agent should recognize it and not manufacture issues)

### 5. Submit a PR

```bash
git checkout -b skill/book-name
# add your skill folder
git add skill-name/
git commit -m "feat: add skill-name skill"
gh pr create --title "feat: add skill-name" --body "..."
```

PR checklist:
- [ ] Folder name matches `name` in SKILL.md
- [ ] `description` is under 1024 characters
- [ ] SKILL.md is under 500 lines
- [ ] `examples/before.md` and `examples/after.md` exist
- [ ] `evals/evals.json` has at least 3 test cases
- [ ] README.md skills table updated

## Requesting a skill

Open an issue titled **"Skill Request: [Book Name]"** and describe why the book would make a good skill. Community members can then pick it up.

## Questions

Use [GitHub Discussions](../../discussions) for questions, ideas, and feedback.
