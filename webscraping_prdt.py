from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random

# Function to scrape product details from Amazon
def scrape_amazon(product_name):
    driver = webdriver.Chrome()  # Use the appropriate WebDriver
    driver.get(f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}")
    time.sleep(random.randint(2, 10))   # Wait for the page to load

    products = []
    try:
        items = driver.find_elements(By.CSS_SELECTOR, 'div.puisg.col.inner')
        count = 0
        for item in items:
            if count >= 3:  # Stop after 3 products
                break
            try:
                name = item.find_element(By.CSS_SELECTOR, 'h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal').text
                price = item.find_element(By.CSS_SELECTOR, '.a-price-whole').text
                products.append({'Site': 'Amazon', 'Product Name': name, 'Price': price})
                count += 1
            except:
                continue  # Skip if any element is not found
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
    finally:
        driver.quit()
    return products

# Function to scrape product details from Flipkart
def scrape_flipkart(product_name):
    driver = webdriver.Chrome()  # Use the appropriate WebDriver
    driver.get(f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}")
    time.sleep(random.randint(2, 10))   # Wait for the page to load

    products = []
    try:
        items = driver.find_elements(By.CSS_SELECTOR, 'div.tUxRFH')
        count = 0
        for item in items:
            if count >= 3:  # Stop after 3 products
                break
            try:
                name = item.find_element(By.CSS_SELECTOR, 'div.KzDlHZ').text
                price = item.find_element(By.CSS_SELECTOR, 'div.Nx9bqj._4b5DiR').text
                products.append({'Site': 'Flipkart', 'Product Name': name, 'Price': price})
                count += 1
            except:
                continue  # Skip if any element is not found
    except Exception as e:
        print(f"Error scraping Flipkart: {e}")
    finally:
        driver.quit()
    return products

# Function to scrape product details from Chroma
def scrape_chroma(product_name):
    driver = webdriver.Chrome()  # Use the appropriate WebDriver
    driver.get(f"https://www.chroma.com/search?q={product_name}")
    time.sleep(random.randint(2, 10))   # Wait for the page to load

    products = []
    try:
        items = driver.find_elements(By.CSS_SELECTOR, 'li.product-item')
        count = 0
        for item in items:
            if count >= 3:  # Stop after 3 products
                break
            try:
                name = item.find_element(By.CSS_SELECTOR, 'h3.product-title').text
                price = item.find_element(By.CSS_SELECTOR, 'span.amount.plp-srp-new-amount').text
                products.append({'Site': 'Chroma', 'Product Name': name, 'Price': price})
                count += 1
            except:
                continue  # Skip if any element is not found
    except Exception as e:
        print(f"Error scraping Chroma: {e}")
    finally:
        driver.quit()
    return products

# Main function to scrape and save data
def main():
    product_name = input("Enter the product name: ")
    
    # Scrape data from both sites
    amazon_products = scrape_amazon(product_name)
    flipkart_products = scrape_flipkart(product_name)
    chroma_products = scrape_chroma(product_name)
    
    # Combine the data
    all_products = amazon_products + flipkart_products + chroma_products
    
    # Save to CSV
    df = pd.DataFrame(all_products)
    df.to_csv(f'{product_name}_prices.csv', index=False)
    print(f"Data saved to {product_name}_products.csv")

if __name__ == "__main__":
    main()
