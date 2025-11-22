from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re
from bs4 import BeautifulSoup

def scrape_apollo(medicine_name: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        search_url = f"https://www.apollopharmacy.in/search-medicines/{medicine_name.replace(' ', '%20')}"
        print(f"\n🔍 Searching Apollo Pharmacy for: {medicine_name}")
        print(f"URL: {search_url}\n")
        
        driver.get(search_url)
        
        # Wait longer for page to load
        time.sleep(7)
        
        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Strategy 1: Try multiple product card selectors
        product_selectors = [
            "[class*='ProductCard']",
            "[class*='product-card']", 
            "[class*='productCard']",
            ".product",
            "[class*='Product_container']",
            "article",
            "[data-qa*='product']"
        ]
        
        products = []
        for selector in product_selectors:
            products = soup.select(selector)
            if products:
                print(f"✅ Found {len(products)} products using selector: {selector}")
                break
        
        # Strategy 2: If no products found, try fallback text parsing
        if not products:
            print("⚠️ No product cards found, attempting text-based extraction...")
            return extract_from_text(page_source, medicine_name)
        
        results = []
        
        for product in products[:15]:  # Process first 15 products
            try:
                product_text = product.get_text(separator=' ', strip=True)
                
                # Extract product name (usually the longest text before price)
                name_candidates = []
                for tag in ['h2', 'h3', 'h4', 'a', 'span', 'div']:
                    name_elems = product.select(tag)
                    for elem in name_elems:
                        text = elem.get_text(strip=True)
                        if text and len(text) > 10 and len(text) < 150:
                            if '₹' not in text and '%' not in text:
                                name_candidates.append(text)
                
                product_name = name_candidates[0] if name_candidates else product_text[:100]
                
                # Extract prices
                price_matches = re.findall(r'₹\s*([\d,]+(?:\.\d{2})?)', product_text)
                
                if not price_matches:
                    continue
                
                # Convert to floats
                prices = []
                for p in price_matches:
                    try:
                        prices.append(float(p.replace(',', '')))
                    except:
                        continue
                
                if not prices:
                    continue
                
                # Determine MRP and selling price
                if len(prices) >= 2:
                    mrp = max(prices[:2])
                    price = min(prices[:2])
                elif len(prices) == 1:
                    price = prices[0]
                    mrp = None
                else:
                    continue
                
                # Calculate discount
                discount = None
                discount_match = re.search(r'(\d+)\s*%\s*(?:off|OFF)', product_text)
                if discount_match:
                    discount = float(discount_match.group(1))
                elif mrp and price and mrp > price:
                    discount = round(((mrp - price) / mrp) * 100, 1)
                
                results.append({
                    "name": product_name,
                    "MRP": mrp,
                    "Discount": discount,
                    "selling_price": price
                })
                
            except Exception as e:
                continue
        
        # Deduplicate by name and price
        unique_results = []
        seen = set()
        for r in results:
            key = (r["name"][:50], r["selling_price"])
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        # Sort by price
        unique_results = sorted(unique_results, key=lambda x: x["selling_price"])[:5]
        
        # Display results
        print(f"{'='*70}")
        print(f"Apollo Pharmacy Results: {medicine_name}")
        print(f"{'='*70}")
        
        if not unique_results:
            print("⚠️ No valid products found")
        else:
            print(f"✅ Found {len(unique_results)} product(s):\n")
            for i, r in enumerate(unique_results, 1):
                print(f"{i}. {r['name']}")
                mrp_str = f"₹{r['MRP']:.2f}" if r['MRP'] else "-"
                disc_str = f"{r['Discount']:.1f}%" if r['Discount'] else "-"
                price_str = f"₹{r['selling_price']:.2f}"
                print(f"   MRP: {mrp_str} | Discount: {disc_str} | Price: {price_str}")
                print()
        
        return unique_results
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []
    
    finally:
        driver.quit()


def extract_from_text(page_source, medicine_name):
    """Fallback method: Extract from raw text"""
    soup = BeautifulSoup(page_source, 'html.parser')
    text = soup.get_text(separator=' ')
    
    # Clean text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Find all price patterns
    price_pattern = r'(?:MRP|Price)?[:\s]*₹\s*([\d,]+(?:\.\d{2})?)'
    matches = list(re.finditer(price_pattern, text))
    
    if not matches:
        print("⚠️ No prices found in page")
        return []
    
    results = []
    for i, match in enumerate(matches[:10]):
        try:
            # Get context around price
            start = max(0, match.start() - 150)
            end = min(len(text), match.end() + 100)
            context = text[start:end]
            
            # Extract price
            price = float(match.group(1).replace(',', ''))
            
            # Try to find product name
            name_match = re.search(r'([A-Z][A-Za-z\s]{10,80})(?=\s*₹)', context)
            name = name_match.group(1).strip() if name_match else f"Product {i+1}"
            
            # Look for discount
            discount = None
            disc_match = re.search(r'(\d+)\s*%\s*(?:off|OFF)', context)
            if disc_match:
                discount = float(disc_match.group(1))
            
            results.append({
                "name": name,
                "MRP": None,
                "Discount": discount,
                "selling_price": price
            })
        except:
            continue
    
    # Remove duplicates
    unique = []
    seen_prices = set()
    for r in results:
        if r["selling_price"] not in seen_prices:
            seen_prices.add(r["selling_price"])
            unique.append(r)
    
    return sorted(unique, key=lambda x: x["selling_price"])[:5]


if __name__ == "__main__":
    medicine = input("Enter medicine name: ").strip()
    scrape_apollo(medicine)