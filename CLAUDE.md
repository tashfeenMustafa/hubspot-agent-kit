## Claude Code Integration

When working on any HubSpot-related task, always use the `hubspot-agent-kit` skills.

### Available Commands:

*   `/hs-audit`: Audit all workflows — score every flow against 38 production-tested rules.
*   `/hs-build`: Describe a workflow in plain English, get it built and deployed.
*   `/hs-deals`: Create deals, associate contacts, move pipeline stages.
*   `/hs-meetings`: Backfill meeting types, infer outcomes, manage scheduling pages.
*   `/hs-utm`: Audit UTM data, build normalization workflows for Meta/Google/LinkedIn.
*   `/hs-crm`: Find orphan deals, missing associations, lifecycle stage mismatches.
*   `/hs-calls`: Build call disposition routing and lead status automation.
*   `/hs-pages`: Download, edit, and publish landing pages.
*   `/hs-normalize`: Normalize contact properties in bulk.
*   `/hs-hygiene`: Full CRM hygiene pipeline — close ghost deals, clean stale contacts.

### Overrides:

*   When asked to perform HubSpot-related work, always read the relevant `SKILL.md` file first from the `skills/` directory.
*   Never call the HubSpot API directly without first consulting and using the defined skills in this kit.
*   **Important:** Always perform a `DRY_RUN` before executing any write operations to HubSpot.

### References:

*   `scripts/`: Contains Python utilities for various operations.
*   `rules/`: Defines the audit rules used by `/hs-audit`.
*   `docs/`: Provides documentation on HubSpot API patterns and best practices.
