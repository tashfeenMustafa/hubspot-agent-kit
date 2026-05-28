# SKILL: workflow-audit

## Name: workflow-audit
## Description: Audit all workflows in a HubSpot portal. Fetches all flows via Automation API v4, runs them against the 38 rules in rules/, scores each workflow, produces a prioritized report with CRITICAL/HIGH/MEDIUM/LOW issues.
## Slash Command: /hs-audit

### Purpose
This skill is designed to provide a comprehensive audit of HubSpot automation workflows within a given portal. It systematically retrieves all active workflows, gathers essential portal context (such as contact and deal properties, pipeline stages, and static lists), and then evaluates each workflow against a predefined set of rules. The output is a prioritized report detailing issues by severity (CRITICAL, HIGH, MEDIUM, LOW), enabling efficient remediation and optimization of automation processes.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal to audit.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Steps

1.  **Fetch All Workflows**:
    *   Initiate a GET request to the HubSpot Automation API v4 to retrieve a list of all workflows in the portal.
    *   **API Pattern**: `GET $HUBSPOT_BASE_URL/automation/v4/flows?limit=100`
    *   Iterate through paginated results to ensure all workflows are captured.

2.  **Get Portal Context**:
    *   Before auditing, gather relevant portal configuration to provide context for rule evaluation. This includes:
        *   Contact Properties: Essential for understanding contact-based workflow criteria and actions.
        *   **API Pattern**: `GET $HUBSPOT_BASE_URL/crm/v3/properties/contacts`
        *   Deal Properties: Crucial for evaluating deal-based workflow criteria and actions.
        *   **API Pattern**: `GET $HUBSPOT_BASE_URL/crm/v3/properties/deals`
        *   Deal Pipelines and Stages: Necessary for assessing deal stage transitions and related automation.
        *   **API Pattern**: `GET $HUBSPOT_BASE_URL/crm/v3/pipelines/deals`
        *   Static Lists: Used to understand list-based enrollments and segmentations.
        *   **API Pattern**: `GET $HUBSPOT_BASE_URL/contacts/v1/lists/all/lists/static`

3.  **Run Workflows Through Rules**:
    *   For each fetched workflow, evaluate its configuration against the 38 rules defined in `rules/INDEX.md`.
    *   Each rule should check for specific conditions, best practices, or potential issues (e.g., missing exit conditions, inefficient branching, unoptimized property updates, deprecated actions).
    *   Rules will assign a severity level to any identified issues.

4.  **Score and Group by Severity**:
    *   Aggregate the findings for each workflow.
    *   Score each workflow based on the number and severity of issues detected.
    *   Group the identified issues by severity: CRITICAL, HIGH, MEDIUM, LOW.

5.  **Output Ranked Report**:
    *   Generate a clear, structured report.
    *   Prioritize the report by severity, listing CRITICAL issues first, followed by HIGH, MEDIUM, and LOW.
    *   For each issue, include:
        *   Workflow Name and ID
        *   Rule Violated
        *   Severity (CRITICAL, HIGH, MEDIUM, LOW)
        *   Description of the Issue
        *   Recommended Fix or Improvement
    *   Ensure the report is generic and contains no company-specific identifiers.

### Example Report Structure

```
## HubSpot Workflow Audit Report - $HUBSPOT_PORTAL_ID

### CRITICAL Issues
- **Workflow Name**: "Abandoned Cart Nurture (V1)" (ID: 12345678)
  - **Rule Violated**: WF-001 - Missing Re-enrollment Trigger
  - **Description**: This workflow lacks a re-enrollment trigger, meaning contacts will only enter once, potentially missing subsequent qualifying events.
  - **Recommendation**: Add "When contact meets criteria" re-enrollment trigger based on cart abandonment event.

### HIGH Issues
- **Workflow Name**: "Lead Qualification Follow-up" (ID: 98765432)
  - **Rule Violated**: WF-005 - Inefficient Property Update
  - **Description**: Workflow updates 'Lifecycle Stage' without checking if it's already at the target stage, causing unnecessary API calls.
  - **Recommendation**: Add an "IF/THEN branch" to check current 'Lifecycle Stage' before updating.

### MEDIUM Issues
...

### LOW Issues
...
```

### Best Practices for AI Agent
*   Always paginate API calls to ensure all data is retrieved.
*   Handle API rate limits gracefully.
*   Provide clear and actionable recommendations for each identified issue.
*   Ensure the report is easily digestible and highlights the most pressing problems.
