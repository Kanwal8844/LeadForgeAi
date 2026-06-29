import requests
from bs4 import BeautifulSoup
import pandas as pd

def run_lead_scraper(business_type, location):
    data = []
    # Google Search URL
    query = f"{business_type} in {location}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Google search results ke links dhoondna
        results = soup.select('div.tF2Cxc')
        for item in results:
            title = item.select_one('h3').text if item.select_one('h3') else "N/A"
            data.append({"Business Name": title, "Phone": "N/A", "Address": "N/A", "Website": "N/A"})
    except:
        pass
    return pd.DataFrame(data)
