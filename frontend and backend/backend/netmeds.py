from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, re

def get_medicine_price(medicine_name: str, max_results: int = 5):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(options=options)
    
    try:
        # Use correct URL format
        search_url = f"https://www.netmeds.com/products/?q={medicine_name.replace(' ', '%20')}"
        print(f"Searching: {search_url}\n")
        driver.get(search_url)

        # Wait longer for JavaScript to render
        print("Waiting for products to load...")
        time.sleep(10)
        
        # Scroll to trigger lazy loading
        driver.execute_script("window.scrollTo(0, 1200);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 2400);")
        time.sleep(2)

        # Get HTML
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find product containers - try multiple patterns
        product_cards = []
        
        # Try finding by common Netmeds patterns
        patterns_to_try = [
            soup.find_all("div", {"class": re.compile(r"product.*card", re.I)}),
            soup.find_all("div", {"class": re.compile(r"ais-Hits-item")}),
            soup.find_all("li", {"class": re.compile(r"item.*product", re.I)}),
            soup.find_all("div", {"data-sku": True}),  # Products often have SKU
            soup.find_all("div", {"class": re.compile(r"search.*item", re.I)}),
        ]
        
        for attempt in patterns_to_try:
            if len(attempt) >= max_results:
                product_cards = attempt
                break
        
        # If still not found, try broader search
        if not product_cards:
            all_divs = soup.find_all("div", class_=True)
            # Look for divs that contain both product name and price
            for div in all_divs:
                text = div.get_text()
                if "₹" in text and len(text) > 20 and len(text) < 500:
                    product_cards.append(div)
                if len(product_cards) >= max_results * 2:  # Get extra to filter
                    break

        if not product_cards:
            print("❌ No products found!")
            print("\n📊 Debug: Checking for common elements...")
            # Check what's actually on the page
            price_elements = soup.find_all(string=re.compile(r"₹"))
            print(f"Found {len(price_elements)} elements with ₹ symbol")
            if price_elements:
                print("Sample text:", price_elements[0][:100] if price_elements else "None")
            return []

        print(f"Found {len(product_cards)} potential products\n")
        print(f"Extracting top {min(max_results, len(product_cards))} results:\n")
        print("=" * 70)
        
        result = []
        seen_names = set()
        
        for card in product_cards:
            if len(result) >= max_results:
                break
            
            # Get all text from card
            card_text = card.get_text(separator="|", strip=True)
            
            # Extract name - look for longer text segments
            name = "Unknown"
            possible_names = []
            
            # Try different name selectors
            for tag in card.find_all(["a", "h2", "h3", "span", "p"]):
                text = tag.get_text(strip=True)
                # Valid name: 10-150 chars, contains letters, not just numbers/symbols
                if 10 < len(text) < 150 and any(c.isalpha() for c in text):
                    if not any(skip in text.lower() for skip in ["add to", "cart", "buy now", "off", "save"]):
                        possible_names.append(text)
            
            # Pick the longest valid name (usually most descriptive)
            if possible_names:
                name = max(possible_names, key=len)
            
            # Skip if duplicate or invalid
            if name in seen_names or name == "Unknown":
                continue
            seen_names.add(name)
            
            # Extract ALL prices from card
            prices_found = re.findall(r'₹\s*(\d+(?:,\d+)*(?:\.\d{1,2})?)', card_text)
            prices_clean = [float(p.replace(',', '')) for p in prices_found]
            prices_clean = sorted(set(prices_clean))  # Remove duplicates and sort
            
            # Extract discount percentage first
            discount = None
            discount_percent = None
            disc_match = re.search(r'(\d+)%\s*[Oo]ff', card_text)
            if disc_match:
                discount_percent = int(disc_match.group(1))
                discount = f"{discount_percent}% off"
            
            # Fix: Correct price indexing (0-based indexing)
            if len(prices_clean) >= 2:
                # Both prices are shown - first is selling price, second is MRP
                selling_price = prices_clean[0]
                mrp = prices_clean[1]
            elif len(prices_clean) == 1 and discount_percent:
                # Only discounted price shown, back-calculate MRP
                selling_price = prices_clean[0]
                # Formula: selling_price = mrp * (1 - discount/100)
                # So: mrp = selling_price / (1 - discount/100)
                mrp = round(selling_price / (1 - discount_percent/100), 2)
            elif len(prices_clean) == 1:
                # Only one price, no discount
                selling_price = prices_clean[0]
                mrp = selling_price
            else:
                selling_price = None
                mrp = None
            
            # Only add if we have meaningful data
            if selling_price and name != "Unknown":
                print(f"\n[{len(result) + 1}] {name}")
                print(f"Selling Price (After Discount): ₹{selling_price}")
                if mrp and mrp != selling_price:
                    print(f" MRP (Original Price): ₹{mrp}")
                    savings = mrp - selling_price
                    print(f"You Save: ₹{savings:.2f}")
                if discount:
                    print(f"Discount: {discount}")
                print("-" * 70)
                
                # Fix: Safe discount calculation
                discount_value = None
                savings_value = None
                
                if mrp and mrp > 0 and mrp != selling_price:
                    savings_value = round(mrp - selling_price, 2)
                    discount_value = int((savings_value * 100) / mrp)
                
                result.append({
                    "name": name,
                    "selling_price": selling_price,
                    "MRP": mrp if (mrp and mrp != selling_price) else None,
                    "Discount": discount_value,
                    "savings": savings_value
                })
        
        if len(result) == 0:
            print("\nCould not extract valid product data.")
            print("The website structure may have changed or requires login.")
            print("Try: Remove '--headless=new' to see what actually loads in browser")
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    finally:
        driver.quit()

if __name__ == "__main__":
    medicine = input("Enter medicine name: ").strip()
    if medicine:
        results = get_medicine_price(medicine, max_results=5)
        print(f"\n{'='*70}")
        print(f"Successfully extracted {len(results)} unique products")
        print(f"{'='*70}")
    else:
        print("Please enter a medicine name")
