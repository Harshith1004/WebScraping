
import asyncio
from playwright.async_api import async_playwright
import os


URL = "https://www.ebay.ie/sch/i.html?_nkw=iphone+17"
SAVE_PATH = "/Users/harshith1004/Documents/scrapped.html"   
USER_DATA_DIR = "/Users/harshith1004/Documents/playwright_profile" 
HEADLESS = False                         

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


if __name__ == "__main__":
    asyncio.run(scrape_page(URL))
