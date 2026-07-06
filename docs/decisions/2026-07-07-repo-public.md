# Decision: make the repository public (2026-07-07)

**Status:** Accepted — executed 2026-07-07.

## Decision

Made `tashfeenMustafa/hubspot-agent-kit` **public** during P0, and enabled
server-side branch protection on `main`.

## Context

The PRD (`docs/prd.md`) originally scheduled public/distribution for **P8** and
set one hard precondition (PRD "Before going public"): audit the full v1 git
history — reachable via branch `archive/v1` / tag `v1-archive` — for PII/secrets
and rewrite/squash if needed, while still private, because history is permanent
once published.

Separately, server-side branch protection is gated by GitHub behind public
repos or a paid plan; the repo was private on the free plan, so protection could
not be enabled (HTTP 403). Going public unlocks it at no cost.

## What was verified first

The PRD precondition was satisfied before flipping visibility:

- Ran the owned PII/secret scanner (`hubspot_agent_kit.ci.secret_scan`) across
  **every blob in all git refs** (117 blobs, 17 commits, incl. `archive/v1`).
- One match: `contact@example.com` in a v1 `deal-operations` skill doc — <!-- pii-allow: reserved example domain -->
  the RFC 2606 **reserved example domain** in an API-payload sample, not real
  PII or a secret. No real emails, UUIDs, tokens, or portal IDs in history.
- Verdict: history clean; safe to publish.

## Consequences

- Repo is public; all history is now permanently visible.
- Branch protection is **active** on `main` (see `docs/conventions/git.md`):
  required CI check, strict, enforce-admins, no force-push/deletion, PR required.
- This pulls the "public" milestone earlier than P8. Distribution work
  (marketplace / skills-registry / `pip` publish) remains P8; only visibility +
  protection moved up.
- Future contributions still land only via PR through the CI gates + human merge
  gate.
