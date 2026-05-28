# SKILL: workflow-build

## Name: workflow-build
## Description: Build and deploy HubSpot automation workflows via Automation API v4. Supports CONTACT_FLOW, DEAL_FLOW, and PLATFORM_FLOW types. Includes enrollment triggers, branch logic, and property write actions.
## Slash Command: /hs-build

### Purpose
This skill enables the creation and deployment of HubSpot automation workflows. It guides the AI agent through defining workflow intent, selecting the appropriate flow type (CONTACT_FLOW, DEAL_FLOW, PLATFORM_FLOW), designing the action sequence with branching logic, validating against common pitfalls, and finally deploying the workflow using the HubSpot Automation API v4.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal where the workflow will be deployed.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Steps

1.  **Understand Workflow Intent**:
    *   Begin by asking the user to describe the desired automation, including the object type it should operate on (contacts, deals, or other objects) and its primary goal.

2.  **Determine Trigger Type and Enrollment Criteria**:
    *   Based on the intent, identify the appropriate workflow object type (CONTACT_FLOW, DEAL_FLOW, PLATFORM_FLOW).
    *   Define the enrollment triggers (e.g., property-based, list-based, form submission, event-based) and criteria.

3.  **Design Action Sequence with Branching**:
    *   Outline the sequence of actions (e.g., setting property values, sending emails, creating tasks, delaying) and decision branches (IF/THEN) required to achieve the workflow's goal.
    *   Ensure logical flow and clear paths for different outcomes.

4.  **Validate Against Common Pitfalls**:
    *   Before deployment, cross-reference the designed workflow against known HubSpot automation pitfalls and best practices, potentially drawing from `rules/` for validation.
    *   **Gotchas to Consider**:
        *   **`CONTACT_FLOW` limitations**: Cannot directly write `dealstage` or other deal-specific properties from a `CONTACT_FLOW`.
        *   **`PLATFORM_FLOW` limitations**: Cannot write `hs_analytics_source` directly from a `PLATFORM_FLOW`.
        *   **`suppressionFilterBranch`**: This field must be *omitted* if not used, not merely set to an empty object `{}`. An empty object will cause API errors.
        *   **Convergent Branches**: HubSpot workflows generally do not support convergent branches where multiple paths merge back into a single path. Design workflows with distinct, non-convergent paths or separate workflows if complex merges are required.

5.  **Deploy via Automation API v4**:
    *   Construct the JSON payload for the workflow based on the designed steps, triggers, and actions.
    *   **API Pattern (Create)**: `POST $HUBSPOT_BASE_URL/automation/v4/flows`
    *   **API Pattern (Update)**: `PATCH $HUBSPOT_BASE_URL/automation/v4/flows/{id}` (Use for modifications after initial creation)
    *   **API Pattern (Delete)**: `DELETE $HUBSPOT_BASE_URL/automation/v4/flows/{id}` (For removing workflows)
    *   Always verify deployment success by checking the API response and, if possible, fetching the newly created/updated workflow.

### Workflow Types Explained

*   **`CONTACT_FLOW`**:
    *   **Object Type**: `0-1` (Contact)
    *   **Purpose**: Primarily for automating actions related to contacts. Triggers often involve contact property changes, form submissions, or list membership.
    *   **Limitations**: Cannot directly modify properties of associated objects (like deals or companies) unless specific association actions are configured.

*   **`DEAL_FLOW`**:
    *   **Object Type**: `0-3` (Deal)
    *   **Purpose**: Focuses on automating actions around deals. Common triggers include deal stage changes, deal property updates, or deal creation.
    *   **Limitations**: Cannot directly modify contact properties unless specific association actions are configured.

*   **`PLATFORM_FLOW`**:
    *   **Object Type**: Various (e.g., `0-48` for Meetings, `0-49` for Calls, `2-1324151` for custom objects)
    *   **Purpose**: Highly flexible, allowing automation on various standard and custom objects beyond contacts and deals. Requires specifying the `objectTypeId`.
    *   **Considerations**: The available actions and properties for `PLATFORM_FLOW` are specific to the `objectTypeId` it operates on. Be mindful of object-specific limitations, such as the `hs_analytics_source` example.

### Best Practices for AI Agent
*   Always confirm the user's intent and desired workflow behavior before constructing the API payload.
*   Present a summary of the planned workflow before deployment for user confirmation.
*   Implement robust error handling for API calls.
*   Provide clear feedback on deployment status and any issues encountered during validation or deployment.
