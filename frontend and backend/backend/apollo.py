from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


def scrape_apollo(medicine_name: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        search_url = f"https://www.apollopharmacy.in/search-medicines/{medicine_name.replace(' ', '%20')}"
        driver.get(search_url)
        time.sleep(5)  # Wait for JS-rendered content to appear

        # ✅ Extract full visible text
        full_text = driver.find_element("tag name", "body").text
        text_clean = re.sub(r"\s+", " ", full_text)
        tokens = text_clean.split()

        # Find where the medicine name occurs
        med_tokens = medicine_name.lower().split()
        found_indices = []
        for i in range(len(tokens) - len(med_tokens)):
            snippet = " ".join(tokens[i:i + len(med_tokens)]).lower()
            if all(word in snippet for word in med_tokens):
                found_indices.append(i)

        results = []
        for idx in found_indices:
            window = tokens[idx:idx + 20]  # Look a bit wider
            snippet = " ".join(window)

            if "₹" not in snippet:
                continue

            # Extract price values
            prices = re.findall(r'₹\s*([\d.,]+)', snippet)
            discount = re.search(r'(\d+)%\s*off', snippet)
            discount = discount.group(1) if discount else None

            mrp = price = None
            if len(prices) >= 2:
                try:
                    vals = [float(p.replace(',', '')) for p in prices[:2]]
                    mrp, price = (max(vals), min(vals))
                except:
                    mrp, price = prices[0], prices[1]
            elif len(prices) == 1:
                price = prices[0]

            results.append({
                "name": snippet,
                "MRP": mrp,
                "Discount": discount,
                "selling_price": price
            })

        # ✅ Deduplicate by identical price (only after we have valid results)
        unique_results = []
        seen_prices = set()
        for r in results:
            price_val = str(r["selling_price"])
            if not price_val or price_val in seen_prices:
                continue
            seen_prices.add(price_val)
            unique_results.append(r)

        # ✅ Sort by price and limit to top 5
        try:
            unique_results = sorted(
                unique_results,
                key=lambda x: float(str(x["selling_price"]).replace(',', '') or 0)
            )[:5]
        except:
            pass

        # ✅ Output
        if not unique_results:
            print("⚠️ No valid matches found for", medicine_name)
        else:
            print(f"✅ Found {len(unique_results)} unique results for '{medicine_name}' in apollo:\n")
            for r in unique_results:
                print("------")
                print(r["name"])
                print(f"MRP: {r['MRP'] or '-'} | Discount: {r['Discount'] or '-'}% | Final Price: {r['selling_price'] or '-'}")

        return unique_results

    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    medicine = input("Enter medicine name: ").strip()
    scrape_apollo(medicine)
