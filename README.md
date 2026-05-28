# **The HubSpot skill pack for AI agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Compatible](https://img.shields.io/badge/Claude%20Code-compatible-blue)](https://claude.ai/code)
[![Works with Codex](https://img.shields.io/badge/Works%20with-Codex-blue)](https://openai.com/blog/openai-codex)
[![Works with Gemini](https://img.shields.io/badge/Works%20with-Gemini-blue)](https://gemini.google.com/)

Audit workflows, manage deals, normalize UTMs, and operate HubSpot like a RevOps engineer — in plain English.

## Installation

```bash
git clone https://github.com/your-org/hubspot-agent-kit.git
cd hubspot-agent-kit
./setup
```

Then add this snippet to your project's `CLAUDE.md` (or `AGENTS.md` / `GEMINI.md`):

```markdown
## HubSpot Agent Kit

HubSpot skills are in `skills/` — read the relevant SKILL.md before any HubSpot task.

Available slash commands:
/hs-audit   /hs-build   /hs-deals   /hs-meetings   /hs-utm
/hs-crm     /hs-calls   /hs-pages   /hs-normalize  /hs-hygiene

Rules for auditing are in rules/INDEX.md.
Scripts are in scripts/. Always run with DRY_RUN=true first.
```

## Slash Commands

| Command | What it does |
|---------|-------------|
| /hs-audit | Audit all workflows — score every flow against 38 production-tested rules |
| /hs-build | Describe a workflow in plain English, get it built and deployed |
| /hs-deals | Create deals, associate contacts, move pipeline stages |
| /hs-meetings | Backfill meeting types, infer outcomes, manage scheduling pages |
| /hs-utm | Audit UTM data, build normalization workflows for Meta/Google/LinkedIn |
| /hs-crm | Find orphan deals, missing associations, lifecycle stage mismatches |
| /hs-calls | Build call disposition routing and lead status automation |
| /hs-pages | Download, edit, and publish landing pages |
| /hs-normalize | Normalize contact properties in bulk |
| /hs-hygiene | Full CRM hygiene pipeline — close ghost deals, clean stale contacts |

## Works With

This kit is designed to work seamlessly with:
*   Claude Code
*   OpenAI Codex
*   Gemini CLI
*   Cursor
*   Any AI agent that reads a `SKILL.md` file for skill definitions.

### Production-Derived Audit Rules

Our `/hs-audit` command checks against 38 production-tested rules, covering everything from CRITICAL to LOW severity issues, ensuring your HubSpot portal remains optimized and error-free.

## Why This Exists

Built from real RevOps work. These patterns come from operating a live HubSpot portal — UTM attribution, deal pipeline, meeting governance, data hygiene. Everything here has been tested against the actual HubSpot API.

## Requirements

*   Python 3.8+
*   `HUBSPOT_API_KEY` (Private App)

## License

This project is licensed under the MIT License.
