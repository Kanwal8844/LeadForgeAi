import requests
from bs4 import BeautifulSoup
import pandas as pd

def run_lead_scraper(business_type, location):
    data = []
    # Google Maps ki jagah Google Search se data uthayenge
    query = f"{business_type} in {location}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google search results se text nikalna
        results = soup.select('.tF2Cxc') 
        
        for item in results[:10]:
            name = item.select_one('h3').text if item.select_one('h3') else "N/A"
            data.append({
                "Business Name": name,
                "Phone": "Manual Check",
                "Address": "Manual Check",
                "Website": "Check result"
            })
            
    except Exception as e:
        print(f"Error: {e}")
        
    return pd.DataFrame(data)
