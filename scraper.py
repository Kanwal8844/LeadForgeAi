import requests
import pandas as pd

def run_lead_scraper(business_type, location):
    # Overpass API URL
    url = "https://overpass-api.de/api/interpreter"
    
    # Ye Query hai jo city aur business type dhundti hai
    # 'amenity' ya 'shop' tags use hote hain
    query = f"""
    [out:json];
    area[name="{location}"];
    (
      node["amenity"="{business_type}"](area);
      node["shop"="{business_type}"](area);
    );
    out body;
    """
    
    try:
        response = requests.get(url, params={'data': query})
        data = response.json()
        
        leads = []
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            leads.append({
                "Business Name": tags.get('name', 'N/A'),
                "Phone": tags.get('phone', 'N/A'),
                "Address": tags.get('addr:street', 'N/A'),
                "Website": tags.get('website', 'N/A')
            })
            
        return pd.DataFrame(leads)
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
