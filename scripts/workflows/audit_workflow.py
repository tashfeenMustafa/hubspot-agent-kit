import os
import requests
import json
import argparse
from dotenv import load_dotenv
from tabulate import tabulate
from ..audit import fetch_portal_context # Import relative to scripts/

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", "https://api.hubapi.com")

# Define simplified audit rules (placeholder for full 38 rules)
# Each rule is a dictionary with id, name, description, severity, check_function
AUDIT_RULES = [
    {
        "id": "WF001",
        "name": "Workflow Active with No Enrollments (90d)",
        "description": "Identifies active workflows that have not enrolled any contacts in the last 90 days.",
        "severity": "MEDIUM",
        "check_function": lambda w, ctx: w.get("is_active") and w.get("enrollment_count_90d", 0) == 0
    },
    {
        "id": "WF002",
        "name": "Workflow Missing Name Prefix",
        "description": "Checks if the workflow name follows a naming convention (e.g., starts with a bracketed prefix).\nPlease adjust prefix logic in script to match your convention.",
        "severity": "LOW",
        "check_function": lambda w, ctx: not w.get("name", "").strip().startswith("[")
    },
    {
        "id": "WF003",
        "name": "Workflow with Potential Re-enrollment Issues",
        "description": "Flags workflows that might have re-enrollment enabled, which can lead to loops if not carefully designed.",
        "severity": "MEDIUM",
        "check_function": lambda w, ctx: w.get("is_active") and w.get("type") == "CONTACT_FLOW" and "reEnrollment" in json.dumps(w)
    },
    {
        "id": "WF004",
        "name": "Workflow with Missing Contact Property Action",
        "description": "Checks for workflows that set a contact property that does not exist in the portal context.",
        "severity": "HIGH",
        "check_function": lambda w, ctx:
            any(
                action.get("type") == "SET_PROPERTY" and
                action.get("propertyName") and
                action.get("objectType") == "CONTACT" and # Assume CONTACT for simplicity, needs more robust parsing
                action["propertyName"] not in [p["name"] for p in ctx.get("contact_properties", [])]
                for action in w.get("actions", [])
            ) if ctx.get("contact_properties") else False
    },
    # Add more rules as needed, up to 38
]

def fetch_workflow_by_id(workflow_id, api_key, base_url):
    # Fetches a single workflow by its ID.
    if not api_key:
        print("Error: HUBSPOT_API_KEY environment variable not set.")
        return None

    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        # Windows SSL workaround - remove in production
        response = requests.get(f"{base_url}/automation/v4/flows/{workflow_id}", headers=headers, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching workflow {workflow_id}: {e}")
        return None

def run_audit_rules(workflow, portal_context):
    # Runs all audit rules against a single workflow and returns violations.
    violations = []
    for rule in AUDIT_RULES:
        try:
            if rule["check_function"](workflow, portal_context):
                violations.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "description": rule["description"],
                    "severity": rule["severity"]
                })
        except Exception as e:
            print(f"Error running rule {rule["id"]} on workflow {workflow.get("id")}: {e}")
    return violations

def main():
    parser = argparse.ArgumentParser(description="Audit a single HubSpot workflow by ID.")
    parser.add_argument("--workflow-id", required=True, help="The ID of the workflow to audit.")
    parser.add_argument("--portal-context-file", default="portal_context.json", 
                        help="Path to a JSON file containing portal context (default: portal_context.json).")
    args = parser.parse_args()

    workflow_id = args.workflow_id
    portal_context_file = args.portal_context_file

    # Fetch portal context
    print(f"Attempting to load portal context from {portal_context_file}...")
    portal_context = None
    if os.path.exists(portal_context_file):
        with open(portal_context_file, "r") as f:
            portal_context = json.load(f)
        print("Portal context loaded.")
    else:
        print(f"Warning: Portal context file not found at {portal_context_file}. ")
        print("Consider running fetch_portal_context.py to generate it first.")
        # Attempt to fetch basic context if file not found to allow some rules to run
        print("Fetching minimal portal context via API for basic checks...")
        contact_props_data = fetch_portal_context.get_contact_properties(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)
        if contact_props_data and "results" in contact_props_data:
            portal_context = {"contact_properties": contact_props_data["results"]}
        else:
            portal_context = {}

    if not portal_context:
        print("Error: Could not obtain portal context. Exiting.")
        exit(1)

    # Fetch workflow
    print(f"Fetching workflow {workflow_id}...")
    workflow = fetch_workflow_by_id(workflow_id, HUBSPOT_API_KEY, HUBSPOT_BASE_URL)

    if not workflow:
        print(f"Workflow with ID {workflow_id} not found or inaccessible. Exiting.")
        exit(1)

    print(f"Auditing workflow '{workflow.get("name", workflow_id)}' (ID: {workflow_id})...")
    violations = run_audit_rules(workflow, portal_context)

    if violations:
        print("\nWorkflow Audit Violations:")
        headers = ["Rule ID", "Severity", "Rule Name", "Description"]
        table_data = []
        has_critical_or_high = False
        for v in violations:
            table_data.append([
                v["rule_id"],
                v["severity"],
                v["rule_name"],
                v["description"]
            ])
            if v["severity"] in ["CRITICAL", "HIGH"]:
                has_critical_or_high = True
        
        print(tabulate(table_data, headers=headers, tablefmt="pipe"))

        if has_critical_or_high:
            print("\nWARNING: CRITICAL or HIGH severity issues found. Exiting with code 1.")
            exit(1)
    else:
        print("\nNo audit violations found for this workflow.")

if __name__ == "__main__":
    main()
