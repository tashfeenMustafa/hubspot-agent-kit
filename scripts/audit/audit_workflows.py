import os
import requests
import json
import argparse
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", "https://api.hubapi.com")

def get_workflows(api_key, base_url):
    """Fetches all workflows from HubSpot Automation API v4 with pagination."""
    if not api_key:
        print("Error: HUBSPOT_API_KEY environment variable not set.")
        return []

    all_workflows = []
    after_cursor = None
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    while True:
        params = {"limit": 100}
        if after_cursor:
            params["after"] = after_cursor

        try:
            # Windows SSL workaround - remove in production
            response = requests.get(f"{base_url}/automation/v4/flows", headers=headers, params=params, verify=False)
            response.raise_for_status()
            data = response.json()
            all_workflows.extend(data.get("results", []))
            after_cursor = data.get("paging", {}).get("next", {}).get("after")
            if not after_cursor:
                break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching workflows: {e}")
            break
    return all_workflows

def audit_workflow(workflow):
    """Runs basic health checks on a single workflow."""
    flags = []
    
    # Flag: active with 0 enrollments (zombie)
    if workflow.get("is_active") and workflow.get("enrollment_count_90d", 0) == 0:
        flags.append("ZOMBIE_ACTIVE_NO_ENROLLMENTS")

    # Flag: No name prefix (assuming a convention like "[Marketing] Workflow Name")
    if not workflow.get("name", "").strip().startswith("["):
        flags.append("NO_NAME_PREFIX")

    # Flag: Re-enrollment enabled for terminal workflows (might cause loops if not carefully designed)
    # This check is an example and might need refinement based on actual re-enrollment logic in payload.
    # For now, a simplified check.
    # A more robust check would involve parsing workflow JSON to see specific re-enrollment settings.
    # The 'reEnrollment' key is not directly available in top-level workflow properties from v4 API,
    # it's usually part of specific triggers or actions. This is a heuristic.
    if workflow.get("is_active") and workflow.get("type") == "CONTACT_FLOW" and "reEnrollment" in json.dumps(workflow):
        flags.append("POTENTIAL_REENROLLMENT_ON_TERMINAL_WORKFLOW")

    return {
        "id": workflow.get("id"),
        "name": workflow.get("name"),
        "type": workflow.get("type"),
        "is_active": workflow.get("is_active"),
        "enrollment_count_90d": workflow.get("enrollment_count_90d"),
        "action_count": len(workflow.get("actions", [])), # Placeholder, actual actions need to be parsed
        "flags": flags,
        "raw_workflow": workflow # For --dump option
    }

def generate_markdown_report(audited_workflows):
    """Generates a Markdown summary report."""
    report = ["# HubSpot Workflow Audit Report\n"]
    
    zombie_workflows = [w for w in audited_workflows if "ZOMBIE_ACTIVE_NO_ENROLLMENTS" in w["flags"]]
    if zombie_workflows:
        report.append("## Zombie Workflows (Active with 0 Enrollments in last 90 days)\n")
        headers = ["ID", "Name", "Type", "Active", "Enrollments (90d)"]
        table_data = [[w["id"], w["name"], w["type"], w["is_active"], w["enrollment_count_90d"]] for w in zombie_workflows]
        report.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report.append("\n")

    no_prefix_workflows = [w for w in audited_workflows if "NO_NAME_PREFIX" in w["flags"]]
    if no_prefix_workflows:
        report.append("## Workflows Without Name Prefixes\n")
        headers = ["ID", "Name", "Type"]
        table_data = [[w["id"], w["name"], w["type"]] for w in no_prefix_workflows]
        report.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report.append("\n")

    reenrollment_warnings = [w for w in audited_workflows if "POTENTIAL_REENROLLMENT_ON_TERMINAL_WORKFLOW" in w["flags"]]
    if reenrollment_warnings:
        report.append("## Workflows with Potential Re-enrollment Issues\n")
        report.append("These workflows might need review to prevent unintended re-enrollments or loops. This is a heuristic check.\n")
        headers = ["ID", "Name", "Type", "Active"]
        table_data = [[w["id"], w["name"], w["type"], w["is_active"]] for w in reenrollment_warnings]
        report.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report.append("\n")

    report.append("## All Workflows Summary\n")
    headers = ["ID", "Name", "Type", "Active", "Enrollments (90d)", "Action Count", "Flags"]
    table_data = []
    for w in audited_workflows:
        table_data.append([
            w["id"], w["name"], w["type"], w["is_active"], 
            w["enrollment_count_90d"], w["action_count"], ", ".join(w["flags"])
        ])
    report.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
    report.append("\n")

    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Audit HubSpot workflows.")
    parser.add_argument("--output", help="Output JSON report to a file.")
    parser.add_argument("--report", help="Output Markdown summary report to a file.")
    parser.add_argument("--dump", action="store_true", help="Dump full raw workflow JSON in the output report.")
    args = parser.parse_args()

    workflows = get_workflows(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)
    if not workflows:
        print("No workflows found or API key missing. Exiting.")
        return

    audited_workflows = [audit_workflow(w) for w in workflows]

    if not args.dump:
        for w in audited_workflows:
            w.pop("raw_workflow", None)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(audited_workflows, f, indent=2)
        print(f"JSON report written to {args.output}")
    else:
        print(json.dumps(audited_workflows, indent=2))

    if args.report:
        markdown_report = generate_markdown_report(audited_workflows)
        with open(args.report, "w") as f:
            f.write(markdown_report)
        print(f"Markdown summary report written to {args.report}")

if __name__ == "__main__":
    main()
