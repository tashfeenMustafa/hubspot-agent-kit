# SKILL: call-routing

## Name: call-routing
## Description: Build and maintain call-based lead status automation. Route leads based on call disposition, duration, and notes keywords. Auto-set hs_lead_status after every completed call.
## Slash Command: /hs-calls

### Purpose
This skill enables the AI agent to automate `hs_lead_status` updates based on call activities. It involves creating and maintaining `PLATFORM_FLOW` workflows that analyze call disposition, duration, and even keywords within call notes to accurately route and update lead statuses after every completed call.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal for call routing operations.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Sections

1.  **PLATFORM_FLOW on Calls Object (`objectTypeId: 0-48`)**:
    *   Call-based automation is best handled using a `PLATFORM_FLOW` triggered on the Calls object.
    *   **Object Type ID**: `0-48` is the standard `objectTypeId` for HubSpot Calls.

2.  **Enrollment Trigger: Call Completed**:
    *   The workflow should enroll contacts (or the associated object) whenever a call activity is marked as completed.
    *   **Trigger Condition**: `hs_call_status` is `COMPLETED`.

3.  **Disposition Values**:
    *   HubSpot uses various `hs_call_disposition` values to describe the outcome of a call.
    *   **Common Values**:
        *   `CONNECTED`: Call was answered and a conversation took place.
        *   `LEFT_LIVE_MESSAGE`: Left a message with someone else.
        *   `LEFT_VOICEMAIL`: Left a message on an answering machine.
        *   `NO_ANSWER`: No one picked up, no voicemail.
        *   `BUSY`: Line was busy.
        *   `WRONG_NUMBER`: The number dialed was incorrect.
        *   `CANCELLED`: Call was cancelled.
    *   These dispositions are central to lead status routing.

4.  **Lead Status Routing Table**:
    *   Define a mapping from call dispositions and other call attributes to `hs_lead_status` values.
    *   **Examples**:
        *   `CONNECTED` + `hs_call_duration` (long duration) -> `open_deal`
        *   `LEFT_VOICEMAIL` -> `in_progress`
        *   `NO_ANSWER` or `BUSY` -> `attempted_to_contact`
        *   `WRONG_NUMBER` -> `unqualified`
        *   `CANCELLED` -> `bad_timing`
    *   This logic will be implemented using `IF/THEN branches` within the workflow.

5.  **Notes Keyword Parsing (`hs_call_body`)**:
    *   Enhance routing by scanning the `hs_call_body` (call notes) for specific keywords.
    *   **Example Keywords**: `"meeting booked"`, `"scheduled demo"`, `"call back next week"`, `"qualified"`, `"not interested"`.
    *   **Inference**: Use keyword presence to further refine `hs_lead_status` or trigger additional actions.

6.  **`hs_lead_status` Values**:
    *   Understand the canonical `hs_lead_status` values used in the portal.
    *   **Common Values**:
        *   `open_deal`: Qualified and actively working a deal.
        *   `in_progress`: Actively being worked, but no deal yet.
        *   `attempted_to_contact`: Tried reaching out multiple times.
        *   `unqualified`: Not a good fit.
        *   `bad_timing`: Not ready now, but potentially later.
        *   `connected`: Made contact, but no clear next step yet.
    *   The agent should be able to map call outcomes to these statuses.

7.  **Branch Structure: Disposition -> Duration -> Notes Keyword**:
    *   Design the workflow with a hierarchical branching structure for robust routing:
        *   **Primary Branch**: Based on `hs_call_disposition`.
        *   **Secondary Branch (within disposition)**: Based on `hs_call_duration` (e.g., calls > 5 minutes vs. < 5 minutes for `CONNECTED`).
        *   **Tertiary Branch (within duration)**: Based on keyword detection in `hs_call_body`.
    *   Each final path should lead to an action that sets the appropriate `hs_lead_status` on the associated contact.

### Best Practices for AI Agent
*   Always confirm the desired lead status definitions and routing logic with the user.
*   Provide a clear visual or textual representation of the proposed workflow branching logic.
*   Allow for customization of keywords used for notes parsing.
*   Implement testing to ensure the routing logic correctly assigns lead statuses.
