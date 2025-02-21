# selenium code to webscraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

def get_product_price(driver, site, product):
    driver.get(site)
    time.sleep(3)  # Allow page to load

    search_box = None  # Initialize to None in case no search box is found

    if site == "https://www.amazon.com":
        try:
            search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        except:
            print(f"Warning: Search box not found on {site} using ID 'twotabsearchtextbox', trying name='q'")
            try:
                search_box = driver.find_element(By.NAME, "q") # Fallback to name if ID fails
            except:
                print(f"Warning: Search box not found on {site} even with name='q'")

    elif site == "https://www.flipkart.com":
        try:
            search_box = driver.find_element(By.NAME, "q")
        except:
            print(f"Warning: Search box not found on {site} using name='q'")

    elif site == "https://www.apple.com/shop":
        try:
            # Click the search icon to open the search bar
            search_icon = driver.find_element(By.ID, "globalnav-menusearch-link")
            search_icon.click()
            time.sleep(1) # Wait for search bar to appear
            search_box = driver.find_element(By.ID, "globalnav-menusearch-searchfield")
        except:
            print(f"Warning: Search box not found on {site} (Apple Shop)")

    elif site == "https://www.bestbuy.com":
        try:
            search_box = driver.find_element(By.ID, "gh-search-input")
        except:
            print(f"Warning: Search box not found on {site} using ID 'gh-search-input'")

    elif site == "https://www.ebay.com":
        try:
            search_box = driver.find_element(By.ID, "gh-ac")
        except:
            print(f"Warning: Search box not found on {site} using ID 'gh-ac'")

    if search_box:  # Proceed only if a search box was found
        search_box.send_keys(product)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for results to load

        try:
            # Price selectors - you might need to adjust these based on the search results pages
            price_element = None
            if site == "https://www.amazon.com":
                price_element = driver.find_element(By.CSS_SELECTOR, ".a-price-whole") # Amazon specific price class on search results
            elif site == "https://www.flipkart.com":
                price_element = driver.find_element(By.CSS_SELECTOR, "._30jeq3") # Flipkart specific price class on search results
            elif site == "https://www.apple.com/shop":
                price_element = driver.find_element(By.CSS_SELECTOR, ".current_price") # Apple shop price class (may need refinement)
            elif site == "https://www.bestbuy.com":
                price_element = driver.find_element(By.CSS_SELECTOR, ".priceView-customer-price span") # BestBuy price class (may need refinement)
            elif site == "https://www.ebay.com":
                price_element = driver.find_element(By.CSS_SELECTOR, ".s-item__price") # eBay price class on search results

            if price_element:
                price = price_element.text
            else:
                price = "Price element not found"

        except Exception as e: # Catch any exception during price finding for robustness
            print(f"Warning: Price not found on {site} - Error: {e}")
            price = "Price not found"
        return price
    else:
        return "Search box not found" # Indicate if no search box at all could be located


def main():
    product = "realme 12 pro plus phones" # Set product directly
    sites = [
        "https://www.amazon.com",
        "https://www.flipkart.com",
        "https://www.apple.com/shop", # Apple Shop - may not be relevant for Realme phones, but included as per original list
        "https://www.bestbuy.com",
        "https://www.ebay.com"
    ]

    driver = webdriver.Chrome() # Or webdriver.Firefox(), etc.

    data = []
    for site in sites:
        price = get_product_price(driver, site, product)
        data.append([site, price])

    driver.quit()

    with open("product_prices.csv", "w", newline="", encoding="utf-8") as file: # Added encoding for broader character support
        writer = csv.writer(file)
        writer.writerow(["Website", "Price"])
        writer.writerows(data)

    print("CSV file created: product_prices.csv")

if __name__ == "__main__":
    main()