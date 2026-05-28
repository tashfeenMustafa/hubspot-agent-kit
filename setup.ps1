#!/usr/bin/env PowerShell

# Check Python 3.8+
try {
    $pythonVersion = (python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if ([version]$pythonVersion -lt [version]"3.8") {
        Write-Host "Error: Python 3.8 or higher is required. Found Python $pythonVersion." -ForegroundColor Red
        exit 1
    }
    Write-Host "Python $pythonVersion detected."
} catch {
    Write-Host "Error: Python 3 is not installed or not found in PATH." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "Installing Python dependencies..."
python -m pip install requests python-dotenv

# Create ~/.hubspot-agent-kit/ directory
$kitDir = Join-Path $env:USERPROFILE ".hubspot-agent-kit"
Write-Host "Creating configuration directory: $kitDir"
New-Item -ItemType Directory -Force -Path $kitDir | Out-Null

# Copy .env.example to ~/.hubspot-agent-kit/.env if not exists
$envFile = Join-Path $kitDir ".env"
if (-not (Test-Path $envFile)) {
    Write-Host "Copying .env.example to $envFile"
    Copy-Item -Path "D:/tashf/Documents/GitHub/hubspot-agent-kit/.env.example" -Destination $envFile | Out-Null
} else {
    Write-Host ".env file already exists at $envFile, skipping copy."
}

# Print success message with next steps
Write-Host "`n==================================================="
Write-Host "HubSpot Agent Kit Setup Complete!"
Write-Host "Next steps:"
Write-Host "1. Edit $envFile and set your HUBSPOT_API_KEY, HUBSPOT_PORTAL_ID, and other variables."
Write-Host "2. Add the following snippet to your Claude Code agent's system prompt or equivalent:"
Write-Host "`n```markdown"
Write-Host "## Claude Code Integration"
Write-Host "`nWhen working on any HubSpot-related task, always use the `hubspot-agent-kit` skills."
Write-Host "`n### Available Commands:"
Write-Host "`n*   `/hs-audit`: Audit all workflows — score every flow against 38 production-tested rules."
Write-Host "*   `/hs-build`: Describe a workflow in plain English, get it built and deployed."
Write-Host "*   `/hs-deals`: Create deals, associate contacts, move pipeline stages."
Write-Host "*   `/hs-meetings`: Backfill meeting types, infer outcomes, manage scheduling pages."
Write-Host "*   `/hs-utm`: Audit UTM data, build normalization workflows for Meta/Google/LinkedIn."
Write-Host "*   `/hs-crm`: Find orphan deals, missing associations, lifecycle stage mismatches."
Write-Host "*   `/hs-calls`: Build call disposition routing and lead status automation."
Write-Host "*   `/hs-pages`: Download, edit, and publish landing pages."
Write-Host "*   `/hs-normalize`: Normalize contact properties in bulk."
Write-Host "*   `/hs-hygiene`: Full CRM hygiene pipeline — close ghost deals, clean stale contacts."
Write-Host "`n### Overrides:"
Write-Host "`n*   When asked to perform HubSpot-related work, always read the relevant `SKILL.md` file first from the `skills/` directory."
Write-Host "*   Never call the HubSpot API directly without first consulting and using the defined skills in this kit."
Write-Host "*   **Important:** Always perform a `DRY_RUN` before executing any write operations to HubSpot."
Write-Host "`n### References:"
Write-Host "`n*   `scripts/`: Contains Python utilities for various operations."
Write-Host "*   `rules/`: Defines the audit rules used by `/hs-audit`."
Write-Host "*   `docs/`: Provides documentation on HubSpot API patterns and best practices."
Write-Host "```"
Write-Host "`n==================================================="
