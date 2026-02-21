# Skill Quality Checklist

A reference for evaluating skill completeness. Skills earn badges based on how many criteria they meet.

---

## Badges

| Badge | Level | Criteria |
|-------|-------|----------|
| 🥉 Bronze | Functional | Valid SKILL.md — agent can use it |
| 🥈 Silver | Complete | + examples showing real value |
| 🥇 Gold | Polished | + evals proving it works + references for depth |
| 💎 Platinum | Exemplary | + scripts automating repetitive tasks |

---

## Full Checklist

### 🥉 Bronze — Functional

A skill an agent can reliably trigger and use.

- [ ] **Folder name** matches `name` field in SKILL.md exactly (lowercase, hyphens only)
- [ ] **`name`** is 1–64 characters, no consecutive hyphens, no leading/trailing hyphens
- [ ] **`description`** is 1–1024 characters and non-empty
- [ ] **Description triggers** — includes specific keywords/phrases agents should match (e.g. "Effective Kotlin", "Kotlin best practice", "Kotlin review")
- [ ] **Description scope** — says both *what* the skill does and *when* to use it
- [ ] **Body is actionable** — SKILL.md gives the agent concrete steps to follow, not just a book summary
- [ ] **SKILL.md under 500 lines** — longer content moved to `references/`

### 🥈 Silver — Complete

A skill that convincingly demonstrates its value.

- [ ] **`examples/before.md`** — realistic code or artifact that violates the skill's principles (10+ lines, real domain context)
- [ ] **`examples/after.md`** — the same thing improved, with a "Key improvements" section citing specific principles
- [ ] **Examples are domain-realistic** — not toy examples (`foo`, `bar`); uses real variable names and scenarios
- [ ] **Before/after difference is clear** — a reader immediately sees why the after is better

### 🥇 Gold — Polished

A skill that has been validated and provides deep reference material.

- [ ] **`evals/evals.json`** — at least 3 test cases
- [ ] **Eval coverage** — includes: (1) clear violation, (2) subtle/intermediate case, (3) already-good code the agent should recognize and not nitpick
- [ ] **Eval expectations are specific** — e.g. "flags the use of `var` where `val` would work", not "gives good advice"
- [ ] **Eval prompts include real code** — 10–25 lines of concrete code or text in each prompt
- [ ] **`references/review-checklist.md`** — systematic checklist organized by book structure
- [ ] **`references/practices-catalog.md`** — all key patterns with Problem / Solution / Key rules
- [ ] **`references/api_reference.md`** — quick-lookup tables (heuristic codes, item numbers, pattern names)
- [ ] **SKILL.md links to references** — body mentions the reference files so agents know to load them

### 💎 Platinum — Exemplary

A skill that automates repetitive work.

- [ ] **`scripts/`** — at least one executable script that saves real time (linting, formatting, report generation, scaffolding)
- [ ] **Scripts are self-contained** — document their dependencies; handle errors gracefully
- [ ] **Scripts are referenced from SKILL.md** — agent knows when and how to run them
- [ ] **`assets/`** — templates, config files, or diagrams that support the skill's workflow

---

## Current Status

| Skill | 🥉 | 🥈 | 🥇 | 💎 |
|-------|----|----|----|----|
| animation-at-work | ✅ | ✅ | ✅ | — |
| clean-code-reviewer | ✅ | ✅ | ✅ | — |
| data-intensive-patterns | ✅ | ✅ | ✅ | — |
| data-pipelines | ✅ | ✅ | ✅ | — |
| design-patterns | ✅ | ✅ | ✅ | — |
| domain-driven-design | ✅ | ✅ | ✅ | — |
| effective-java | ✅ | ✅ | ✅ | — |
| effective-kotlin | ✅ | ✅ | ✅ | ✅ |
| effective-python | ✅ | ✅ | ✅ | — |
| kotlin-in-action | ✅ | ✅ | ✅ | — |
| lean-startup | ✅ | ✅ | ✅ | — |
| microservices-patterns | ✅ | ✅ | ✅ | — |
| refactoring-ui | ✅ | ✅ | ✅ | — |
| storytelling-with-data | ✅ | ✅ | ✅ | — |
| system-design-interview | ✅ | ✅ | ✅ | — |
| using-asyncio-python | ✅ | ✅ | ✅ | — |
| web-scraping-python | ✅ | ✅ | ✅ | — |

---

## For contributors

When submitting a new skill, aim for at least 🥈 Silver before opening a PR. Gold is the target for skills that cover deep technical books with many specific rules. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a skill.
