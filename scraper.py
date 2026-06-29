from playwright.sync_api import sync_playwright
import pandas as pd

def run_lead_scraper(business_type, location):
    data = []
    with sync_playwright() as p:
        # Browser launch with reduced memory footprint for VPS
        browser = p.chromium.launch(headless=True, args=[
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-sandbox",
            "--single-process"
        ])
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        # Google Maps URL
        query = f"{business_type} in {location}"
        page.goto(f"https://www.google.com/maps/search/{query.replace(' ', '+')}")
        page.wait_for_timeout(5000)
        
        # 1. Scroll karne ka logic taake 20+ results load ho jayen
        scroll_container = page.locator('div[role="feed"]')
        for _ in range(3): # 3 baar scroll karega taake list lambi ho jaye
            scroll_container.evaluate("node => node.scrollTop = node.scrollHeight")
            page.wait_for_timeout(3000)
        
        # 2. Results selectors
        listings = page.locator('a.hfpxzc').all()
        
        # 3. 20 results tak scrape karein
        for listing in listings[:20]: 
            try:
                listing.click()
                page.wait_for_timeout(3000)
                
                name = page.locator('h1.DUwDvf').inner_text() if page.locator('h1.DUwDvf').count() > 0 else "N/A"
                phone = page.locator('button[aria-label^="Phone:"]').get_attribute('aria-label') if page.locator('button[aria-label^="Phone:"]').count() > 0 else "N/A"
                address = page.locator('button[aria-label^="Address:"]').get_attribute('aria-label') if page.locator('button[aria-label^="Address:"]').count() > 0 else "N/A"
                website = page.locator('a[aria-label^="Website:"]').get_attribute('href') if page.locator('a[aria-label^="Website:"]').count() > 0 else "N/A"
                
                data.append({
                    "Business Name": name, 
                    "Phone": phone.replace("Phone: ", ""), 
                    "Address": address.replace("Address: ", ""), 
                    "Website": website
                })
            except: continue
        browser.close()
    return pd.DataFrame(data)