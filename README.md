# hubspot-agent-kit

A standalone, portal-agnostic toolkit that provides the intelligence layer HubSpot's
generic tooling omits: it **learns** a portal (Discovery), **grades** it against universal
HubSpot truths plus the portal's own conventions (Grading), and **operates** on it with
audit-gated, dry-run-first remediation (Operation).

Built for agentic use (Claude Code, Cowork, Codex) and packaged so HubSpot Agent CLI users
can bolt it on as an extension. See [`docs/prd.md`](docs/prd.md) for the full product spec.

> **Status:** early development (P0 — Foundation). Not yet usable.

## Install (dev)

```bash
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Develop

```bash
ruff check .        # lint
black --check .     # format
mypy                # type-check (strict)
pytest              # tests
```

## Safety

Every write defaults to **dry-run** (`DRY_RUN=true`) and is gated by a harness-level
write-guard. Copy [`.env.example`](.env.example) to `.env` and fill in credentials.
