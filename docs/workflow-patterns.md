# Proven HubSpot Workflow Design Patterns for AI Agents

This document outlines common and effective HubSpot workflow design patterns, providing guidance for AI agents to implement robust automation.

## 1. UTM Normalization

*   **Trigger Type:** Filter Based
*   **Object Type:** Contact
*   **Key Actions:** Standardize `utm_source` and `utm_medium` properties.
*   **Enrollment Criteria:** Contact's `utm_source` property contains known non-canonical values (e.g., 'facebook', 'fb', 'Google Ads').
*   **Re-enrollment Setting:** `true` (allow contacts to re-enroll if their `utm_source` changes back to a non-canonical value).
*   **Suppression Gate:** Contact's `utm_source` property is already set to the canonical value (e.g., 'meta', 'google').
*   **Known Gotchas:** Ensure comprehensive lists of non-canonical variations. Order of operations matters if normalizing multiple UTM properties.

## 2. Deal Stage Contact Tracking

*   **Trigger Type:** Platform Flow (Deal Stage Change)
*   **Object Type:** Deal
*   **Key Actions:** Copy relevant contact properties (e.g., UTMs) to deal properties at each stage. Update associated contact's `lifecyclestage` and `hs_lead_status`.
*   **Enrollment Criteria:** Deal enters a specific deal stage.
*   **Re-enrollment Setting:** `false` (typically only needs to fire once per stage progression).
*   **Known Gotchas:** Ensure correct property mapping. Be mindful of potential race conditions if multiple workflows update the same contact properties.

## 3. Meeting-Booked Deal Creation

*   **Trigger Type:** Platform Flow (Meeting based)
*   **Object Type:** Meeting
*   **Key Actions:** Create a new deal and associate it with the contact and meeting. Set initial deal properties (e.g., `dealname`, `pipeline`, `dealstage`).
*   **Enrollment Criteria:** Meeting `hs_activity_type` is 'MEETING' and `hs_meeting_outcome` is 'COMPLETED' or 'BOOKED'.
*   **Re-enrollment Setting:** `false`.
*   **Known Gotchas:** Prevent duplicate deal creation for the same meeting. Ensure appropriate associations are made (contact to deal, meeting to deal).

## 4. Call Lead Status Routing

*   **Trigger Type:** Platform Flow (Call based)
*   **Object Type:** Call
*   **Key Actions:** Set associated contact's `hs_lead_status` based on call disposition, duration, or notes.
*   **Enrollment Criteria:** Call `hs_call_status` is 'COMPLETED'.
*   **Re-enrollment Setting:** `false`.
*   **Known Gotchas:** Define clear branching logic for various call outcomes. Consider owner filters to prevent unintended changes by non-sales calls.

## 5. Lifecycle Stage Enforcement

*   **Trigger Type:** Contact Flow
*   **Object Type:** Contact
*   **Key Actions:** Ensure `lifecyclestage` is never downgraded. Always update `lifecyclestage` and `hs_lead_status` in tandem to maintain consistency.
*   **Enrollment Criteria:** Contact's `lifecyclestage` changes or `hs_lead_status` changes.
*   **Re-enrollment Setting:** `true`.
*   **Known Gotchas:** Complex branching logic can lead to difficult-to-debug scenarios. Carefully define the hierarchy of lifecycle stages and lead statuses.

## 6. Ghost Deal Cleanup

*   **Trigger Type:** Contact Flow (on deals object - though typically contact-based workflows are used to manage deal properties based on contact activity).
*   **Object Type:** Deal
*   **Key Actions:** Move stale deals to a 'Closed Lost' deal stage.
*   **Enrollment Criteria:** Deal's `hs_last_activity_date` is more than 90 days ago AND `dealstage` is not 'Closed Won' or 'Closed Lost'.
*   **Re-enrollment Setting:** `true` (to catch deals that become stale again).
*   **Known Gotchas:** Ensure clear definition of 'stale'. Consider exceptions for specific deal types or sales processes.

## 7. Meeting Governance

*   **Trigger Type:** Platform Flow (Meeting based)
*   **Object Type:** Meeting
*   **Key Actions:** Flag meetings with missing required fields, send reminders to the meeting owner.
*   **Enrollment Criteria:** Meeting is created or updated AND specific properties (e.g., `hs_meeting_title`, `hs_meeting_body`) are empty.
*   **Re-enrollment Setting:** `false` (unless you want continuous reminders).
*   **Known Gotchas:** Avoid spamming owners with too many notifications. Provide clear instructions for corrective actions.

## 8. Owner Assignment Rotation

*   **Trigger Type:** Contact Flow
*   **Object Type:** Contact
*   **Key Actions:** Assign contacts to owners in a round-robin fashion from a predefined list.
*   **Enrollment Criteria:** New contact created or specific contact property changes.
*   **Re-enrollment Setting:** `false` (to prevent re-assigning contacts unnecessarily).
*   **Known Gotchas:** Manage the list of owners effectively. Handle out-of-office or inactive owners gracefully. Ensure proper property updates for `hubspot_owner_id`.