# Plan: Consolidate Agent Context Files (CLAUDE.md / AGENTS.md / GEMINI.md)

**Date:** 2026-05-28  
**Status:** Ready to execute

---

## What Happened

The original subagent created a `CLAUDE.md` that was:
- Just a flat list of slash commands (same info already in README)
- Not teaching Claude anything it couldn't read from the skills themselves
- Missing the structural context an agent actually needs to operate the kit

When the user flagged it, I proposed deletion and they confirmed — but the right action
was consolidation into something genuinely useful. The file was deleted instead of fixed.

`AGENTS.md` and `GEMINI.md` have the same problem: they're thin duplicates of the README
command table, not real agent context files.

---

## Goal

Restore `CLAUDE.md` and rewrite all three context files so they are:
1. **Non-redundant** — each file has a specific purpose and audience
2. **Substantive** — actually teach the agent how the kit is structured and how to use it
3. **Consolidated** — no copy-pasted content across files; shared content lives in one place
   and the others reference it

---

## Proposed Structure

### CLAUDE.md (primary, most detailed)
This is read by Claude Code and any agent that respects `CLAUDE.md`. It should:
- State the kit's purpose in 2 sentences
- Explain the directory structure so the agent knows where to look
- Define the behavior contract:
  - Always read the relevant `SKILL.md` before touching HubSpot
  - Never call HubSpot API without reading `docs/api-reference.md` first
  - Default `DRY_RUN=true` — never write without explicit confirmation
  - Run `audit_workflows.py` before making workflow changes
  - Check `rules/INDEX.md` to understand what can go wrong
- List the 10 skills with a one-liner description each
- List the 3 agents and when to invoke them
- Point to `docs/` for deep reference
- Point to `scripts/` for runnable utilities

### AGENTS.md (Codex/OpenAI, lean version)
Codex reads this. It should:
- Be a condensed version of CLAUDE.md (Codex prompts are shorter/more directive)
- Same behavior contract, fewer words
- Explicitly state: "Skills are in `skills/` — read SKILL.md before acting"
- Note: scripts use Python + dotenv, not Node

### GEMINI.md (Gemini CLI, lean version)
Gemini reads this. Should mirror AGENTS.md in length and tone.
No copy-pasting the full skill list — just the contract and a pointer.

---

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `CLAUDE.md` | Create (restore + rewrite) | Full substantive version |
| `AGENTS.md` | Rewrite | Condensed, Codex-appropriate |
| `GEMINI.md` | Rewrite | Condensed, Gemini-appropriate |
| `README.md` | Minor update | The "paste this into CLAUDE.md" snippet in README should be removed or simplified — the real CLAUDE.md now exists in the repo and users just include it via their setup |

---

## Step-by-Step

1. Write `CLAUDE.md` with full structure (see content spec below)
2. Rewrite `AGENTS.md` as a condensed derivative (no copy-paste of skill list)
3. Rewrite `GEMINI.md` same as AGENTS.md
4. Remove the inline CLAUDE.md snippet from README (it's now redundant — the actual file exists)
5. Update `setup` and `setup.ps1` to print: "CLAUDE.md is included in the kit — add it to your project root or symlink it"
6. Commit

---

## CLAUDE.md Content Spec

```markdown
# hubspot-agent-kit

HubSpot operator skill pack for AI agents. Covers workflow auditing,
deal operations, UTM normalization, CRM hygiene, and more.

## Directory Layout

skills/          10 SKILL.md files — one per operation domain
rules/           38 audit rules (INDEX.md is the master table)
scripts/         Python utilities (audit, workflows, processing)
templates/       Workflow JSON templates for common patterns
docs/            API reference, workflow patterns, data models, security
agents/          3 specialist subagent definitions

## Behavior Contract

- Before any HubSpot task: read the relevant skills/*/SKILL.md
- Before any API call: check docs/api-reference.md for correct endpoint + auth
- Before any workflow change: run scripts/audit/audit_workflows.py first
- Default DRY_RUN=true — never write to HubSpot without user confirmation
- State findings as facts. Say UNKNOWN rather than guessing.
- Never log or echo HUBSPOT_API_KEY in output

## Skills (slash commands)

/hs-audit      → skills/workflow-audit/SKILL.md   — audit all workflows against 38 rules
/hs-build      → skills/workflow-build/SKILL.md   — build + deploy workflows via API v4
/hs-deals      → skills/deal-operations/SKILL.md  — create, associate, move deals
/hs-meetings   → skills/meeting-operations/SKILL.md — activity types, outcomes, governance
/hs-utm        → skills/utm-operations/SKILL.md   — UTM normalization + backfill
/hs-crm        → skills/crm-audit/SKILL.md        — orphans, missing associations, hygiene
/hs-calls      → skills/call-routing/SKILL.md     — disposition routing, lead status
/hs-pages      → skills/landing-pages/SKILL.md    — download, edit, publish pages
/hs-normalize  → skills/lead-normalization/SKILL.md — bulk property normalization
/hs-hygiene    → skills/data-hygiene/SKILL.md     — ghost deals, stale contacts, dupes

## Agents

agents/hubspot-auditor.md   — read-only portal analysis
agents/hubspot-builder.md   — workflow creation and deployment
agents/hubspot-analyst.md   — CRM queries and reporting

## Key Rules to Know

See rules/INDEX.md. Most impactful:
- WF-005 CRITICAL: Circular enrollment loop
- WF-006 CRITICAL: Lifecycle stage downgrade
- WF-016 CRITICAL: Object type / flow type mismatch
- WF-002 HIGH: Broken property reference
- WF-018 HIGH: Meeting deal missing activity type filter
```

---

## Risks / Tradeoffs

- CLAUDE.md living inside the kit repo means users who `git clone` into their
  `~/.claude/skills/` directory get it automatically loaded by Claude Code.
  This is the correct behavior — it's how skill packs are meant to work.
- AGENTS.md and GEMINI.md condensed versions mean Codex/Gemini get less context,
  but that's appropriate — those agents work better with tighter prompts.
- The README inline snippet (added in the previous fix) becomes slightly redundant
  once CLAUDE.md is restored. Keep a one-liner in README pointing to the file,
  remove the inline block.

---

## Validation

After changes:
- `grep -r "gstack" .` → 0 results
- `grep -r "getlevrg" .` → 0 results
- CLAUDE.md exists at repo root
- `cat CLAUDE.md` shows the behavior contract, not just a command list
- AGENTS.md and GEMINI.md are each under 60 lines, no copy-pasted skill lists
- `git diff --stat` shows clean set of changes
