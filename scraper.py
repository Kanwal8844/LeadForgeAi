from serpapi import GoogleSearch
import pandas as pd

def run_lead_scraper(business_type, location):
    # Free tier wali API key yahan rakhein
    params = {
      "engine": "google_maps",
      "q": f"{business_type} in {location}",
      "api_key": "APNI_SERPAPI_KEY_YAHAN_DAALEIN" 
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    leads = []
    # Google Maps ke local_results se data uthayein
    for place in results.get("local_results", []):
        leads.append({
            "Business Name": place.get("title"),
            "Phone": place.get("phone"),
            "Address": place.get("address"),
            "Website": place.get("website")
        })
    return pd.DataFrame(leads)
