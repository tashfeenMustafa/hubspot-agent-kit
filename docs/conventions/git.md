# Git conventions

> Scope note: this file will be expanded in issue #5 (P0) with the full CI +
> review-gate discipline. It currently records the branch/merge safety rules,
> which are enforced by a hook (see below), not just documented.

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
