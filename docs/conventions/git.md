# Git conventions

> This file records the branch/merge safety rules (enforced by a hook, see
> below) and the CI + owned review-gate discipline every PR passes through.

## Branch & merge safety (enforced)

These rules exist because a branch was once deleted on the *assumption* a PR had
merged when it had not — which closed the still-open PR. The fix is to verify
against git/GitHub, never against a claim (including the user's or your own).

1. **Verify a merge before acting on it.** "It's merged" is a claim, not a fact.
   Before any cleanup, confirm with one of:
   - `git log --oneline origin/main` shows the merge commit, or
   - `gh pr view <n> --json state,mergedAt` returns `state: MERGED` and a non-null
     `mergedAt`. A PR can be **CLOSED without being merged** (`mergedAt: null`).

2. **Never delete a branch (local or remote) unless `origin/main` provably
   contains its commits.** Enforced by `.claude/hooks/guard-branch-delete.py`
   (a `PreToolUse` hook): any `git branch -d/-D/--delete` or
   `git push … --delete`/`:branch` is checked against `origin/main`; if the
   branch is not an ancestor — or the state can't be verified — the deletion is
   held for human confirmation. To intentionally abandon unmerged work, set
   `ALLOW_UNMERGED_BRANCH_DELETE=1`.

3. **Deleting a PR's remote head branch closes the PR.** Only delete a remote
   branch *after* the PR is confirmed merged (rule 1). If you delete it while the
   PR is open, GitHub closes the PR unmerged.

4. **`git branch -d` warnings are signal, not noise.** If it prints
   "not yet merged", stop — that contradicts any belief that it was merged.

5. **Never `git reset --hard` on `main`** (or force-push it). To sync local main,
   `git checkout main && git pull` — a fast-forward, not a reset.

6. **Branch off freshly-pulled main.** `git checkout main && git pull` before
   `git checkout -b <branch>` so the new branch starts from the current tip.

## Recovering a mistakenly-closed/deleted PR branch

Commits are not lost when a branch is deleted:
- Local object store keeps them (find via `git reflog` or a known SHA).
- GitHub keeps the PR head at `refs/pull/<n>/head` —
  `git fetch origin refs/pull/<n>/head`.

Recreate the branch at that SHA, push it, then `gh pr reopen <n>`.

## CI gates (blocking)

Every push to `main`/`staging` and every PR runs `.github/workflows/ci.yml`.
All five steps are **blocking** — a red step blocks merge:

1. **Ruff** — `ruff check src tests` (lint).
2. **Black** — `black --check src tests` (format).
3. **Mypy** — `mypy` (strict, from `pyproject.toml`).
4. **Pytest** — `pytest -q` (full suite).
5. **PII/secret scan** — `python -m hubspot_agent_kit.ci.secret_scan .`

Run the same gates locally before pushing (see the commands above, via `.venv`).

### PII/secret scanner

`hubspot_agent_kit.ci.secret_scan` fails the build if it finds the shape of data
that must never land in this public repo: email addresses, UUIDs, HubSpot
`pat-` private-app tokens, and labeled `portalId`/`hubId` values. Bare integers
are not flagged. To keep an intentional example (a fabricated fixture, a doc
sample), put `pii-allow` on that line and the scanner skips it. Never use it to
smuggle real client data — client specifics live only in the private engine and
as scrubbed `examples/`.

## Owned review-gate

Review tooling is **owned-only — no external SaaS bot** (no Greptile/CodeRabbit/
Qodo/etc.). The path from `/implement` to merge:

```
/implement (TDD, fresh session per issue)
  → push PR
  → CI gates          (lint · type · test · PII/secret scan)   ← deterministic, blocking
  → AI review-loop    (owned only)                             ← judgment
  → human gate        (mandatory)                              → merge → staging → main
```

- **`/code-review`** — reviews the diff for correctness + reuse/simplification/
  efficiency. `--comment` posts inline PR comments; `--fix` applies fixes.
- **`superpowers:requesting-code-review` / `receiving-code-review`** — the
  disciplined request → address → re-verify loop.

**Rules of the loop:**

- **Cap iterations; don't chase a score.** A human makes the final merge call —
  don't Goodhart any confidence metric.
- **Auto-merge is forbidden on write-path / remediation code.** Anything that can
  mutate a live CRM gets mandatory human review before merge.
- Keep PRs **minimal/stacked** so each has a single review surface. Branch flow
  is `staging → main`.

## Branch protection

**Target:** `main` (and `staging`) require the CI `gates` check to pass and
require a PR — no direct pushes, no force-push, no deletion. Because auto-merge
is forbidden on write-path code, the human gate is a review discipline, not just
a GitHub setting.

**Status — ACTIVE** (since 2026-07-07, when the repo went public — see
`docs/decisions/2026-07-07-repo-public.md`). `main` enforces: the required
status check `lint · type · test · pii-scan`, strict up-to-date, `enforce_admins`
on, no force-push, no deletion, PR required. The convention layer (no auto-merge
on write-path, mandatory human merge, branch-delete hook) still applies on top.

To re-apply or verify (the command that set it — GitHub only allows this on
public repos or private repos on a paid plan). It needs a nested JSON body, so
pass `--input` (not `-F`, which sends flat literal keys), and use
`{owner}/{repo}` placeholders (gh does not expand REST-doc `:owner` colons). The
required-check context is the CI **job name**, `lint · type · test · pii-scan`:

```sh
gh api -X PUT repos/{owner}/{repo}/branches/main/protection --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["lint · type · test · pii-scan"] },
  "enforce_admins": true,
  "required_pull_request_reviews": { "required_approving_review_count": 0 },
  "restrictions": null
}
JSON
# verify:
gh api repos/{owner}/{repo}/branches/main/protection --jq '.required_status_checks.contexts'
```
