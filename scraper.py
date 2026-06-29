import requests
from bs4 import BeautifulSoup
import pandas as pd

def run_lead_scraper(business_type, location):
    data = []
    # Google Maps ke bajaye Google Search URL
    query = f"{business_type} in {location}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    # Headers ko update kiya hai taake Google block na kare
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google ke organic results se headings nikalna
        results = soup.find_all('div', class_='g')
        
        for item in results:
            name_tag = item.find('h3')
            if name_tag:
                name = name_tag.text
                data.append({
                    "Business Name": name,
                    "Phone": "N/A (Use Maps)",
                    "Address": "N/A (Use Maps)",
                    "Website": "Check result"
                })
        
        # Agar list khali ho, to error message check karein
        if not data:
            print("No data found, check selectors.")
            
    except Exception as e:
        print(f"Error: {e}")
        
    return pd.DataFrame(data)
