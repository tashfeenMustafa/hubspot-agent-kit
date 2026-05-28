import os
import requests
import json
import argparse
from dotenv import load_dotenv
from datetime import datetime, timedelta
from tabulate import tabulate

load_dotenv()

# Set DISABLE_SSL_VERIFY=true only for local Windows dev with SSL issues. Never in production.
DISABLE_SSL_VERIFY = os.getenv("DISABLE_SSL_VERIFY", "false").lower() == "true"

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", "https://api.hubapi.com")
DRY_RUN_DEFAULT = os.getenv("DRY_RUN", "True").lower() == "true"

def fetch_objects(object_type, api_key, base_url, filters=None, properties=None):
    """Generic function to fetch objects with pagination and filters."""
    if not api_key:
        print("Error: HUBSPOT_API_KEY environment variable not set.")
        return []

    all_objects = []
    after_cursor = None
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    while True:
        search_body = {"limit": 100}
        if properties:
            search_body["properties"] = properties
        if filters:
            search_body["filterGroups"] = [{
                "filters": filters
            }]
        if after_cursor:
            search_body["after"] = after_cursor

        try:
            # Windows SSL workaround - remove in production
            response = requests.post(f"{base_url}/crm/v3/objects/{object_type}/search", 
                                     headers=headers, json=search_body, verify=(not DISABLE_SSL_VERIFY))
            response.raise_for_status()
            data = response.json()
            all_objects.extend(data.get("results", []))
            after_cursor = data.get("paging", {}).get("next", {}).get("after")
            if not after_cursor:
                break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {object_type}: {e}")
            break
    return all_objects

def check_orphan_deals(api_key, base_url):
    """Finds deals with no associated contacts."""
    print("Checking for orphan deals...")
    # HubSpot search API doesn't allow direct filtering on association count, requires post-processing
    deals = fetch_objects("deals", api_key, base_url, properties=["dealname"])
    orphan_deals = []
    for deal in deals:
        # Fetch associations for each deal - this can be slow for many deals
        # In a real-world scenario, you might optimize this with batch association fetching if API supports it
        try:
            # Windows SSL workaround - remove in production
            response = requests.get(f"{base_url}/crm/v3/objects/deals/{deal['id']}/associations/contacts",
                                    headers={"Authorization": f"Bearer {api_key}"}, verify=(not DISABLE_SSL_VERIFY))
            response.raise_for_status()
            associations = response.json()
            if not associations.get("results"):
                orphan_deals.append(deal)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching associations for deal {deal.get('id')}: {e}")
            continue
    return orphan_deals

def check_missing_associations(api_key, base_url):
    """Finds contacts at 'salesqualifiedlead' lifecycle stage with no associated deals."""
    print("Checking for contacts with missing deal associations...")
    filters = [
        {
            "propertyName": "hs_lifecycle_stage",
            "operator": "EQ",
            "value": "salesqualifiedlead"
        }
    ]
    contacts = fetch_objects("contacts", api_key, base_url, filters=filters, properties=["firstname", "lastname", "email"])
    missing_associations_contacts = []
    for contact in contacts:
        try:
            # Windows SSL workaround - remove in production
            response = requests.get(f"{base_url}/crm/v3/objects/contacts/{contact['id']}/associations/deals",
                                    headers={"Authorization": f"Bearer {api_key}"}, verify=(not DISABLE_SSL_VERIFY))
            response.raise_for_status()
            associations = response.json()
            if not associations.get("results"):
                missing_associations_contacts.append(contact)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching associations for contact {contact.get('id')}: {e}")
            continue
    return missing_associations_contacts

def check_zombie_contacts(api_key, base_url):
    """Finds contacts with 'attempted_to_contact' status and no activity in last 90 days."""
    print("Checking for zombie contacts...")
    ninety_days_ago = (datetime.now() - timedelta(days=90)).isoformat() + "Z"

    filters = [
        {
            "propertyName": "hs_lead_status",
            "operator": "EQ",
            "value": "ATTEMPTED_TO_CONTACT"
        },
        {
            "propertyName": "hs_last_activity_date",
            "operator": "LT", # Less than 90 days ago
            "value": ninety_days_ago
        }
    ]
    contacts = fetch_objects("contacts", api_key, base_url, filters=filters, properties=["firstname", "lastname", "email", "hs_last_activity_date"])
    return contacts

def generate_hygiene_report(orphan_deals, missing_associations_contacts, zombie_contacts):
    """Generates a Markdown report of CRM hygiene issues."""
    report = ["# CRM Hygiene Report\n"]

    if orphan_deals:
        report.append(f"## Orphan Deals ({len(orphan_deals)} found)\n")
        report.append("Deals with no associated contacts. Consider associating them or closing them.\n")
        headers = ["Deal ID", "Deal Name"]
        table_data = [[d["id"], d["properties"].get("dealname", "N/A")] for d in orphan_deals[:5]] # Sample 5
        report.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report.append("\n")

    if missing_associations_contacts:
        report.append(f"## Contacts with Missing Deal Associations ({len(missing_associations_contacts)} found)\n")
        report.append("Contacts at 'Sales Qualified Lead' stage with no associated deals. Investigate why no deal exists.\n")
        headers = ["Contact ID", "Name", "Email"]
        table_data = [[c["id"], f"{c['properties'].get('firstname', '')} {c['properties'].get('lastname', '')}".strip(), c["properties"].get("email", "N/A")] for c in missing_associations_contacts[:5]] # Sample 5
        report.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report.append("\n")

    if zombie_contacts:
        report.append(f"## Zombie Contacts ({len(zombie_contacts)} found)\n")
        report.append("Contacts with 'Attempted to Contact' status and no activity in the last 90 days. Consider re-engaging or marking as stale.\n")
        headers = ["Contact ID", "Name", "Email", "Last Activity"]
        table_data = [[c["id"], f"{c['properties'].get('firstname', '')} {c['properties'].get('lastname', '')}".strip(), c["properties"].get("email", "N/A"), c["properties"].get("hs_last_activity_date", "N/A")] for c in zombie_contacts[:5]] # Sample 5
        report.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report.append("\n")

    if not any([orphan_deals, missing_associations_contacts, zombie_contacts]):
        report.append("No CRM hygiene issues found!\n")

    return "\n".join(report)

def fix_orphan_deals(api_key, base_url, deals_to_fix, dry_run):
    if not deals_to_fix: return
    print(f"Attempting to close {len(deals_to_fix)} orphan deals...")
    updates = []
    for deal in deals_to_fix:
        updates.append({"id": deal["id"], "properties": {"dealstage": "closedlost", "hs_lastmodifieddate": datetime.now().isoformat() + "Z"}})
    
    if dry_run:
        print("Dry run: Would update deals with: ")
        print(json.dumps(updates, indent=2))
        return

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    for i in range(0, len(updates), 100):
        batch = updates[i:i + 100]
        batch_payload = {"inputs": batch}
        try:
            # Windows SSL workaround - remove in production
            response = requests.post(f"{base_url}/crm/v3/objects/deals/batch/update", 
                                     headers=headers, json=batch_payload, verify=(not DISABLE_SSL_VERIFY))
            response.raise_for_status()
            print(f"Successfully closed {len(batch)} orphan deals.")
        except requests.exceptions.RequestException as e:
            print(f"Error closing orphan deals: {e}")

def fix_zombie_contacts(api_key, base_url, contacts_to_fix, dry_run):
    if not contacts_to_fix: return
    print(f"Attempting to mark {len(contacts_to_fix)} zombie contacts as 'Stale Lead'...")
    updates = []
    for contact in contacts_to_fix:
        updates.append({"id": contact["id"], "properties": {"hs_lead_status": "STALE_LEAD"}})

    if dry_run:
        print("Dry run: Would update contacts with: ")
        print(json.dumps(updates, indent=2))
        return

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    for i in range(0, len(updates), 100):
        batch = updates[i:i + 100]
        batch_payload = {"inputs": batch}
        try:
            # Windows SSL workaround - remove in production
            response = requests.post(f"{base_url}/crm/v3/objects/contacts/batch/update", 
                                     headers=headers, json=batch_payload, verify=(not DISABLE_SSL_VERIFY))
            response.raise_for_status()
            print(f"Successfully updated {len(batch)} zombie contacts to 'Stale Lead'.")
        except requests.exceptions.RequestException as e:
            print(f"Error updating zombie contacts: {e}")

def main():
    parser = argparse.ArgumentParser(description="Find and optionally fix CRM hygiene issues.")
    parser.add_argument("--check", choices=["orphan-deals", "missing-associations", "zombie-contacts", "all"], 
                        default="all", help="Which hygiene check(s) to perform.")
    parser.add_argument("--live", action="store_true", help="Execute live API calls instead of dry run. Overrides DRY_RUN env var.")
    parser.add_argument("--fix", action="store_true", help="Attempt automated fixes for found issues (requires --live). ")
    args = parser.parse_args()

    dry_run = DRY_RUN_DEFAULT and not args.live
    if args.fix and dry_run:
        print("Error: --fix flag requires --live flag to be set. Aborting.")
        exit(1)

    orphan_deals = []
    missing_associations_contacts = []
    zombie_contacts = []

    if args.check in ["orphan-deals", "all"]:
        orphan_deals = check_orphan_deals(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)

    if args.check in ["missing-associations", "all"]:
        missing_associations_contacts = check_missing_associations(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)

    if args.check in ["zombie-contacts", "all"]:
        zombie_contacts = check_zombie_contacts(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)
    
    print("\n--- CRM Hygiene Report ---")
    report_markdown = generate_hygiene_report(orphan_deals, missing_associations_contacts, zombie_contacts)
    print(report_markdown)

    if args.fix and not dry_run:
        print("\n--- Attempting Automated Fixes ---")
        if orphan_deals:
            confirm = input(f"Found {len(orphan_deals)} orphan deals. Do you want to close them as 'closedlost'? (yes/no): ")
            if confirm.lower() == "yes":
                fix_orphan_deals(HUBSPOT_API_KEY, HUBSPOT_BASE_URL, orphan_deals, dry_run)
        
        if zombie_contacts:
            confirm = input(f"Found {len(zombie_contacts)} zombie contacts. Do you want to set their lead status to 'Stale Lead'? (yes/no): ")
            if confirm.lower() == "yes":
                fix_zombie_contacts(HUBSPOT_API_KEY, HUBSPOT_BASE_URL, zombie_contacts, dry_run)

    if dry_run:
        print("\nCRM Hygiene dry run complete. No changes were made to HubSpot.")
    else:
        print("\nCRM Hygiene checks complete.")

if __name__ == "__main__":
    main()
