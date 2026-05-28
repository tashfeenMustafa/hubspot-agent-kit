# HubSpot API Reference for AI Agents

This document provides a concise reference for AI agents interacting with the HubSpot API.

## 1. Authentication

HubSpot APIs are primarily authenticated using **Private App tokens**.

*   **Method:** Include the token in the `Authorization` header as a Bearer token.
    `Authorization: Bearer $HUBSPOT_API_KEY`
*   **Creation:** Private App tokens can be created in your HubSpot account under `Settings > Integrations > Private Apps`.
*   **Scopes:** Each API operation requires specific scopes. Ensure your Private App has the necessary scopes enabled. Refer to the HubSpot API documentation for required scopes per endpoint.

## 2. Base URL

All HubSpot API requests should be made to: `https://api.hubapi.com`

## 3. Pagination

HubSpot APIs often use **cursor-based pagination**.

*   **Request:** Include an `after` parameter in your GET requests to retrieve results after a specific cursor.
*   **Response:** Look for `paging.next.after` in the response body to get the cursor for the next page of results.

## 4. Rate Limits

Be mindful of API rate limits to avoid service disruptions.

*   **Private Apps:** 100 requests per 10 seconds.
*   **OAuth Apps:** 200 requests per 10 seconds.

## 5. Key API Endpoints and Operations

### Contacts
*   **Get Contact Properties:** `GET /crm/v3/properties/contacts`
*   **Search Contacts:** `POST /crm/v3/objects/contacts/search` (supports filters)
*   **Update Contact:** `PATCH /crm/v3/objects/contacts/{id}`
*   **Batch Update Contacts:** `POST /crm/v3/objects/contacts/batch/update`

### Deals
*   **Get Deals:** `GET /crm/v3/objects/deals`
*   **Create Deal:** `POST /crm/v3/objects/deals`
*   **Update Deal:** `PATCH /crm/v3/objects/deals/{id}`
*   **Get Deal Pipelines:** `GET /crm/v3/pipelines/deals`

### Associations (v4)
*   **Create Association:** `PUT /crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
    *   Example: Associate a contact (0-1) to a deal (0-3) with association type ID 4.
        `PUT /crm/v4/objects/0-1/{contactId}/associations/0-3/{dealId}/4`

### Automation API (v4) - Workflows
*   **Get Flows:** `GET /automation/v4/flows`
*   **Create Flow:** `POST /automation/v4/flows`
*   **Update Flow:** `PATCH /automation/v4/flows/{id}`

### Meetings
*   **Get Meetings:** `GET /crm/v3/objects/meetings`
*   **Update Meeting:** `PATCH /crm/v3/objects/meetings/{id}`

### Calls
*   **Get Calls:** `GET /crm/v3/objects/calls`

### Lists
*   **Get Static Contact Lists:** `GET /contacts/v1/lists/all/lists/static`

### Landing Pages
*   **Get Landing Pages:** `GET /cms/v3/pages/landing-pages`
*   **Create Landing Page:** `POST /cms/v3/pages/landing-pages`
*   **Update Landing Page:** `PATCH /cms/v3/pages/landing-pages/{id}`

## 6. Common Error Codes

*   **400 Bad Request:** The request payload is malformed or invalid.
*   **401 Unauthorized:** Invalid or missing API key/token.
*   **403 Forbidden:** The authenticated private app lacks the required scopes for the operation.
*   **404 Not Found:** The requested resource (e.g., contact ID, deal ID) does not exist.
*   **429 Too Many Requests:** Rate limit exceeded. Implement retry logic with exponential backoff.

## 7. Windows SSL Note

When running `requests` on Windows in development environments, you might encounter SSL certificate issues. A common workaround is to use `requests(..., verify=False)`.
**WARNING:** This disables SSL certificate verification and should **never be used in production environments**. Always ensure proper SSL certificate handling in production.
