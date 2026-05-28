import os
import requests
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", "https://api.hubapi.com")
DRY_RUN_DEFAULT = os.getenv("DRY_RUN", "True").lower() == "true"

# Normalization functions
def normalize_job_title(title):
    if not title: return None
    title = title.strip().lower()
    mappings = {
        "ceo": "CEO", "chief executive officer": "CEO",
        "cto": "CTO", "chief technology officer": "CTO",
        "cfo": "CFO", "chief financial officer": "CFO",
        "coo": "COO", "chief operating officer": "COO",
        "vp": "VP", "vice president": "VP",
        "director": "Director",
        "manager": "Manager",
        "engineer": "Engineer",
        "developer": "Developer",
        "analyst": "Analyst",
        "consultant": "Consultant",
        "sales": "Sales Representative",
        "marketing": "Marketing Specialist",
        "owner": "Owner",
        "founder": "Founder"
    }
    for k, v in mappings.items():
        if k in title:
            return v
    return title.title() # Capitalize first letter of each word

def normalize_annual_revenue(revenue):
    if not revenue: return None
    try:
        return float(revenue)
    except ValueError:
        return None

def normalize_team_size(size):
    if not size: return None
    try:
        return int(size)
    except ValueError:
        return None

def normalize_business_category(category):
    if not category: return None
    category = category.strip().lower()
    mappings = {
        "tech": "Technology", "it": "Technology", "software": "Technology",
        "finance": "Finance", "banking": "Finance",
        "health": "Healthcare", "medical": "Healthcare",
        "retail": "Retail", "e-commerce": "Retail",
        "education": "Education", "university": "Education",
        "manufacturing": "Manufacturing",
        "consulting": "Consulting"
    }
    return mappings.get(category, category.title())

NORMALIZATION_FUNCTIONS = {
    "job_title": normalize_job_title,
    "annual_revenue": normalize_annual_revenue,
    "team_size": normalize_team_size,
    "business_category": normalize_business_category,
}

def search_contacts(api_key, base_url, property_name):
    """Searches for contacts where the specified property is not null."""
    if not api_key:
        print("Error: HUBSPOT_API_KEY environment variable not set.")
        return []

    all_contacts = []
    after_cursor = None
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    while True:
        search_body = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": property_name,
                            "operator": "HAS_PROPERTY"
                        }
                    ]
                }
            ],
            "properties": [property_name],
            "limit": 100
        }
        if after_cursor:
            search_body["after"] = after_cursor

        try:
            # Windows SSL workaround - remove in production
            response = requests.post(f"{base_url}/crm/v3/objects/contacts/search", 
                                     headers=headers, json=search_body, verify=False)
            response.raise_for_status()
            data = response.json()
            all_contacts.extend(data.get("results", []))
            after_cursor = data.get("paging", {}).get("next", {}).get("after")
            if not after_cursor:
                break
        except requests.exceptions.RequestException as e:
            print(f"Error searching contacts: {e}")
            break
    return all_contacts

def batch_update_contacts(api_key, base_url, updates, dry_run):
    """Performs a batch update on contacts or prints the payload if dry_run is True."""
    if not api_key:
        print("Error: HUBSPOT_API_KEY environment variable not set.")
        return

    if not updates:
        print("No updates to perform.")
        return

    if dry_run:
        print("Dry run: Batch update payload would be posted to HubSpot:")
        print(json.dumps(updates, indent=2))
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # HubSpot batch update limit is 100
    for i in range(0, len(updates), 100):
        batch = updates[i:i + 100]
        batch_payload = {"inputs": batch}
        try:
            # Windows SSL workaround - remove in production
            response = requests.post(f"{base_url}/crm/v3/objects/contacts/batch/update", 
                                     headers=headers, json=batch_payload, verify=False)
            response.raise_for_status()
            print(f"Successfully updated {len(batch)} contacts.")
        except requests.exceptions.RequestException as e:
            print(f"Error in batch update for contacts: {e}")
            print(f"Problematic batch: {json.dumps(batch_payload, indent=2)}")

def main():
    parser = argparse.ArgumentParser(description="Bulk-normalize contact properties.")
    parser.add_argument("--property", choices=NORMALIZATION_FUNCTIONS.keys(), required=True,
                        help="Contact property to normalize (job_title|annual_revenue|team_size|business_category).")
    parser.add_argument("--live", action="store_true", help="Execute live API calls instead of dry run. Overrides DRY_RUN env var.")
    args = parser.parse_args()

    property_name = args.property
    normalize_func = NORMALIZATION_FUNCTIONS[property_name]
    dry_run = DRY_RUN_DEFAULT and not args.live

    print(f"Searching for contacts with non-null '{property_name}'...")
    contacts = search_contacts(HUBSPOT_API_KEY, HUBSPOT_BASE_URL, property_name)
    print(f"Found {len(contacts)} contacts to potentially normalize.")

    updates = []
    for contact in contacts:
        contact_id = contact["id"]
        current_value = contact["properties"].get(property_name)
        normalized_value = normalize_func(current_value)

        if current_value != normalized_value:
            updates.append({"id": contact_id, "properties": {property_name: normalized_value}})
            if dry_run:
                print(f"Contact ID: {contact_id}, Old: '{current_value}', New: '{normalized_value}'")
    
    print(f"Preparing to update {len(updates)} contacts.")
    batch_update_contacts(HUBSPOT_API_KEY, HUBSPOT_BASE_URL, updates, dry_run)

    if dry_run:
        print("Normalization dry run complete. No changes were made to HubSpot.")
    else:
        print("Normalization process complete.")

if __name__ == "__main__":
    main()
