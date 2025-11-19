from bs4 import BeautifulSoup
import pandas as pd

html_path = "/Users/harshith1004/Documents/scrapped.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

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

    results.append({
        "Name": title,
        "Price": price,
        "Postage": postage,
        "Condition": condition,
        "Location": location
    })

# Convert to DataFrame
df = pd.DataFrame(results)
pd.set_option("display.max_colwidth", None)
df.head(100)
