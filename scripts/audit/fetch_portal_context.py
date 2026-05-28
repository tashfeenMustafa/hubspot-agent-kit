import os
import requests
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", "https://api.hubapi.com")

def fetch_data(url, api_key, params=None):
    """Helper function to fetch data from HubSpot API."""
    if not api_key:
        print("Error: HUBSPOT_API_KEY environment variable not set.")
        return None

    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        # Windows SSL workaround - remove in production
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def get_contact_properties(api_key, base_url):
    """Fetches all contact properties."""
    return fetch_data(f"{base_url}/crm/v3/properties/contacts", api_key)

def get_deal_properties(api_key, base_url):
    """Fetches all deal properties."""
    return fetch_data(f"{base_url}/crm/v3/properties/deals", api_key)

def get_deal_pipelines(api_key, base_url):
    """Fetches all deal pipelines and their stages."""
    pipelines_data = fetch_data(f"{base_url}/crm/v3/pipelines/deals", api_key)
    pipelines = []
    pipeline_stages = {}
    if pipelines_data and "results" in pipelines_data:
        for p in pipelines_data["results"]:
            pipelines.append({"id": p["id"], "label": p["label"]})
            pipeline_stages[p["id"]] = [{
                "id": s["id"], "label": s["label"], "value": s["metadata"].get("value")
            } for s in p.get("stages", [])]
    return pipelines, pipeline_stages

def get_static_lists(api_key, base_url):
    """Fetches all static contact lists."""
    return fetch_data(f"{base_url}/contacts/v1/lists/all/lists/static", api_key)

def main():
    parser = argparse.ArgumentParser(description="Fetch HubSpot portal context.")
    parser.add_argument("--output", required=True, help="Output JSON file for portal context.")
    args = parser.parse_args()

    portal_context = {
        "contact_properties": [],
        "deal_properties": [],
        "pipelines": [],
        "pipeline_stages": {},
        "lists": []
    }

    print("Fetching contact properties...")
    contact_props = get_contact_properties(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)
    if contact_props and "results" in contact_props:
        portal_context["contact_properties"] = contact_props["results"]
    
    print("Fetching deal properties...")
    deal_props = get_deal_properties(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)
    if deal_props and "results" in deal_props:
        portal_context["deal_properties"] = deal_props["results"]

    print("Fetching deal pipelines and stages...")
    pipelines, pipeline_stages = get_deal_pipelines(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)
    portal_context["pipelines"] = pipelines
    portal_context["pipeline_stages"] = pipeline_stages

    print("Fetching static lists...")
    static_lists = get_static_lists(HUBSPOT_API_KEY, HUBSPOT_BASE_URL)
    if static_lists and "lists" in static_lists:
        portal_context["lists"] = static_lists["lists"]

    with open(args.output, "w") as f:
        json.dump(portal_context, f, indent=2)
    print(f"Portal context successfully written to {args.output}")

if __name__ == "__main__":
    main()
