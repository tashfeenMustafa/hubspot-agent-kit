## Gemini Compatibility

This agent kit provides a set of pre-defined skills to interact with HubSpot. These can be integrated as system prompts for Gemini CLI.

### Available Skills and Commands:

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

### Usage Guidelines:

*   Skills are defined in the `skills/` directory. Before executing any HubSpot-related action, always read the relevant `SKILL.md` file to understand the skill's capabilities and parameters.
*   Always perform a `DRY_RUN` before executing any write operations to HubSpot.
