# Claude Skills

A personal collection of [Claude Code](https://claude.com/claude-code) skills,
kept in git so they sync across machines. Each skill is a self-contained folder
under `skills/`; Claude loads it automatically when a task matches its description.

## Skills

| Skill | What it does |
|-------|--------------|
| **fable-advisor** | Cost-aware work router: routes a task to the cheapest adequate destination (just-do-it / `advisor` / NotebookLM / spawn Fable 5) and the cheapest adequate model (haiku/sonnet/opus/fable), so Fable quota and tokens are spent only where they buy something. |
| **design-extract** (`/extract`) | Extract a comprehensive design system (tokens, components, layout) from any website via agent-browser. |
| **drawio-swimlane** | Author, clean up, and review draw.io swimlane / cross-functional flowcharts to a professional standard, with a scripted layout gate. |
| **thai-docx** | Fix broken Thai rendering in Word `.docx` files generated with python-docx (fonts, tone marks, bold/italic, justification). |
| **postgres-drizzle** | PostgreSQL + Drizzle ORM best practices (schemas, migrations, indexes, queries). Vendored — tracked in `skills-lock.json`. |

## Using them

Point Claude Code at these skills by symlinking or copying `skills/*` into your
skills directory (e.g. `~/.claude/skills/`), or load this repo as a skills source.
Once available, they trigger on intent — no need to invoke by name (though the
slash forms like `/extract` and `/fable-advisor` work too).

`skills-lock.json` records vendored skills pulled from external sources; update
them with your skills manager.

MIT License · [GitHub](https://github.com/ChampPABA/claude-multi-agent-template)
