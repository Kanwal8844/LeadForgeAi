import requests
import pandas as pd

def run_lead_scraper(business_type, location):
    print(f"DEBUG: Scraper initiated for {business_type} in {location}")
    url = "https://overpass-api.de/api/interpreter"
    
    # Query ko robust banaya hai: nwr matlab Node, Way, Relation (OSM ka har data)
    # [timeout:30] server ko time dega data dhundne ke liye
    query = f"""
    [out:json][timeout:30];
    area[name="{location}"]->.searchArea;
    (
      nwr["amenity"~"{business_type}",i](area.searchArea);
      nwr["shop"~"{business_type}",i](area.searchArea);
      nwr["craft"~"{business_type}",i](area.searchArea);
    );
    out body;
    """
    
    try:
        response = requests.get(url, params={'data': query})
        print(f"DEBUG: API Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print("DEBUG: API Connection Failed")
            return pd.DataFrame()

        data = response.json()
        elements = data.get('elements', [])
        print(f"DEBUG: Elements found: {len(elements)}")
        
        leads = []
        for element in elements:
            tags = element.get('tags', {})
            # Sirf wo results uthayein jin ka naam mojood ho
            if 'name' in tags:
                leads.append({
                    "Business Name": tags.get('name', 'N/A'),
                    "Phone": tags.get('phone', tags.get('contact:phone', 'N/A')),
                    "Address": tags.get('addr:street', 'N/A'),
                    "Website": tags.get('website', 'N/A')
                })
        
        return pd.DataFrame(leads)
        
    except Exception as e:
        print(f"DEBUG: Error occurred: {e}")
        return pd.DataFrame()
