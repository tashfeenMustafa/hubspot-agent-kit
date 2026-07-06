#!/usr/bin/env python3
"""PreToolUse guard: never delete a git branch that isn't merged into origin/main.

Reads the Claude Code hook payload on stdin. If the Bash command is a branch
deletion (local `git branch -d/-D/--delete`, or remote `git push <remote>
--delete NAME` / `git push <remote> :NAME`), it verifies every targeted branch
is an ancestor of origin/main. If any branch is NOT provably merged — or the
merge state can't be determined — it returns permissionDecision "ask" so a human
must confirm. Provably-merged deletions pass silently.

This exists because a branch was once deleted on the assumption a PR had merged
when it had not, which closed the still-open PR. The check here is independent of
any "it's merged" claim: it asks git, not the caller.

Escape hatch: set ALLOW_UNMERGED_BRANCH_DELETE=1 to intentionally abandon work.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

BASE = "origin/main"


def _emit_ask(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=os.environ.get("CLAUDE_PROJECT_DIR") or None,
    )


def _is_ancestor(ref: str) -> bool | None:
    """True if ref is an ancestor of origin/main, False if not, None if unknown."""
    if _git("rev-parse", "--verify", "--quiet", ref).returncode != 0:
        return None  # ref doesn't resolve locally — can't judge
    if _git("rev-parse", "--verify", "--quiet", BASE).returncode != 0:
        return None  # no origin/main to compare against
    return _git("merge-base", "--is-ancestor", ref, BASE).returncode == 0


def _targets(cmd: str) -> list[tuple[str, str]]:
    """Return (label, ref-to-check) pairs for branches this command would delete."""
    out: list[tuple[str, str]] = []
    # Local: git branch -d/-D/--delete NAME...
    if re.search(r"\bgit\b[^|&;]*\bbranch\b", cmd) and re.search(
        r"(?:^|\s)(?:-d|-D|--delete|-[a-zA-Z]*[dD])(?:\s|$)", cmd
    ):
        after = re.split(r"(?:-d|-D|--delete)\b", cmd, maxsplit=1)
        if len(after) > 1:
            for tok in after[1].split():
                if tok.startswith("-") or tok in {"branch", "git"}:
                    continue
                out.append((tok, tok))
    # Remote: git push <remote> --delete NAME  |  git push <remote> :NAME
    if re.search(r"\bgit\b[^|&;]*\bpush\b", cmd):
        m = re.search(r"push\s+(\S+)\s+(?:--delete|-d)\s+(\S+)", cmd)
        if m:
            out.append((m.group(2), f"{m.group(1)}/{m.group(2)}"))
        for m in re.finditer(r"push\s+(\S+)\s+:(\S+)", cmd):
            out.append((m.group(2), f"{m.group(1)}/{m.group(2)}"))
    return out


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # can't parse — don't interfere
    cmd = (payload.get("tool_input") or {}).get("command") or ""
    if not cmd:
        return 0
    if os.environ.get("ALLOW_UNMERGED_BRANCH_DELETE") == "1":
        return 0

    targets = _targets(cmd)
    if not targets:
        return 0  # not a branch deletion

    problems: list[str] = []
    for label, ref in targets:
        state = _is_ancestor(ref)
        if state is True:
            continue  # merged into origin/main — safe
        if state is False:
            problems.append(f"'{label}' is NOT merged into {BASE}")
        else:
            problems.append(f"'{label}' merge state vs {BASE} could not be verified")

    if problems:
        _emit_ask(
            "Branch-delete guard: "
            + "; ".join(problems)
            + f". Confirm it is truly merged (check `git log {BASE}` or "
            "`gh pr view <n> --json mergedAt`) before deleting, or set "
            "ALLOW_UNMERGED_BRANCH_DELETE=1 to abandon it intentionally."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
