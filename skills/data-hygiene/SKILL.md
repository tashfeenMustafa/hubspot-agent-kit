# SKILL: data-hygiene

## Name: data-hygiene
## Description: Run full CRM hygiene pipeline. Close ghost deals (no activity 90+ days), clean stale SAL contacts, infer missing meeting outcomes, remove duplicate contacts, and enforce data quality standards.
## Slash Command: /hs-hygiene

### Purpose
This skill orchestrates a comprehensive CRM data hygiene pipeline in HubSpot. It automates the identification and remediation of various data quality issues, including closing inactive deals, cleaning stale sales-accepted leads (SALs), inferring missing meeting outcomes, and detecting duplicate contacts. The ultimate goal is to maintain a clean, accurate, and actionable CRM database.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal for data hygiene operations.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Sections

1.  **Ghost Deal Cleanup**:
    *   **Problem**: Deals that have been inactive for an extended period and are not in a closed stage can skew pipeline metrics.
    *   **Search Pattern**: Use the CRM Search API for deals.
    *   **Filter Criteria**: `last_activity_date < (today - 90 days)` AND `dealstage NOT IN ['closedwon', 'closedlost', 'closedlost_unqualified']` (adjust terminal stages as per portal configuration).
    *   **Action**: Move identified ghost deals to `Closed Lost` with a `reason = stale` or `no_activity`.
    *   **API Pattern**: `PATCH $HUBSPOT_BASE_URL/crm/v3/objects/deals/{dealId}`

2.  **Stale SAL Cleanup**:
    *   **Problem**: Contacts at the Sales Accepted Lead (SAL) lifecycle stage who have no recent engagement or active deals.
    *   **Search Pattern**: Use the CRM Search API for contacts.
    *   **Filter Criteria**: `lifecyclestage = salesqualifiedlead` AND `last_meeting_date < (today - 90 days)` AND `associations.deals = 0`.
    *   **Action**: Move these stale SAL contacts to a `cold_lead` or `nurture` status, or update their `hs_lead_status` accordingly.
    *   **API Pattern**: `PATCH $HUBSPOT_BASE_URL/crm/v3/objects/contacts/{contactId}`

3.  **Meeting Outcome Inference**:
    *   **Problem**: Missing `hs_meeting_outcome` values for historical or recently completed meetings, impacting reporting.
    *   **Process**: (Leverages `meeting-operations` skill components)
        1.  Search meetings (objectTypeId `0-48`) where `hs_meeting_outcome` is empty.
        2.  Scan `hs_meeting_body` for keywords like `"booked next step"`, `"reschedule"`, `"no show"`, `"completed"`.
        3.  Infer and set `hs_meeting_outcome`.
    *   **API Pattern**: `PATCH $HUBSPOT_BASE_URL/crm/v3/objects/meetings/batch/update`

4.  **Duplicate Removal (Flag for Review)**:
    *   **Problem**: Duplicate contact records lead to inaccurate data, inefficient outreach, and skewed analytics.
    *   **Detection**: (Leverages `crm-audit` skill components)
        1.  Find contacts with the same email domain and similar names (e.g., `firstname` and `lastname` fuzzy match).
        2.  Identify contacts with identical email addresses (primary key for duplicates).
    *   **Action**: **Do NOT automatically merge.** Flag potential duplicates for human review and provide details for manual merging via HubSpot's UI or a separate, confirmed merge process.

5.  **Always Require Explicit Confirmation Before Writing Any Changes**:
    *   **Critical Safety Measure**: For all data modification operations within the hygiene pipeline (closing deals, moving contacts, updating meetings), the AI agent *must* present a summary of proposed changes to the user and require explicit confirmation (e.g., a "yes" or "confirm") before executing any write operations.

6.  **Nightly Automation Pattern: GitHub Actions Cron Job**:
    *   **Implementation**: To ensure continuous data hygiene, schedule the execution of these hygiene scripts or API calls.
    *   **Method**: Utilize GitHub Actions with a `cron` trigger to run these processes nightly.
    *   **Workflow Example (`.github/workflows/hubspot-hygiene.yml`)**:
        ```yaml
        name: HubSpot CRM Daily Hygiene
        on:
          schedule:
            - cron: '0 0 * * *' # Runs every day at midnight UTC
          workflow_dispatch:

        jobs:
          run-hygiene:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v2
              - name: Run Hygiene Script
                run: |
                  python3 hygiene_script.py --portal-id ${{ secrets.HUBSPOT_PORTAL_ID }} \
                                            --api-key ${{ secrets.HUBSPOT_API_KEY }} \
                                            --base-url ${{ vars.HUBSPOT_BASE_URL || 'https://api.hubapi.com' }}
        ```
    *   The `hygiene_script.py` would encapsulate the logic defined in this skill.

### Best Practices for AI Agent
*   Provide detailed logging of all hygiene operations, including records identified, actions taken, and any errors.
*   Allow users to customize the thresholds for "stale" or "inactive" (e.g., 90 days).
*   Clearly distinguish between actions that can be automated and those requiring human review (e.g., duplicate merging).
*   Ensure that any automated changes are reversible if possible.
