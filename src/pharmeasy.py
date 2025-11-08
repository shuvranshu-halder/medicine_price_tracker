from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time


def get_medicine_price(medicine_name: str):
    # Setup Chrome options
    options = Options()
    # 🚫 Remove headless for dynamic rendering
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--start-maximized")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    driver = webdriver.Chrome(options=options)

    try:
        search_url = f"https://pharmeasy.in/search/all?name={medicine_name.replace(' ', '%20')}"
        driver.get(search_url)

        print(f"Searching PharmEasy for: {medicine_name} ...")

        # Wait for main content container (not specific cards yet)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ProductCard_medicineUnitWrapper__"))
        )

        # Retry loop for lazy-loaded products
        for i in range(10):  # Try for ~10 seconds
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            products = soup.find_all('div', class_=lambda x: x and 'ProductCard_medicineUnitWrapper' in x)
            if len(products) >= 5:
                break
            time.sleep(1)

        if not products:
            print(f"No medicine named '{medicine_name}' found.")
            return

        print(f"\nTop results for '{medicine_name}':\n")

        for p in products[:5]:
            name_tag = p.find('a', {'class': lambda x: x and 'ProductCard_medicineName' in x})
            name = name_tag.get_text(strip=True) if name_tag else "Unknown"

            text = p.get_text(separator=' ').strip()
            prices = re.findall(r'₹\s*([\d,]+)', text)
            discount = re.search(r'(\d+)%\s*OFF', text, re.IGNORECASE)

            mrp = float(prices[0].replace(',', '')) if len(prices) >= 1 else None
            actual_price = float(prices[1].replace(',', '')) if len(prices) >= 2 else None
            discount_percent = float(discount.group(1)) if discount else None

            if actual_price and mrp and actual_price > mrp:
                mrp, actual_price = actual_price, mrp

            print(f"Name: {name}")
            print(f"Price after discount: ₹{actual_price if actual_price else 'N/A'}")
            print(f"MRP: ₹{mrp if mrp else 'N/A'}")
            print(f"Discount: {discount_percent if discount_percent else 'N/A'}%")
            print('-' * 50)

    except Exception as e:
        print(f"⚠️ Error: {type(e).__name__} - {e}")

    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    med = input("Enter medicine name: ")
    get_medicine_price(med)
