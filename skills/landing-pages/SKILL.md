# SKILL: landing-pages

## Name: landing-pages
## Description: Download, audit, modify, and publish HubSpot landing pages via CMS API. Sync pages to local files, apply bulk edits, duplicate campaigns, and push changes live.
## Slash Command: /hs-pages

### Purpose
This skill empowers the AI agent to manage HubSpot landing pages comprehensively using the CMS API. It covers downloading page content for local review or modification, performing audits, applying bulk edits, duplicating pages for new campaigns, and publishing changes live. This enables efficient and scalable management of HubSpot web assets.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal for landing page operations.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Sections

1.  **List Landing Pages**:
    *   Before performing any operations, you often need to identify the pages in the portal.
    *   **API Pattern**: `GET $HUBSPOT_BASE_URL/cms/v3/pages/landing-pages?limit=100`
    *   Paginate through results to get a comprehensive list of all landing pages, including their IDs and key properties.

2.  **Download Page HTML/Content**:
    *   To audit or modify a page, its content needs to be retrieved.
    *   **API Pattern**: `GET $HUBSPOT_BASE_URL/cms/v3/pages/landing-pages/{id}`
    *   This returns a detailed JSON object representing the page, including its HTML, modules, and property values.

3.  **Update Page**:
    *   After making modifications (e.g., in a local file), changes can be pushed back to HubSpot.
    *   **API Pattern**: `PATCH $HUBSPOT_BASE_URL/cms/v3/pages/landing-pages/{id}`
    *   **Payload**: A JSON object containing the properties to be updated. Only include the properties you intend to change.

4.  **Publish Page**:
    *   To make a draft page live or push changes immediately, the page needs to be published.
    *   **API Pattern**: `POST $HUBSPOT_BASE_URL/cms/v3/pages/landing-pages/{id}/schedule`
    *   **Payload**: `{"publishDate": "YYYY-MM-DDTHH:MM:SS.sssZ"}`. To publish immediately, set `publishDate` to a timestamp in the past.

5.  **Duplicate a Page**:
    *   For new campaigns or A/B testing, duplicating an existing page is efficient.
    *   **API Pattern**: `POST $HUBSPOT_BASE_URL/cms/v3/pages/landing-pages/clone`
    *   **Payload**: `{"id": {sourcePageId}}` and optionally `"name": "New Page Name"`.

6.  **Sync to Local Files**:
    *   For more complex or bulk edits, it's effective to sync pages to local files.
    *   **Process**:
        1.  Download the page JSON using `GET /cms/v3/pages/landing-pages/{id}`.
        2.  Extract relevant sections (e.g., `layoutSections`, `htmlTitle`, `metaDescription`) into a local file structure (e.g., individual HTML/Markdown files for content, a JSON config file for properties).
        3.  Allow for local modification of these files.
        4.  When ready, reconstruct the HubSpot-compatible JSON payload and push changes back using `PATCH /cms/v3/pages/landing-pages/{id}`.

7.  **Revert Changes**:
    *   To safeguard against unintended errors, implement a revert mechanism.
    *   **Process**: Before any modification, save a snapshot of the original page JSON content locally.
    *   If a revert is needed, use the saved snapshot to perform a `PATCH` update, restoring the page to its previous state.

### Best Practices for AI Agent
*   Always confirm page IDs and intended actions with the user before executing any modifications or publications.
*   When syncing to local files, provide a clear directory structure and naming convention.
*   Highlight the differences between draft and published content.
*   Implement version control for local page files if extensive modifications are anticipated.
*   Provide clear success/failure messages for all operations.
