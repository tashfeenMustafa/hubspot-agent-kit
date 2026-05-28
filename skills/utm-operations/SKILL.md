# SKILL: utm-operations

## Name: utm-operations
## Description: Build, audit, and maintain UTM normalization workflows for Meta, Google, and LinkedIn. Backfill UTM data on existing contacts. Ensure consistent attribution tracking.
## Slash Command: /hs-utm

### Purpose
This skill focuses on ensuring clean and consistent UTM tracking within HubSpot. It enables the AI agent to create, audit, and maintain workflows that normalize UTM property values from various sources (Meta, Google, LinkedIn). Additionally, it supports backfilling historical UTM data on existing contacts to improve attribution accuracy.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal for UTM operations.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Sections

1.  **Standard UTM Field Names**:
    *   HubSpot utilizes several standard properties for UTM tracking. Understanding these is crucial for consistent data capture and reporting.
    *   `utm_source`: Identifies the source of the traffic (e.g., Google, Meta, LinkedIn).
    *   `utm_medium`: Identifies the medium of the traffic (e.g., cpc, organic, paid_social).
    *   `utm_campaign`: Identifies a specific product promotion or strategic campaign.
    *   `utm_term`: Identifies paid keywords.
    *   `utm_content`: Differentiates similar content, or links within the same ad.
    *   `hs_analytics_source`: This is an **Original Source** property, typically read-only via workflow. It reflects the first touchpoint and is set by HubSpot automatically. While not directly modifiable via workflow for normalization, it's important for attribution context.

2.  **Canonical UTM Values**:
    *   To maintain clean data, establish and enforce canonical values for common traffic sources.
    *   **Meta (Facebook/Instagram)**:
        *   `utm_source = meta` (or `facebook`, `instagram` can be normalized to `meta`)
        *   `utm_medium = paid_social`
    *   **Google (Ads/Organic)**:
        *   `utm_source = google`
        *   `utm_medium = cpc` (for paid ads) or `organic` (for organic search)
    *   **LinkedIn**:
        *   `utm_source = linkedin`
        *   `utm_medium = paid_social`

3.  **FILTER_BASED Trigger with Re-enrollment ON**:
    *   When building UTM normalization workflows, use a `FILTER_BASED` enrollment trigger.
    *   **Crucially, enable re-enrollment** to ensure contacts are re-evaluated and normalized if their UTM properties change over time, or if they acquire new non-canonical UTM values.
    *   The trigger criteria should identify contacts whose `utm_source`, `utm_medium`, etc., match non-canonical values.

4.  **Suppression Gate**:
    *   Implement a suppression gate at the beginning of the workflow using an `IF/THEN branch`.
    *   **Condition**: Skip actions if `utm_source` (or other relevant UTM properties) already match the desired canonical values.
    *   This prevents unnecessary processing and API calls for contacts whose UTM data is already clean.
    *   Example: `IF utm_source IS EQUAL TO 'meta' THEN GO TO END`

5.  **Backfill Pattern**:
    *   For historical data cleanup, implement a backfill process:
    *   **Search**: Use the CRM Search API to find existing contacts where `utm_source` (or `utm_medium`, etc.) is `IN` a list of non-canonical values (e.g., `['facebook', 'instagram', 'fb', 'ig']`).
    *   **Batch Update**: Use the CRM Batch Update API (`PATCH $HUBSPOT_BASE_URL/crm/v3/objects/contacts/batch/update`) to update these contacts to their canonical `utm_source` and `utm_medium` values.
    *   This can be a one-time operation or a regularly scheduled cleanup.

6.  **Common Violations Caught by Audit Rules**:
    *   **WF-009**: Detects workflows attempting to write `hs_analytics_source` directly, which is read-only.
    *   **WF-010**: Flags inconsistent or non-canonical UTM values in workflow filters or actions.
    *   **WF-028**: Identifies workflows with missing re-enrollment for normalization tasks, leading to stale data.

### Best Practices for AI Agent
*   Always confirm with the user the desired canonical values before creating or modifying normalization workflows.
*   Suggest a `DRY_RUN` for backfill operations, if supported by the API, or preview changes before applying them.
*   Provide clear reporting on the number of contacts updated during backfill operations.
*   Regularly audit UTM-related workflows to ensure they remain effective and catch new non-canonical inputs.
