# hubspot-agent-kit

HubSpot operator skill pack for AI agents. Covers workflow auditing,
deal operations, UTM normalization, CRM hygiene, and more.

## Directory Layout

```
skills/       10 SKILL.md files — one per operation domain
rules/        38 audit rules (rules/INDEX.md is the master table)
scripts/      Python utilities (audit, workflows, processing)
templates/    Workflow JSON templates for common patterns
docs/         API reference, workflow patterns, data models, security
agents/       3 specialist subagent definitions
```

## Behavior Contract

- Before any HubSpot task: read the relevant `skills/*/SKILL.md`
- Before any API call: check `docs/api-reference.md` for the correct endpoint and auth
- Before any workflow change: run `scripts/audit/audit_workflows.py` first
- Default `DRY_RUN=true` — never write to HubSpot without explicit user confirmation
- State findings as facts. Say UNKNOWN rather than guessing.
- Never log or echo `HUBSPOT_API_KEY` in output

## Skills

| Slash Command | Skill File | What It Does |
|---|---|---|
| `/hs-audit` | `skills/workflow-audit/SKILL.md` | Audit all workflows against 38 rules |
| `/hs-build` | `skills/workflow-build/SKILL.md` | Build and deploy workflows via API v4 |
| `/hs-deals` | `skills/deal-operations/SKILL.md` | Create, associate, and move deals |
| `/hs-meetings` | `skills/meeting-operations/SKILL.md` | Activity types, outcomes, governance |
| `/hs-utm` | `skills/utm-operations/SKILL.md` | UTM normalization and backfill |
| `/hs-crm` | `skills/crm-audit/SKILL.md` | Orphans, missing associations, hygiene |
| `/hs-calls` | `skills/call-routing/SKILL.md` | Disposition routing and lead status |
| `/hs-pages` | `skills/landing-pages/SKILL.md` | Download, edit, and publish pages |
| `/hs-normalize` | `skills/lead-normalization/SKILL.md` | Bulk contact property normalization |
| `/hs-hygiene` | `skills/data-hygiene/SKILL.md` | Ghost deals, stale contacts, duplicates |

## Specialist Agents

| Agent | File | Role |
|---|---|---|
| hubspot-auditor | `agents/hubspot-auditor.md` | Read-only portal analysis — never writes |
| hubspot-builder | `agents/hubspot-builder.md` | Workflow creation and deployment |
| hubspot-analyst | `agents/hubspot-analyst.md` | CRM queries and reporting |

## Key Audit Rules

See `rules/INDEX.md` for all 38. The highest-impact ones:

| ID | Severity | Name |
|---|---|---|
| WF-005 | CRITICAL | Circular enrollment loop |
| WF-006 | CRITICAL | Lifecycle stage downgrade |
| WF-016 | CRITICAL | Object type / flow type mismatch |
| WF-002 | HIGH | Broken property reference |
| WF-018 | HIGH | Meeting deal missing activity type filter |
| WF-019 | HIGH | Missing deal creation associations |

## Environment Variables

```
HUBSPOT_API_KEY       Required. HubSpot Private App token.
HUBSPOT_PORTAL_ID     Required for portal-scoped operations.
HUBSPOT_BASE_URL      Default: https://api.hubapi.com
DRY_RUN               Default: true. Set false only to write live.
DISABLE_SSL_VERIFY    Default: false. Windows dev only — never true in production.
```
