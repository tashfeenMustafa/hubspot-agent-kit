# hubspot-agent-kit — Codex Agent Instructions

HubSpot operator skill pack. Read `CLAUDE.md` for full context.

## Rules

- Read the relevant `skills/*/SKILL.md` before any HubSpot operation
- Check `docs/api-reference.md` before making API calls
- Run `scripts/audit/audit_workflows.py` before modifying workflows
- `DRY_RUN=true` is the default — never write without explicit confirmation
- Scripts are Python 3.8+ using `requests` and `python-dotenv`
- Never output `HUBSPOT_API_KEY` in any response

## Skills

| Command | Skill |
|---|---|
| `/hs-audit` | `skills/workflow-audit/SKILL.md` |
| `/hs-build` | `skills/workflow-build/SKILL.md` |
| `/hs-deals` | `skills/deal-operations/SKILL.md` |
| `/hs-meetings` | `skills/meeting-operations/SKILL.md` |
| `/hs-utm` | `skills/utm-operations/SKILL.md` |
| `/hs-crm` | `skills/crm-audit/SKILL.md` |
| `/hs-calls` | `skills/call-routing/SKILL.md` |
| `/hs-pages` | `skills/landing-pages/SKILL.md` |
| `/hs-normalize` | `skills/lead-normalization/SKILL.md` |
| `/hs-hygiene` | `skills/data-hygiene/SKILL.md` |

## Reference

- `rules/INDEX.md` — 38 workflow audit rules
- `docs/api-reference.md` — HubSpot API endpoints and auth
- `docs/workflow-patterns.md` — proven automation patterns
- `docs/data-models.md` — CRM object schemas
