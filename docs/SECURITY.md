# Security Guide for HubSpot Agent Kit Users

This document outlines essential security practices for users of the `hubspot-agent-kit` to ensure safe and responsible interaction with HubSpot APIs.

## 1. Environment Variables and Sensitive Data

*   **Never Commit `.env` Files:** Always ensure your `.gitignore` file includes `.env` to prevent accidentally committing files containing sensitive credentials to version control. This is enforced for your protection.
*   **Private App Tokens:** Always use HubSpot Private App tokens for authentication. Avoid using legacy API keys, which are less secure and have broader permissions.
*   **No Logging/Output of API Keys:** Never log API keys, access tokens, or other sensitive credentials to console output, logs, or include them in any agent responses or generated content. Implement strict sanitization.
*   **Key Rotation:** If an API key is accidentally committed or exposed, rotate it immediately in HubSpot and update all relevant configurations.

## 2. API Scopes and Permissions

*   **Minimum Required Scopes:** When creating HubSpot Private Apps, grant only the absolute minimum required scopes for each specific skill or operation. Adhere to the principle of least privilege.

## 3. Safe Execution with `DRY_RUN`

*   **`DRY_RUN=true` (Default):** The `hubspot-agent-kit` defaults to a `DRY_RUN` mode for all write operations. This means actions will be simulated, and their intended effects will be reported without actually modifying data in HubSpot.
*   **Always Verify:** Before running any operation with `--live` (or equivalent parameter to disable dry run), meticulously verify the `DRY_RUN` output. Ensure the planned changes align with your expectations and business rules.
*   **Use `--live` with Caution:** Only execute operations with `--live` after thorough verification and understanding of their impact.

## 4. Secure Practices in CI/CD (GitHub Actions Example)

*   **Repository Secrets:** When using CI/CD pipelines (e.g., GitHub Actions), store HubSpot API keys and other sensitive credentials as repository secrets. Never hardcode these values directly into workflow YAML files.
*   **Secure Environment:** Ensure your CI/CD environment is properly secured and follows best practices for secret management.

## 5. SSL/TLS Verification

*   **`verify=False` is a Development Workaround:** The note about `requests(..., verify=False)` for Windows SSL issues is strictly a development workaround. This disables SSL certificate verification, making your connection vulnerable to man-in-the-middle attacks.
*   **Production Requirements:** In production environments, always ensure proper SSL certificate handling. Do not disable `verify` for production API calls. Configure your environment to trust valid certificate authorities.
