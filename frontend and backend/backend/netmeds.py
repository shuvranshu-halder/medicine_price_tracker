from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, re

def get_medicine_price(medicine_name: str, max_results: int = 1):
    # --- Chrome configuration ---
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(options=options)
    try:
        search_url = f"https://www.netmeds.com/products?q={medicine_name.replace(' ', '%20')}"
        driver.get(search_url)

        # Let JS render results
        time.sleep(8)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        html = driver.execute_script("return document.body.innerHTML;")
        soup = BeautifulSoup(html, "html.parser")

        # ✅ Find each medicine card
        product_cards = soup.find_all("div", class_=lambda c: c and "product-card" in c)

        if not product_cards:
            print(f"⚠️ No medicine results found for '{medicine_name}'. Try increasing sleep time slightly.")
            return

        print(f"\nTop {min(max_results, len(product_cards))} results for '{medicine_name} in netmeds':\n")
        result=[]
        for card in product_cards[:max_results]:
            
            # --- Medicine name ---
            name_tag = card.find(["a", "span", "p"], string=True)
            name = "Unknown"
            if name_tag:
                # Filter out empty or generic text
                name = name_tag.get_text(strip=True)
                # Skip irrelevant strings like "Add to Cart"
                if len(name) < 3 or "Add" in name:
                    name = "Unknown"

            # --- Price and MRP ---
            text = card.get_text(separator=" ").strip()
            prices = re.findall(r"₹\s*([\d,.]+)", text)
            actual_price = prices[0] if len(prices) >= 1 else None
            mrp = prices[1] if len(prices) >= 2 else None

            # --- Discount ---
            discount = None
            disc_tag = card.find("span", class_=lambda c: c and "discount" in c)
            if disc_tag:
                discount = disc_tag.get_text(strip=True)

            print(f"Name: {name}")
            print(f"Price after discount: ₹{actual_price}")
            # print(f"MRP: ₹{mrp}")
            print(f"Discount: {discount}")
            print("-" * 40)
            result.append({
                "name": name,
                "MRP": mrp,
                "Discount": discount,
                "selling_price": actual_price
            })
        return result
    except Exception as e:
        print("❌ Error:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    med = input("Enter medicine name: ")
    get_medicine_price(med)
