# SKILL: lead-normalization

## Name: lead-normalization
## Description: Normalize contact property values in bulk. Standardize job titles, company names, annual revenue buckets, business categories, team sizes, and services needed fields.
## Slash Command: /hs-normalize

### Purpose
This skill enables the AI agent to perform bulk normalization of contact property values in HubSpot. It addresses common data quality issues by standardizing unstructured or inconsistent data across various fields like job titles, company names, annual revenue, and business categories. The goal is to improve data accuracy, segmentation, and reporting.

### Environment Variables
- `$HUBSPOT_API_KEY`: Your HubSpot API key for authentication.
- `$HUBSPOT_PORTAL_ID`: The ID of the HubSpot portal for lead normalization operations.
- `$HUBSPOT_BASE_URL`: (Optional) The base URL for the HubSpot API. Defaults to `https://api.hubapi.com`.

### Key Sections

1.  **Job Title Normalization**:
    *   **Problem**: Inconsistent job titles (e.g., "CEO", "Chief Executive Officer", "Founder & CEO").
    *   **Process**:
        1.  Convert all job titles to lowercase.
        2.  Strip punctuation and extraneous characters.
        3.  Map common variants to a canonical list (e.g., `ceo`, `chief executive`, `founder` -> `CEO`).
    *   **Example Mapping**: `{ "chief executive officer": "CEO", "founder": "CEO", "cto": "CTO", "software engineer": "Software Engineer" }`

2.  **Annual Revenue Buckets**:
    *   **Problem**: Free-text annual revenue fields that are hard to segment.
    *   **Process**: Map free-text or numeric revenue values into predefined enum buckets.
    *   **Canonical Buckets (Examples)**:
        *   `<100k`
        *   `100k-500k`
        *   `500k-1M`
        *   `1M-5M`
        *   `5M-25M`
        *   `25M+`
    *   **Action**: Create or update a dedicated `annual_revenue_bucket` property.

3.  **Business Category Normalization**:
    *   **Problem**: Varied ways of describing industry or business type.
    *   **Process**: Map diverse inputs to a canonical list of business categories (e.g., "Software as a Service", "B2B SaaS", "Cloud Software" -> "SaaS").
    *   **Action**: Update a `business_category` property with canonical values.

4.  **Team Size Normalization**:
    *   **Problem**: Text descriptions of team size (e.g., "small team", "mid-market", "50-100 employees").
    *   **Process**: Map these to numeric ranges or predefined buckets.
    *   **Example**: `"startup"` -> `1-10`, `"enterprise"` -> `1000+`.

5.  **Bulk Search Pattern**:
    *   To find contacts requiring normalization, use the CRM Search API.
    *   **API Pattern**: `POST $HUBSPOT_BASE_URL/crm/v3/objects/contacts/search`
    *   **Filter**: Apply a `non-null` filter on the property you intend to normalize (e.g., `propertyName: "jobtitle", operator: "HAS_PROPERTY"`). Then, further filter results by specific non-canonical values.
    *   **Payload Example**: `{"filterGroups": [{"filters": [{"propertyName": "jobtitle", "operator": "CONTAINS_TOKEN", "value": "ceo"}]}], "properties": ["firstname", "lastname", "email", "jobtitle"]}` (for initial discovery)

6.  **Batch Update for Normalization**:
    *   After identifying contacts and their normalized values, use the batch update API.
    *   **API Pattern**: `POST $HUBSPOT_BASE_URL/crm/v3/objects/contacts/batch/update`
    *   **Payload**: A list of objects, each containing an `id` and `properties` with the new, normalized values.
    *   **Constraint**: Maximum 100 contacts per batch request. Implement pagination and rate limiting.

7.  **Always Run `DRY_RUN=true` First and Confirm**:
    *   **Critical Step**: Before making any live changes, always perform a dry run. If the API supports it, use a `DRY_RUN` parameter. If not, simulate the changes and *print the proposed changes to the user for explicit confirmation*.
    *   **Process**: Fetch the current values, calculate the proposed normalized values, display a diff or a list of `Contact ID | Old Value | New Value`.
    *   Only proceed with the actual update after the user has explicitly confirmed the changes.

### Best Practices for AI Agent
*   Provide clear definitions of the canonical values and mappings used for normalization.
*   Offer to create custom mappings based on user input.
*   Clearly communicate the number of records that will be affected by a normalization operation.
*   Log all changes made for auditing and potential rollback.
