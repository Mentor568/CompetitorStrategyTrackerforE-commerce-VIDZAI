import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Function to get price safely
def get_price(driver):
    try:
        price_element = driver.find_element(By.CSS_SELECTOR, ".a-price-whole, .s-item__price")  # Adjust selectors
        price = price_element.text
    except NoSuchElementException:
        price = "Price not found"
    return price

# Function to scrape product data from Amazon
def scrape_amazon():
    url = "https://www.amazon.com/s?k=Dyson+Airwrap"
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    products = []
    product_elements = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")

    for product in product_elements:
        try:
            title = product.find_element(By.CSS_SELECTOR, "h2 .a-link-normal").text
            price = get_price(product)
            products.append({'Title': title, 'Price': price})
        except NoSuchElementException:
            continue

    return products

# Function to scrape product data from eBay
def scrape_ebay():
    url = "https://www.ebay.com/sch/i.html?_nkw=Dyson+Airwrap"
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    products = []
    product_elements = driver.find_elements(By.CSS_SELECTOR, ".s-item")

    for product in product_elements:
        try:
            title = product.find_element(By.CSS_SELECTOR, ".s-item__title").text
            price = get_price(product)
            products.append({'Title': title, 'Price': price})
        except NoSuchElementException:
            continue

    return products

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Scrape data from both Amazon and eBay
amazon_products = scrape_amazon()
ebay_products = scrape_ebay()

# Combine the results
all_products = amazon_products + ebay_products

# Convert to DataFrame and save to CSV
df = pd.DataFrame(all_products)
df.to_csv('dyson_airwrap_products.csv', index=False)

# Clean up
driver.quit()
print("Data scraped and saved to dyson_airwrap_products.csv")