"""PII/secret scanner used as a blocking CI gate.

Detects, in source text, the shapes of data that must never land in this public
repo: email addresses, UUIDs, HubSpot private-app tokens, and labeled HubSpot
portal/hub IDs. A line carrying an inline ``pii-allow`` marker is skipped, so
fabricated fixtures and intentional examples can coexist with the gate.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

#: A line containing this marker is exempt from scanning.
ALLOW_MARKER = "pii-allow"

#: Ordered (kind, pattern) rules. First-listed wins is not assumed — every rule
#: runs against every line, so a line can raise more than one finding.
_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("hubspot_token", re.compile(r"\bpat-[a-z0-9]+-[0-9a-fA-F-]{12,}")),
    ("portal_id", re.compile(r"(?i)\b(?:portal|hub)[_-]?id\b\s*[:=]\s*\d{5,}")),
    (
        "uuid",
        re.compile(
            r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-" r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
        ),
    ),
)


@dataclass(frozen=True)
class Finding:
    """One suspected secret/PII match."""

    path: str
    line: int
    kind: str
    match: str


#: Directory names never worth scanning (VCS, caches, envs, build output).
_SKIP_DIRS = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "node_modules",
        ".tox",
        "dist",
        "build",
        ".idea",
    }
)


def scan_text(text: str, *, path: str = "<text>") -> list[Finding]:
    findings: list[Finding] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if ALLOW_MARKER in line:
            continue
        for kind, pattern in _RULES:
            for m in pattern.finditer(line):
                findings.append(Finding(path=path, line=lineno, kind=kind, match=m.group(0)))
    return findings


def _iter_files(paths: Iterable[str]) -> Iterable[Path]:
    for raw in paths:
        root = Path(raw)
        if root.is_file():
            yield root
            continue
        for p in root.rglob("*"):
            # Skip-dir names are matched only *below* the scan root, so a skip
            # word in an ancestor (e.g. a checkout under .../build/) can't
            # silently disable the whole scan.
            if p.is_file() and not (_SKIP_DIRS & set(p.relative_to(root).parts)):
                yield p


def _read_text(path: Path) -> str | None:
    """Decode a file to text, or None if unreadable.

    A security gate must not skip a file just because it is not UTF-8: PowerShell
    writes UTF-16 by default. Try UTF-8 (with BOM) then UTF-16, then fall back to
    latin-1 (which maps every byte), so a real secret cannot hide behind an
    encoding the naive reader chokes on.
    """
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    for enc in ("utf-8-sig", "utf-16"):
        try:
            return raw.decode(enc)
        except UnicodeError:
            continue
    return raw.decode("latin-1", errors="replace")


def scan_paths(paths: Iterable[str]) -> list[Finding]:
    findings: list[Finding] = []
    for file in _iter_files(paths):
        text = _read_text(file)
        if text is None:
            continue
        findings.extend(scan_text(text, path=str(file)))
    return findings


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    paths = args or ["."]
    missing = [p for p in paths if not Path(p).exists()]
    if missing:
        # A misconfigured path must fail the gate, not silently scan nothing.
        print(f"PII/secret scan: path(s) not found: {', '.join(missing)}", file=sys.stderr)
        return 2
    findings = scan_paths(paths)
    for f in findings:
        print(f"{f.path}:{f.line}: {f.kind}: {f.match}", file=sys.stderr)
    if findings:
        print(
            f"PII/secret scan failed: {len(findings)} finding(s). "
            f"Fix, or annotate an intentional line with '{ALLOW_MARKER}'.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
