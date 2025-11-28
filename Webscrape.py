
import asyncio
from playwright.async_api import async_playwright
import os

from bs4 import BeautifulSoup
import pandas as pd
import re


URL = "https://www.ebay.ie/sch/i.html?_nkw=iphone+17"
SAVE_PATH = "/Users/harshith1004/Documents/scrapped.html"   
USER_DATA_DIR = "/Users/harshith1004/Documents/playwright_profile" 
HEADLESS = True                         

async def scrape_page(url):
    # Start Playwright
    async with async_playwright() as p:
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=HEADLESS,
        )

        # Open a new tab
        page = await context.new_page()

        
        print("Opening page:", url)
        await page.goto(url)

        
        await asyncio.sleep(5)

        html = await page.content()


        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            f.write(html)

        print("HTML saved at:", SAVE_PATH)

        
        await context.close()
        return html
        


#if __name__ == "__main__":
    #asyncio.run(scrape_page(URL))

"""MERGED RWO SEPRATE CODE INOTN ONE """


def extract_data(html):
    soup = BeautifulSoup(html, "lxml")

    items = soup.select(".srp-results li.s-card")
    print(f"Found {len(items)} items")

    results = []

    for item in items:
        # Name / Title
        title_span = item.select_one(".srp-results .s-card__title span.primary")
        title = title_span.text.strip() if title_span else None

        # Price
        price_span = item.select_one(".su-card-container__attributes__primary .s-card__price")
        price = price_span.text.strip() if price_span else None

        # Postage and Location
        postage = None
        location = None
        attr_rows = item.select(".s-card__attribute-row .su-styled-text.secondary.large")
        for row in attr_rows:
            text = row.text.strip()
            if "postage" in text.lower():
                postage = text
            elif "from" in text.lower():
                location = text

        # Condition
        condition_span = item.select_one(".s-card__subtitle span")
        condition = condition_span.text.strip() if condition_span else None

        
#AFTER FIRST REVIEW
        
        # Advanced Extraction
        model = "Unknown"
        storage = "Unknown"
        color = "Unknown"
        network = "Unknown"

        if title:
            # Model
            model_match = re.search(r"(iPhone\s?\d+\s?(?:Pro|Max|Plus|Air|Mini)?)", title, re.IGNORECASE)
            if model_match:
                model = model_match.group(1)
            
            # Storage
            storage_match = re.search(r"(\d+\s?(?:GB|TB))", title, re.IGNORECASE)
            if storage_match:
                storage = storage_match.group(1).upper().replace(" ", "")

            # Color
            color_match = re.search(r"(Black|White|Blue|Natural|Titanium|Orange|Sage|Silver|Gold|Grey|Green|Pink|Purple|Red|Yellow)", title, re.IGNORECASE)
            if color_match:
                color = color_match.group(1).title()

        results.append({
            "Model": model,
            "Storage": storage,
            "Color": color,
            "Network": network,
            "Price": price,
            "Condition": condition,
            "Location": location,
            "Postage": postage,
            #"Original_Title": title
        })

    return pd.DataFrame(results)

async def main():
    html_content = await scrape_page(URL)
    df = extract_data(html_content)
    
    # Save to CSV
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    csv_path = os.path.join(results_dir, "ebay_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
    
    pd.set_option("display.max_colwidth", None)
    print(df.head(100))

if __name__ == "__main__":
    asyncio.run(main())
