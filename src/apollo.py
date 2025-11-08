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
        search_url = f"https://www.apollopharmacy.in/search-medicines/{medicine_name.replace(' ', '%20')}"
        driver.get(search_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Let JS render results
        time.sleep(8)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Try to locate product containers
        products = soup.find_all('div', {'class': lambda x: x and 'ProductCard' in x})
        if not products:
            products = soup.find_all('a', {'href': lambda x: x and '/drugs/' in x})
            # print("first if not products")
            print(f"No medicine named '{medicine_name}' found.")
            return

        print(f"Top results for '{medicine_name}':\n")
        for p in products[:1]:
            # print(p)
            text = p.get_text(separator=' ').strip()
            if '₹' in text:
                name = text.split('₹')[0].strip()
                price = '₹' + text.split('₹')[1].split()[0]
                # price=text.split('off')[1]
                print(f"{name}: {price}")
            # print("-----------------")

    finally:
        driver.quit()


if __name__ == "__main__":
    med = input("Enter medicine name: ")
    get_medicine_price(med)
