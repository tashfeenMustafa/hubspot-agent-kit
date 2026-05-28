# SKILL: meeting-operations

## Name: meeting-operations
## Description: Manage HubSpot meeting activity types, backfill hs_activity_type on historical meetings, configure scheduling page mapping, and maintain meeting-booked deal creation workflows.
## Slash Command: /hs-meetings

### Purpose
This skill focuses on ensuring accurate and actionable meeting data within HubSpot. It enables the AI agent to manage `hs_activity_type` values for meetings, backfill this data for historical records, configure mappings for scheduling pages, and maintain workflows that create deals upon meeting bookings.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal for meeting operations.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Sections

1.  **`hs_activity_type` Values and Deal Creation Triggers**:
    *   The `hs_activity_type` property categorizes different types of meeting activities.
    *   Some `hs_activity_type` values are critical for triggering downstream automation, particularly deal creation.
    *   **Example**: `Commercial Call - Prospect` is often configured to trigger automatic deal creation.
    *   Other values, like `Internal Meeting` or `Customer Support Call`, might *not* trigger deal creation.
    *   **Action**: Agent should be able to query existing `hs_activity_type` values and their associated automation implications.

2.  **Backfill Pattern for Missing `hs_activity_type`**:
    *   Historical meetings might lack an `hs_activity_type` value, hindering reporting and automation.
    *   **Search**: Use the CRM Search API to find meetings (objectTypeId `0-48`) where `hs_activity_type` is unknown or empty.
    *   **Infer**: Attempt to infer the correct `hs_activity_type` from other meeting properties like `hs_meeting_title`, `hs_meeting_body`, or the URL of the scheduling page if available in notes.
    *   **Batch Update**: Use the CRM Batch Update API (`PATCH $HUBSPOT_BASE_URL/crm/v3/objects/meetings/batch/update`) to populate the `hs_activity_type`.

3.  **Scheduling Page to Activity Type Mapping Approach**:
    *   HubSpot scheduling pages often correspond to specific meeting types.
    *   **Configuration**: Define a mapping table (e.g., within agent's configuration or a separate lookup skill) that links scheduling page URLs or names to canonical `hs_activity_type` values.
    *   **Automation**: When a meeting is booked via a specific scheduling page, use this mapping to automatically set the `hs_activity_type` either at the time of booking or via a `PLATFORM_FLOW`.

4.  **Meeting Outcome Inference**:
    *   The `hs_meeting_outcome` property provides valuable data on meeting results (e.g., `Booked`, `Rescheduled`, `No Show`, `Completed`).
    *   **Inference**: Scan the `hs_meeting_body` or `hs_call_body` (for calls associated with meetings) for keywords to infer the outcome.
    *   **Example Keywords**: `"booked next step"`, `"reschedule"`, `"no show"`, `"completed meeting"`.
    *   **Action**: Update `hs_meeting_outcome` based on inferred intent.

5.  **PLATFORM_FLOW on Meetings Object (`objectTypeId: 0-48`)**:
    *   Most meeting-related automation will be built using `PLATFORM_FLOW` on the meetings object.
    *   **Object Type ID**: `0-48` is the standard `objectTypeId` for HubSpot meetings.
    *   **Triggers**: Changes to meeting properties (e.g., `hs_meeting_start_time`, `hs_activity_type`, `hs_meeting_outcome`).
    *   **Actions**: Updating meeting properties, creating tasks, sending notifications, or triggering associated object workflows (e.g., creating a deal).

6.  **Common Issues Caught by Audit Rules**:
    *   **WF-018**: Flags meetings missing `hs_activity_type`, indicating a gap in data enrichment.
    *   **WF-033**: Identifies deal creation workflows that are not properly triggered by `hs_activity_type`, leading to missed deal opportunities.

### Best Practices for AI Agent
*   Always confirm the desired `hs_activity_type` values and their impact on deal creation with the user.
*   Prioritize backfilling `hs_activity_type` for active or recently completed meetings to ensure current data accuracy.
*   Provide a clear summary of proposed scheduling page mappings before implementation.
*   When inferring outcomes, allow for human review of suggestions, especially for critical decisions.
