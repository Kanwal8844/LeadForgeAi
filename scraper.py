import requests
import pandas as pd

def run_lead_scraper(business_type, location):
    url = "https://overpass-api.de/api/interpreter"
    
    # Hum ne query ko mazeed smart bana diya hai
    # Ye 'craft', 'shop', aur 'amenity' teeno check karega
    query = f"""
    [out:json][timeout:25];
    area[name="{location}"]->.searchArea;
    (
      nwr["craft"~"{business_type}",i](area.searchArea);
      nwr["shop"~"{business_type}",i](area.searchArea);
      nwr["amenity"~"{business_type}",i](area.searchArea);
    );
    out body;
    """
    
    try:
        response = requests.get(url, params={'data': query})
        data = response.json()
        
        leads = []
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            # Hum name aur phone dono dhoondenge
            if 'name' in tags:
                leads.append({
                    "Business Name": tags.get('name', 'N/A'),
                    "Phone": tags.get('phone', tags.get('contact:phone', 'N/A')),
                    "Address": tags.get('addr:street', 'N/A'),
                    "Website": tags.get('website', 'N/A')
                })
        
        return pd.DataFrame(leads)
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
