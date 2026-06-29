import requests
from bs4 import BeautifulSoup
import pandas as pd

def run_lead_scraper(business_type, location):
    data = []
    # Google Maps Search URL
    query = f"{business_type} in {location}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=lcl"
    
    # Browser ki tarah act karne ke liye headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Results ko dhoondna
        listings = soup.select('.rllt__details')
        
        for item in listings[:20]:
            name = item.select_one('.OSrXXb').text if item.select_one('.OSrXXb') else "N/A"
            # Requests method se phone/website directly nahi milti, 
            # isliye hum yahan "Check Website" show kar rahe hain
            data.append({
                "Business Name": name,
                "Phone": "Check Business Site",
                "Address": "Check Business Site",
                "Website": "Check Business Site"
            })
            
    except Exception as e:
        print(f"Error: {e}")
        
    return pd.DataFrame(data)
