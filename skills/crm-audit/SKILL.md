# SKILL: crm-audit

## Name: crm-audit
## Description: Audit HubSpot CRM data quality. Find contacts missing deal associations, identify orphan deals, reconcile lifecycle stages, detect duplicates, and clean data hygiene issues.
## Slash Command: /hs-crm

### Purpose
This skill enables a comprehensive audit of HubSpot CRM data quality. It helps identify common data hygiene issues such as contacts without associated deals, orphaned deals, discrepancies in lifecycle stages, and potential duplicate contacts. The goal is to provide actionable insights for cleaning and maintaining a healthy CRM.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal for CRM audit.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Sections

1.  **Find Contacts at Lifecycle Stage with No Deal**:
    *   Identify contacts who have progressed to a sales-ready lifecycle stage but lack an associated deal, indicating potential dropped leads or missed opportunities.
    *   **Search Pattern**: Use the CRM Search API for contacts.
    *   **Filter**: `lifecyclestage = salesqualifiedlead` (or other relevant sales stages) AND `associations.deals = 0` (no associated deals).
    *   **API Pattern**: `POST $HUBSPOT_BASE_URL/crm/v3/objects/contacts/search` with appropriate filters.

2.  **Find Orphan Deals**:
    *   Detect deals that exist in the CRM but are not associated with any contacts, companies, or other relevant objects. These are often data entry errors.
    *   **Search Pattern**: Use the CRM Search API for deals.
    *   **Filter**: Deals where `associations.contacts = 0`.
    *   **API Pattern**: `POST $HUBSPOT_BASE_URL/crm/v3/objects/deals/search` with appropriate filters.

3.  **Lifecycle Stage Reconciliation**:
    *   Identify contacts whose `lifecyclestage` property does not align with the stage of their associated deals.
    *   **Process**: For contacts with associated deals, compare the `lifecyclestage` with the `dealstage` of their primary deal (or latest deal).
    *   **Discrepancy Example**: Contact is `Customer` but their only deal is `Closed Lost` and no other won deals exist.
    *   **Action**: Flag these contacts for review and potential `lifecyclestage` adjustment using `PATCH /crm/v3/objects/contacts/{id}`.

4.  **Duplicate Contact Detection**:
    *   Identify potential duplicate contacts within the CRM.
    *   **Detection Methods**:
        *   **Email Domain Similarity**: Group contacts by email domain and then analyze `firstname` and `lastname` for similar patterns.
        *   **Name Similarity**: Search for contacts with identical or very similar `firstname` and `lastname` values, especially if they also share company or other identifying information.
    *   **Action**: Flag potential duplicates for human review and merging.

5.  **Association Patterns**:
    *   To effectively audit relationships, understand how to retrieve associations.
    *   **API Pattern**: `GET $HUBSPOT_BASE_URL/crm/v4/objects/contacts/{id}/associations/deals`
    *   This allows fetching all deals associated with a specific contact.
    *   Similar patterns exist for other object associations (e.g., companies, tickets).

6.  **Bulk Update Pattern for Remediation**:
    *   Once data quality issues are identified, bulk updates are often necessary for remediation.
    *   **API Pattern**: `PATCH $HUBSPOT_BASE_URL/crm/v3/objects/contacts/batch/update`
    *   **Payload**: A list of objects, each containing an `id` and the `properties` to update.
    *   **Constraint**: Maximum 100 objects per batch request.
    *   **Best Practice**: Always perform a dry run or review changes before executing bulk updates.

### Best Practices for AI Agent
*   Always clearly state the criteria used for identifying data quality issues.
*   Present audit findings in a structured, easy-to-understand format with specific examples.
*   For any proposed data modifications (e.g., updating lifecycle stages, merging duplicates), *always* require explicit user confirmation before execution.
*   Suggest a regular cadence for CRM audits to maintain data hygiene over time.
