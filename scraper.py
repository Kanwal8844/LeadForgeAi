import requests
import pandas as pd

def run_lead_scraper(business_type, location):
    # Overpass API ka URL
    url = "https://overpass-api.de/api/interpreter"
    
    # Humne query ko dynamic banaya hai taake har business type ke liye chale
    # 'craft' aur 'shop' tags mein zyadatar plumbers, electricians, etc mil jate hain
    query = f"""
    [out:json][timeout:25];
    area[name="{location}"]->.searchArea;
    (
      node["craft"="{business_type.lower()}"](area.searchArea);
      node["shop"="{business_type.lower()}"](area.searchArea);
      node["amenity"="{business_type.lower()}"](area.searchArea);
    );
    out body;
    """
    
    try:
        response = requests.get(url, params={'data': query})
        data = response.json()
        
        leads = []
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            # Agar naam mil jaye to data list mein daal dein
            if 'name' in tags:
                leads.append({
                    "Business Name": tags.get('name', 'N/A'),
                    "Phone": tags.get('phone', 'N/A'),
                    "Address": tags.get('addr:street', 'N/A'),
                    "Website": tags.get('website', 'N/A')
                })
        
        return pd.DataFrame(leads)
        
    except Exception as e:
        print(f"Scraping Error: {e}")
        return pd.DataFrame()
