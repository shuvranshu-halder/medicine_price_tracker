from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re


def scrape_pharmeasy(medicine_name):
    
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    medicines = []

    try:
  
        search_url = f"https://pharmeasy.in/search/all?name={medicine_name.replace('%', '%25').replace(' ', '%20')}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 15)

        
        time.sleep(4)

        
        product_cards = []
        try:
            product_cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='Search_medicineUnitWrapper']")
        except:
            pass

        if not product_cards:
            try:
                product_cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='ProductCard_container']")
            except:
                pass

        if not product_cards:
            try:
                product_cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='ProductCard']")
            except:
                pass

        print(f"Found {len(product_cards)} product cards")

        # Track unique medicines by name to avoid duplicates
        seen_names = set()

        
        for card in product_cards:
            if len(medicines) >= 3:
                break

            try:
                medicine_data = {}

                
                try:
                    name_elem = card.find_element(By.CSS_SELECTOR,
                                                  "h1[class*='medicineName'], h2[class*='medicineName'], div[class*='medicineName'], a[class*='medicineName']")
                    medicine_data['name'] = name_elem.text.strip()
                except:
                    try:
                        name_elem = card.find_element(By.TAG_NAME, "h1")
                        medicine_data['name'] = name_elem.text.strip()
                    except:
                        medicine_data['name'] = "N/A"

                # Skip if duplicate
                if medicine_data['name'] in seen_names or medicine_data['name'] == "N/A":
                    continue

                # MRP (original price)
                try:
                    mrp_elem = card.find_element(By.CSS_SELECTOR,
                                                 "span[class*='striked'], span[class*='mrp'], span[class*='Prices_slashedPrice']")
                    mrp_text = mrp_elem.text.strip()
                    mrp_value = re.search(r'[\d,]+\.?\d*', mrp_text.replace(',', ''))
                    medicine_data['MRP'] = float(mrp_value.group()) if mrp_value else 0
                except:
                    medicine_data['MRP'] = 0

                # Get selling price
                try:
                    price_elem = card.find_element(By.CSS_SELECTOR,
                                                   "div[class*='ourPrice'], span[class*='ourPrice'], div[class*='Prices_ourPrice']")
                    price_text = price_elem.text.strip()
                    price_value = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                    medicine_data['selling_price'] = float(price_value.group()) if price_value else 0
                except:
                    medicine_data['selling_price'] = 0

                # Get discount percentage
                try:
                    discount_elem = card.find_element(By.CSS_SELECTOR,
                                                      "span[class*='discount'], div[class*='discount'], span[class*='percentageDiscount']")
                    discount_text = discount_elem.text.strip()
                    discount_value = re.search(r'(\d+)%', discount_text)
                    medicine_data['Discount'] = int(discount_value.group(1)) if discount_value else 0
                except:
                    # Calculate discount if not directly available
                    if medicine_data['MRP'] > 0 and medicine_data['selling_price'] > 0:
                        discount = ((medicine_data['MRP'] - medicine_data['selling_price']) / medicine_data[
                            'MRP']) * 100
                        medicine_data['Discount'] = round(discount, 1)
                    else:
                        medicine_data['Discount'] = 0

                # Only add if we have valid data
                if medicine_data['selling_price'] > 0:
                    medicines.append(medicine_data)
                    seen_names.add(medicine_data['name'])
                    print(f"Added: {medicine_data['name']}")

            except Exception as e:
                print(f"Error parsing card: {e}")
                continue

    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()

    return medicines


def display_results(medicines):
    """Display scraped medicines in a formatted way"""
    if not medicines:
        print("No medicines found!")
        return

    print(f"\n{'=' * 80}")
    print(f"Found {len(medicines)} medicine(s):")
    print(f"{'=' * 80}\n")

    for i, med in enumerate(medicines, 1):
        print(f"{i}. {med['name']}")
        print(f"   MRP: ₹{med['MRP']:.2f}")
        print(f"   Selling Price: ₹{med['selling_price']:.2f}")
        print(f"   Discount: {med['discount']}%")
        # print(f"   Savings: ₹{med['mrp'] - med['selling_price']:.2f}")
        print("-" * 80)


# if __name__ == "__main__":
#     # Get user input
#     medicine_name = input("Enter medicine name to search: ").strip()

#     if not medicine_name:
#         print("Please enter a valid medicine name!")
#     else:
#         print(f"\nSearching for '{medicine_name}' on PharmEasy...")
#         results = scrape_pharmeasy(medicine_name)
#         display_results(results)