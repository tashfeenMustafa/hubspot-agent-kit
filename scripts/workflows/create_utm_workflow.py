import os
import requests
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

# Set DISABLE_SSL_VERIFY=true only for local Windows dev with SSL issues. Never in production.
DISABLE_SSL_VERIFY = os.getenv("DISABLE_SSL_VERIFY", "false").lower() == "true"

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", "https://api.hubapi.com")
DRY_RUN_DEFAULT = os.getenv("DRY_RUN", "True").lower() == "true"

PLATFORM_CONFIGS = {
    "meta": {
        "canonical_source": "meta",
        "canonical_medium": "paid_social",
        "non_canonical_sources": ["facebook", "fb", "instagram", "ig", "Meta"]
    },
    "google": {
        "canonical_source": "google",
        "canonical_medium": "cpc",
        "non_canonical_sources": ["googleads", "adwords"]
    },
    "linkedin": {
        "canonical_source": "linkedin",
        "canonical_medium": "paid_social",
        "non_canonical_sources": ["linkedin_ads"]
    }
}

def build_utm_workflow_payload(platform_config):
    canonical_source = platform_config["canonical_source"]
    canonical_medium = platform_config["canonical_medium"]
    non_canonical_sources = platform_config["non_canonical_sources"]

    workflow_name = f"UTM Normalization - {canonical_source.title()} - Auto-generated"

    # HubSpot API v4 workflow structure
    payload = {
        "name": workflow_name,
        "type": "CONTACT_FLOW",
        "isEnabled": True,
        "reEnrollmentSettings": {
            "allowContactToReEnroll": True,
            "reEnrollmentTrigger": "CONTACT_PROPERTY_CHANGE" # Example, can be refined
        },
        "trigger": {
            "type": "FILTER_BASED_ENROLLMENT",
            "filterConditions": [
                {
                    "operator": "IN",
                    "property": "utm_source",
                    "value": non_canonical_sources
                }
            ]
        },
        "suppressionFilters": [
            {
                "operator": "EQ",
                "property": "utm_source",
                "value": canonical_source
            }
        ],
        "actions": [
            {
                "type": "SET_PROPERTY",
                "propertyName": "utm_source",
                "value": canonical_source
            },
            {
                "type": "SET_PROPERTY",
                "propertyName": "utm_medium",
                "value": canonical_medium
            }
        ]
    }
    return payload

def create_workflow(api_key, base_url, payload, dry_run):
    """Creates a workflow in HubSpot or prints the payload if dry_run is True."""
    if not api_key:
        print("Error: HUBSPOT_API_KEY environment variable not set.")
        return

    if dry_run:
        print("Dry run: Workflow payload would be posted to HubSpot:")
        print(json.dumps(payload, indent=2))
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Windows SSL workaround - remove in production
        response = requests.post(f"{base_url}/automation/v4/flows", headers=headers, json=payload, verify=(not DISABLE_SSL_VERIFY))
        response.raise_for_status()
        print("Workflow created successfully:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error creating workflow: {e}")

def main():
    parser = argparse.ArgumentParser(description="Deploy a UTM normalization workflow for a given platform.")
    parser.add_argument("--platform", choices=PLATFORM_CONFIGS.keys(), required=True, 
                        help="Platform to create UTM workflow for (meta|google|linkedin).")
    parser.add_argument("--live", action="store_true", help="Execute live API call instead of dry run. Overrides DRY_RUN env var.")
    args = parser.parse_args()

    platform = args.platform
    platform_config = PLATFORM_CONFIGS.get(platform)

    if not platform_config:
        print(f"Error: Invalid platform '{platform}'. Choose from {', '.join(PLATFORM_CONFIGS.keys())}.")
        return
    
    dry_run = DRY_RUN_DEFAULT and not args.live

    print(f"Preparing UTM normalization workflow for {platform.title()}...")
    workflow_payload = build_utm_workflow_payload(platform_config)
    create_workflow(HUBSPOT_API_KEY, HUBSPOT_BASE_URL, workflow_payload, dry_run)

if __name__ == "__main__":
    main()
