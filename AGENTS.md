# Agent Integration

How to install and use booklib-ai/skills with different AI coding assistants.

## Claude Code

Install all skills globally:

```bash
npx skills add booklib-ai/skills --all -g
```

Install a single skill:

```bash
npx skills add booklib-ai/skills --skill clean-code-reviewer
```

Skills are placed in `~/.claude/skills/` and available in every project. Claude Code picks them up automatically based on the `description` field in each `SKILL.md`.

To invoke a skill explicitly, use a slash command:

```
/clean-code-reviewer
```

## Cursor

Install skills into your project:

```bash
npx skills add booklib-ai/skills --all
```

Skills are placed in `.claude/skills/` in your project root. Cursor reads these when Agent mode is active.

To trigger a skill, reference it by name in your prompt:

```
Apply the effective-python skill to refactor this module.
```

## GitHub Copilot (VS Code)

Install skills globally:

```bash
npx skills add booklib-ai/skills --all -g
```

In VS Code with Copilot Chat, skills in `~/.claude/skills/` are available as context. Reference them explicitly in chat:

```
Using the design-patterns skill, review this class for pattern opportunities.
```

## Windsurf

Install skills into your project:

```bash
npx skills add booklib-ai/skills --all
```

Skills are placed in `.claude/skills/`. In Windsurf's Cascade mode, you can reference a skill by name in your instructions or let the `skill-router` meta-skill select the right one automatically.

## skill-router — automatic routing

Instead of choosing a skill manually, install the `skill-router` meta-skill and let it pick:

```bash
npx skills add booklib-ai/skills --skill skill-router -g
```

Then prefix any task with:

```
Route this task to the right skill, then apply it: [your request]
```

The router returns a ranked recommendation (primary + optional secondary) and applies it.

## Manual installation

If your agent isn't listed above, copy skills directly:

```bash
# Single skill
cp -r skills/effective-kotlin /path/to/project/.claude/skills/

# All skills
cp -r skills/* /path/to/project/.claude/skills/
```

Any agent that reads `.claude/skills/` will pick them up.

## Supported agents

| Agent | Install path | Auto-trigger | Manual trigger |
|-------|-------------|--------------|----------------|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` | Yes | `/skill-name` |
| Cursor | `.claude/skills/` | Partial | Reference by name |
| GitHub Copilot | `~/.claude/skills/` | No | Reference by name |
| Windsurf | `.claude/skills/` | Partial | Reference by name |

## Requesting support for a new agent

Open an issue titled **"Agent Support: [Agent Name]"** and describe how the agent loads context files. We'll add installation instructions here.
