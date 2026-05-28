# SKILL: deal-operations

## Name: deal-operations
## Description: Create deals, associate contacts to deals, move deals through pipeline stages, and trigger deal tracking workflows via HubSpot CRM API v3/v4.
## Slash Command: /hs-deals

### Purpose
This skill enables the AI agent to perform various operations related to deals in HubSpot CRM. It covers finding contacts, creating new deals, associating contacts with deals, and managing deal stages, all through the CRM API v3/v4. It also touches on patterns for triggering deal-related workflows.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal for deal operations.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Sections

1.  **Find Contact by Name or Email**:
    *   Before creating or associating deals, you often need to find the relevant contact.
    *   **API Pattern**: `POST $HUBSPOT_BASE_URL/crm/v3/objects/contacts/search`
    *   **Payload Example**: `{"filterGroups": [{"filters": [{"propertyName": "email", "operator": "EQ", "value": "contact@example.com"}]}], "properties": ["firstname", "lastname", "email"]}`
    *   Retrieve the `id` of the contact for subsequent operations.

2.  **Create Deal**:
    *   New deals are created by specifying key properties.
    *   **API Pattern**: `POST $HUBSPOT_BASE_URL/crm/v3/objects/deals`
    *   **Payload Example**: `{"properties": {"dealname": "New Client Opportunity", "amount": "5000", "pipeline": "default_sales_pipeline", "dealstage": "appointmentscheduled"}}`
    *   **Required Properties**: `dealname`, `pipeline` (ID or internal name), `dealstage` (internal name). `amount` is highly recommended.

3.  **Associate Contact to Deal**:
    *   Once a deal and contact exist, they need to be associated.
    *   **API Pattern**: `PUT $HUBSPOT_BASE_URL/crm/v4/objects/deals/{dealId}/associations/contacts/{contactId}/deal_to_contact`
    *   This API establishes a two-way association.

4.  **Move Deal Stage**:
    *   Progressing a deal involves updating its `dealstage` property.
    *   **API Pattern**: `PATCH $HUBSPOT_BASE_URL/crm/v3/objects/deals/{dealId}`
    *   **Payload Example**: `{"properties": {"dealstage": "qualifiedtobuy"}}`
    *   Ensure the new `dealstage` is valid for the deal's current `pipeline`.

5.  **Standard Deal Stages (Examples)**:
    *   While internal names vary by portal, common stages include:
        *   `appointmentscheduled` (Sales Accepted Lead - SAL)
        *   `qualifiedtobuy` (Sales Qualified Lead - SQL)
        *   `presentationscheduled` (Building Consensus)
        *   `decisionmakerboughtin` (Proposal Sent)
        *   `contractsent` (In-Contract/Negotiation)
        *   `closedwon` (Won)
        *   `closedlost` (Lost)
    *   Always verify internal stage names within the target HubSpot portal.

6.  **Create Deal for Meeting-Booked Pattern**:
    *   A common automation is creating a deal when a meeting is booked.
    *   This typically involves a `PLATFORM_FLOW` (or `CONTACT_FLOW` with deal creation action) triggered by a meeting activity.
    *   **Trigger**: A meeting being created or updated, often with a filter on `hs_activity_type` (e.g., `hs_activity_type = Commercial Call - Prospect`).
    *   **Action**: Create a new deal, associating it with the contact who booked the meeting.
    *   The deal name could be dynamically set (e.g., "Meeting with [Contact Name]").

### Best Practices for AI Agent
*   Always confirm the correct `pipelineId` and `dealstage` internal names with the user before creating or updating deals.
*   Validate that a contact exists before attempting to associate them with a deal.
*   Provide clear feedback on the success or failure of deal operations.
*   For deal stage changes, consider showing the current stage and confirming the target stage with the user.
