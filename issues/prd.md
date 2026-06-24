# PRD — hubspot-agent-kit

> Status: Draft v1 · Generated via the `write-a-prd` workflow after a 16-question grilling session.
> This is the **destination document**. It is intentionally not a line-by-line implementation spec —
> phase plans and vertical-slice issues (`prd-to-issues`) derive from it.

---

## Problem Statement

HubSpot power users, super admins, RevOps engineers, and ops managers run portals that drift over time:
features go unused, data integrity decays, conventions are inconsistent, and nobody has a defensible,
repeatable answer to *"how good is this portal, and what should we fix?"*. Auditing a portal today is
manual, tribal, and tangled with one company's specific setup.

HubSpot has just shipped the **Agent CLI** (public beta, 2026-06-23), an official **MCP server**, and an
**agent-tools** extension model. These cover the *plumbing* — CRUD, search, pipelines, properties,
associations, workflows, dry-run — but they have **no opinion** about whether a portal is well-run.
There is no portable *intelligence layer* that learns a portal, grades it against HubSpot best practice
and the portal's own declared standards, and drives safe remediation.

## Solution

**hubspot-agent-kit** is a **standalone, portal-agnostic toolkit** that provides the intelligence HubSpot's
generic tooling deliberately omits: it **learns** a portal (discovery), **grades** it (against universal
HubSpot truths + the portal's own conventions + an extensible knowledge base), and **operates** on it
(audit-gated, dry-run-first remediation). It is built for agentic use (Claude Code, Cowork, Codex) and is
packaged so HubSpot Agent CLI users can bolt it on as an extension — the kit is the base; the Agent CLI
*extends on top of it*, not the reverse.

Three co-equal pillars — **Discovery, Grading, Operation** — sit on one swappable data layer and one
user-owned portal profile, so the *judgment engine is generic* while the *standard is per-portal*.

---

## Ubiquitous Language (Glossary)

| Term | Meaning |
|---|---|
| **Portal** | A HubSpot account/instance being analyzed. |
| **Discovery** | Read-only enumeration of what a portal contains and how it is used. |
| **Grading** | Evaluating a portal against a standard, producing scored findings. |
| **Operation / Remediation** | Writes that fix a graded finding; always dry-run-gated. |
| **Universal rule** | A grading rule true for *any* HubSpot portal (platform truth + KB best practice); zero config. |
| **Convention rule** | A grading rule meaningful only against a portal's *own* declared standard. |
| **Portal profile** | `portal-profile.yaml` — the user-owned declaration of a portal's conventions (lifecycle order, lead-status enum, stage→status maps, UTM canon, SLAs, disposition maps, custom-doc paths). Consumed by every skill, agent, rule, hook, command, tool. |
| **HubSpot client** | The single deep module that all code calls to reach HubSpot; never raw HTTP. |
| **Adapter** | A concrete implementation of the HubSpot-client interface (REST / Agent-CLI / MCP / in-memory fake). |
| **Reference KB** | `references/*.md` — distilled, provenanced HubSpot KB/dev-doc/changelog facts, refreshable + human-ratified. |
| **Finding** | A single graded issue with severity, category, evidence, and (if fixable) a remediation. |
| **Bootstrap** | The short post-install run that learns the portal and drafts the portal profile. |

---

## Users & Their Jobs (priority order)

1. **RevOps engineer / architect** — *"keep my portal healthy and operate it at scale."* Primary. Runs the kit in Claude Code; values grading **and** operation.
2. **HubSpot Super Admin** — *"prove the portal is well-run and compliant."* Consumes adoption, data-integrity, governance, and compliance outputs; favors read-only/conversational (MCP) paths.
3. **Agency / solutions consultant** — *"audit a portal I didn't build and produce a client deliverable."* Repeatable discovery + polished graded report + remediation backlog.
4. **Marketing / Sales Ops manager** — pipeline/workflow/lead hygiene in their lane.

All four are covered in the READMEs and in functionality.

---

## User Stories

**Discovery**
1. As a RevOps engineer, I want to point the toolkit at a portal and enumerate objects, properties, pipelines, stages, lifecycle order, users/owners, workflows, and lists, so I have a complete inventory.
2. As a consultant, I want a one-command bootstrap right after install that learns a client portal and drafts a `portal-profile.yaml`, so I'm not starting from a blank page.
3. As a super admin, I want to see which HubSpot features/objects are used vs unused, so I can justify licensing and adoption.
4. As a RevOps engineer, I want workflow + enrollment discovery (active/disabled, enrollment counts), so I can find dead and underused automations.
5. As a consultant, I want repo↔live drift detection, so documented config that diverged from the live portal is surfaced.
6. As any user, I want discovery to be strictly read-only, so learning a portal can never change it.

**Grading**
7. As any user, I want **universal rules** to run with zero configuration and grade any portal on platform truths (broken action chains, empty enrollment criteria, read-only-field writes, branch convergence, orphan/ghost deals, missing associations, zero-enrollment workflows, duplicates).
8. As a RevOps engineer, I want **convention rules** that grade against *my* portal profile (lead-status↔deal-stage conformance, lifecycle stickiness, UTM canon, SLA timings), so grading reflects my standard, not someone else's.
9. As a super admin, I want **data-integrity & completeness** checks (missing activity type/outcome/notes, click-ID sync gaps, missing associations) and **feature-adoption % coverage** scoring.
10. As a consultant, I want each finding to carry severity, category, evidence, and (where fixable) a remediation, so I can hand over a prioritized backlog.
11. As any user, I want grading to be **deterministic and testable** (rules are versioned files, not live fetches).
12. As any user, I want every rule tagged with `source` + `hubspot_verified_date`, so I can trust and date the judgment.

**Knowledge**
13. As any user, I want a **refreshable reference KB** with provenance that I can re-pull from HubSpot docs/changelog, with diffs surfaced for **human ratification** (never silently trusted).
14. As any user, I want a staleness warning when the KB is older than a threshold or a HubSpot changelog entry post-dates it.
15. As a RevOps engineer, I want to **ingest my own KBs, SOPs, playbooks, guides, and templates** — local files or pulled directly from HubSpot — and have them distilled into `references/*.md` and auto-drafted into rules, so my standard becomes gradeable and stays updated.
16. As a power user, I want to pull specific HubSpot KB/docs/specs via **context7 MCP** or a **custom agent-browse** and update knowledge when I choose.

**Operation (audit-gated)**
17. As a RevOps engineer, I want to remediate a graded finding (deal/meeting/call ops, contact hygiene, UTM/click-ID backfill, workflow auto-patch vs recreate), so fixing follows from findings.
18. As any user, I want every write to default to **dry-run** and require explicit confirmation, so a live CRM is never mutated by surprise.
19. As any user, I want a **harness-level write guard** so writes are blocked unless dry-run is explicitly disabled and confirmed — safety that a skill cannot forget.
20. As a RevOps engineer, I want bulk/scheduled writes to optionally route through the HubSpot Agent CLI adapter.

**Reporting & distribution**
21. As a consultant, I want per-domain report templates (audit, backlog, funnel, drift) legible to a client stakeholder.
22. As any user, I want to install via plugin marketplace, plain `git clone`, **or** `pip install`, and to add the skills to an Agent-CLI setup like `npx skills add`.
23. As a super admin, I want a paste-in `CLAUDE.md` snippet for my own portal-working repo so my agent loads the profile and obeys the dry-run contract.

---

## Implementation Decisions

### Identity & relationship to HubSpot tooling
- **Standalone toolkit with its own intelligence layer.** Full discovery + grading + operation retained. Packaged so the HubSpot **Agent CLI extends on top of it** (kit is the base).

### Architecture — deep modules & the central seam
- **One `HubSpot client` deep module** is the single interface all code calls (`search_objects`, `get_workflows`, `update_property`, etc.). No raw HTTP anywhere else. This is *the* seam and the test boundary.
- **Adapters** behind that interface (swappable, picked by job):
  - **direct-REST** — default, standalone, zero external dependency (generalized from the proven private engine; all client specifics stripped).
  - **Agent-CLI** — bulk/scheduled/background writes via `hubspot <noun> <verb>`.
  - **HubSpot MCP** — conversational, read-heavy, human-in-loop (super-admin path).
  - **in-memory fake** — for tests.
- **Two-tier grading:** `scope: universal | convention` on every rule. Universal = out-of-the-box value; convention = profile-driven.
- **Portal profile (`portal-profile.yaml`)** — user-owned, Hybrid-bootstrapped: universal rules need nothing; the discovery layer **drafts** the profile from inspection; the user **ratifies/edits** (by hand, any CLI agent, or an opt-in end-of-session hook). GL-style values ship only as `examples/`.
- **Three-tier knowledge:** curated versioned `rules/` · refreshable provenanced `references/` (human-ratified refresh) · user-supplied docs wired through the profile. Ingestion **drafts**, humans **ratify**.

### Language, packaging, distribution
- **Python 3.11+ engine** (type hints + mypy/pyright strict, `black` + `ruff`) + **markdown** skills/agents/rules; **hooks** as bash/python commands. Markdown is the agent-facing contract; python/bash is the implementation.
- **Layered distribution (Q8/C):** the repo **is** a Claude Code plugin (marketplace-installable), **also** a plain `git clone`, **and** a `pip install -e .` package. Skills also publishable to the skills registry. **One shipped plugin** initially, internally sub-grouped `skills/audit/* · skills/operate/* · skills/knowledge/*` for a later split.
- **Dev-only Matt-Pocock SDLC skills** (`grill-me`, `write-a-prd`, `prd-to-issues`, `tdd`, `improve-codebase-architecture`) vendored under `.claude/skills/dev-sdlc/` — **gitignored and search-ignored**, never shipped.

### Config, safety, context
- **`settings.json` + hooks:** permission allowlist for read-only/safe commands; **SessionStart** freshness guard (missing profile → prompt bootstrap; stale KB → warn) + load profile summary; **PreToolUse write-guard** (non-negotiable shipped hook) enforcing dry-run-gated, confirmed writes at the harness level; opt-in **Stop** hook to refresh profile/ingest knowledge. `DRY_RUN=true` shipped default; `HUBSPOT_*` via `.env`.
- **`CLAUDE.md`** = thin (≤200-line) map + behavior contract; canonical, with thin `AGENTS.md`/`GEMINI.md` pointers (no duplication); plus a paste-in snippet for users' own repos. Behavior contract: read relevant `SKILL.md` first · load profile, never assume GL values · dry-run default + gated writes · never commit client specifics/PII · state UNKNOWN over guessing.
- **MCPs:** HubSpot (runtime adapter), context7 + a search MCP (dev-time), all optional and documented per-purpose. REST + a token alone is fully functional.

### Conventions (enforced)
- `docs/conventions/`: `code.md`, `testing.md`, `docs-and-markdown.md` (no markdown > 200 lines), `rules-authoring.md` (rule frontmatter + provenance), `safety-and-privacy.md`, `git.md`.
- **Blocking CI + pre-commit gates:** lint + type + test **and a PII/secret scanner** (portal IDs, emails, GUID/token shapes) so client data cannot land in the repo.

### Proposed modules (write-a-prd step 4)
| Module | Depth / responsibility | Interface (sketch) |
|---|---|---|
| `hubspot_client` | the seam; hides transport, auth, pagination, rate-limit, dry-run | `search/get/list/create/update/...` per object family |
| `adapters/*` | satisfy `hubspot_client` (rest / agent_cli / mcp / fake) | injected into client |
| `discovery` | enumerate portal → inventory | `discover(portal) -> Inventory` |
| `profile` | draft/load/validate `portal-profile.yaml` | `bootstrap(Inventory) -> Profile`, `load() -> Profile` |
| `rules` | rule registry + evaluator (universal + convention) | `evaluate(Inventory, Profile) -> [Finding]` |
| `grading` | scoring/severity/adoption % over findings | `score([Finding]) -> Report` |
| `knowledge` | references KB, refresh, ingest, staleness | `refresh()`, `ingest(source)` |
| `remediation` | finding → dry-run-gated write | `plan(Finding) -> Change`, `apply(Change, dry_run)` |
| `reporting` | per-domain templates → md/csv/html | `render(Report, template)` |

---

## Testing Decisions

- **Good tests verify behavior through public interfaces, not implementation details.** Mock **only at the HubSpot-client adapter boundary** (the system boundary) — never internal modules.
- **Unit (bulk, fast):** rule evaluators, grading/scoring, profile parse+validate, normalization, inference heuristics, report rendering — driven by **PII-scrubbed JSON fixtures** from a sandbox.
- **Integration:** whole audit domains through the deep module via the **in-memory fake adapter**; the **REST adapter against recorded HTTP cassettes** (pagination/auth/dry-run).
- **Adapter contract suite:** one shared suite **all adapters (REST/Agent-CLI/MCP) must pass**, proving interface parity.
- **E2E (slow, opt-in, credentials-gated):** against a **dedicated HubSpot developer sandbox** — discover → bootstrap → audit → **assert dry-run writes nothing** → one gated real write to a throwaway record → verify → cleanup. CI nightly/manual only, never per-PR.
- Shape = test pyramid: many unit, some integration + contract, few e2e. Highest-value safety tests: the **contract suite** and the **dry-run-writes-nothing** assertion.
- Modules explicitly targeted for tests first: `hubspot_client` + adapters (contract), `rules`, `grading`, `profile`. *(Confirm with the team before P1.)*

---

## Phasing Roadmap

| Phase | Vertical slice |
|---|---|
| **P0 Foundation** | plugin scaffold, `CLAUDE/AGENTS/GEMINI`, conventions docs, `settings.json` + write-guard hook, CI (lint/type/test/PII-scan), python package skeleton, vendored dev SDLC skills |
| **P1 Data seam** | `hubspot_client` interface + REST adapter + in-memory fake + contract suite |
| **P2 Tracer bullet** | discover workflows → one universal workflow audit → report (thin end-to-end proof) |
| **P3 Discovery + profile bootstrap** | full enumeration → draft `portal-profile.yaml` → user ratifies |
| **P4 Universal grading** | all platform-truth rules across objects/deals/associations |
| **P5 Convention grading** | profile-driven rules; data-integrity/completeness; feature-adoption % scoring; 4-chunk audit generalized |
| **P6 Knowledge layer** | `references/` + provenance; `refresh-knowledge` + `ingest-knowledge` skills (local/HubSpot/context7/agent-browse); staleness hook |
| **P7 Operate (audit-gated)** | deal/meeting/call ops, hygiene, UTM/click-ID backfill, workflow remediation; all dry-run-gated |
| **P8 Reporting + distribution** | per-domain report templates; marketplace + skills-registry publish; Agent-CLI + MCP adapters; all-4-persona docs |

Order is dependency-driven. Discovery/Grading/Operation are **co-equal in value** but Operation depends on the seam + findings. A thin dry-run operate slice may be pulled into P2 if desired.

`prd-to-issues` will break each phase into independently-grabbable vertical-slice issues (`issues/NNN-*.md`), tagged HITL/AFK.

---

## Out of Scope

- Re-implementing CRUD/auth/pagination plumbing that the HubSpot Agent CLI/MCP already provide *as a goal in itself* — the kit drives them; it competes on **judgment**, not plumbing.
- Shipping any client-specific values, IDs, owner names, GUIDs, or PII (those exist only in the private engine and as scrubbed `examples/`).
- An autonomous unattended write-loop ("Ralph"-style product feature) — explicitly dropped.
- A hosted SaaS / multi-tenant service, billing, or a web app (CLI/agent + reports only for now; dashboards are later-phase, optional).
- Non-HubSpot CRMs.

---

## Further Notes / Open Questions

- **Marketplace timing:** plugin-marketplace publish is part of P8; confirm whether an earlier private marketplace is wanted.
- **Empty working tree:** the v1 repo's 92 files currently exist only in git HEAD (`07bb7c4`), deleted from disk. Decide at scaffold time whether to `git restore` and refactor v1 in place, or scaffold fresh and cherry-pick. (Not done in this PRD step.)
- **`issues/` tracking:** kept in-repo as the planning record (PRD + generated issues); revisit if dock-rot becomes a concern.
- **Sandbox portal:** E2E needs a dedicated HubSpot developer test account — provision before P1 work that touches adapters.
- The 16 grilling decisions behind this PRD are recorded in the conversation; key ones are reflected inline above.
