from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_medicine_price(medicine_name: str):
    # Setup Chrome options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        search_url = f"https://www.1mg.com/search/all?name={medicine_name.replace(' ', '%20')}"
        driver.get(search_url)
        time.sleep(10)  # Wait for JavaScript to render fully

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Try to locate product containers
        products = soup.find_all('div', {'class': lambda x: x and 'ProductCard' in x})
        if not products:
            products = soup.find_all('a', {'href': lambda x: x and '/drugs/' in x})

        if not products:
            print(f"No medicine named '{medicine_name}' found.")
            return

        print(f"Top results for '{medicine_name}':\n")
        for p in products[:5]:
            text = p.get_text(separator=' ').strip()
            if '₹' in text:
                name = text.split('₹')[0].strip()
                price = '₹' + text.split('₹')[1].split()[0]
                print(f"{name}: {price}")

    finally:
        driver.quit()


# Example usage
if __name__ == "_main_":
    med = input("Enter medicine name: ")
    get_medicine_price(med)
