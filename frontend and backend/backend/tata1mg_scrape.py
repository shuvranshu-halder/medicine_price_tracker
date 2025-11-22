from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

def scrape_tata1mg(medicine_name: str):
    # Setup Chrome options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    driver = webdriver.Chrome(options=options)

    try:
        search_url = f"https://www.1mg.com/search/all?name={medicine_name.replace('%', '%25').replace(' ', '%20')}"
        driver.get(search_url)
        time.sleep(4)  # Wait for JavaScript to render fully

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Try to locate product containers
        products = soup.find_all('div', {'class': lambda x: x and 'ProductCard' in x})
        if not products:
            products = soup.find_all('a', {'href': lambda x: x and '/drugs/' in x})
            # print("first if not products")

        if not products:
            print(f"No medicine named '{medicine_name}' found.")
            return

        print(f"Top results for '{medicine_name}' in tata1mg:\n")
        result=[]
        for p in products[:3]:
            text = p.get_text(separator=' ').strip()

            # Extract medicine name (first few words before ₹)
            name_match = re.match(r'([A-Za-z0-9\s\-\+]+)', text)
            name = name_match.group(1).strip() if name_match else "Unknown"

            # Extract all ₹ values and discount %
            prices = re.findall(r'₹\s*([\d.]+)', text)
            discount = re.search(r'(\d+)%\s*off', text)

            mrp = float(prices[0]) if len(prices) >= 1 else None
            actual_price = float(prices[1]) if len(prices) >= 2 else None
            discount_percent = float(discount.group(1)) if discount else None

            if discount_percent is not None:
                if mrp > actual_price:
                    pass
                else:
                    (mrp, actual_price) = (actual_price, mrp)

            print(f"Name: {name}")
            print(f"Price after discount: ₹{actual_price}")
            print(f"MRP: ₹{mrp}")
            print(f"Discount: {discount_percent}%")
            print('-' * 40)
            result.append({
                "name": name,
                "MRP": mrp,
                "Discount": discount_percent,
                "selling_price": actual_price
            }) 
        return result
    finally:
        driver.quit()


# Example usage
# if __name__ == "__main__":
#     med = input("Enter medicine name: ")
#     scrape_tata1mg(med)
