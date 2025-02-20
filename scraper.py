from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
# Unified function to scrape product details from multiple sites
def scrape_products(product_name, site):
    driver = webdriver.Chrome()  # Use the appropriate WebDriver
    # Define URLs and CSS selectors for each site
    sites = {
        'Amazon': {
            'url': f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}",
            'item_selector': 'div.puisg.col.inner',
            'name_selector': 'h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal',
            'price_selector': '.a-price-whole'
        },
        'Flipkart': {
            'url': f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}",
            'item_selector': 'div.slAVV4',
            'name_selector': 'a.wjcEIp',
            'price_selector': 'div.Nx9bqj'
        },
        'Chroma': {
            'url': f"https://www.chroma.com/search?q={product_name}",
            'item_selector': 'li.product-item',
            'name_selector': 'h3.product-title',
            'price_selector': 'span.amount.plp-srp-new-amount'
        }
    }
    # Navigate to the site
    driver.get(sites[site]['url'])
    time.sleep(random.randint(2, 10))   # Wait for the page to load
    products = []
    try:
        items = driver.find_elements(By.CSS_SELECTOR, sites[site]['item_selector'])
        count = 0
        for item in items:
            if count >= 5:  # Stop after 5 products
                break
            try:
                name = item.find_element(By.CSS_SELECTOR, sites[site]['name_selector']).text
                price = item.find_element(By.CSS_SELECTOR, sites[site]['price_selector']).text
                products.append({'Site': site, 'Product Name': name, 'Price': price})
                count += 1
            except:
                continue  # Skip if any element is not found
    except Exception as e:
        print(f"Error scraping {site}: {e}")
    finally:
        driver.quit()
    return products
# Main function to scrape and save data
def main():
    product_name = input("Enter the product name: ")
    # Scrape data from all sites
    all_products = []
    for site in ['Amazon', 'Flipkart', 'Chroma']:
        products = scrape_products(product_name, site)
        all_products.extend(products)
    # Save to CSV
    df = pd.DataFrame(all_products)
    df.to_csv(f'{product_name}_prices.csv', index=False)
    print(f"Data saved to {product_name}_prices.csv")
if __name__ == "__main__":
    main()