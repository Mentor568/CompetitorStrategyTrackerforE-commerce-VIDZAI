from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


urls = {
    'Amazon': [
        'https://www.amazon.in/Apple-EarPods-with-Lightning-Connector/dp/B0D7MNX9Y5',  
        'https://www.amazon.in/Samsung-Galaxy-Graphite-128GB-Storage/dp/B09P7G7Y95', 
        'https://www.amazon.in/boAt-Airdopes-121-Pro-Plus/dp/B0D49XY9Y8',
        'https://www.amazon.in/All-New-release-smart-speaker-Black/dp/B09B917Z8D',
        'https://www.amazon.in/Sony-WH-1000XM5-Wireless-Cancelling-Headphones/dp/B09XS7JWHH'   
    ],
    'Flipkart': [
        'https://www.flipkart.com/apple-iphone-13/p/itm6e30aafca13d0',
        'https://www.flipkart.com/boat-rockerz-450-bluetooth-headset/p/itm7c1ed9f9c4128',
        'https://www.flipkart.com/adidas-men-black-running-shoes/p/itmf3xzfwjywgcbf',
        'https://www.flipkart.com/timex-analog-watch-men/p/itmfg56s4fgyr9dh',
        'https://www.flipkart.com/wildcraft-rucksack/p/itmf3vfypp2haj8h'
    'Myntra': [
        'https://www.myntra.com/jackets/puma/puma-men-black-solid-sporty-jacket/13251576/buy',
        'https://www.myntra.com/shoes/nike/nike-men-grey-running-shoes/13279856/buy',
        'https://www.myntra.com/jeans/levis/levis-men-blue-slim-fit-jeans/14884676/buy',
        'https://www.myntra.com/watches/fossil/fossil-men-brown-leather-watch/13648234/buy',
        'https://www.myntra.com/bags/skybag/skybag-unisex-backpack/12549378/buy'
    ],
    'eBay': [
        'https://www.ebay.com/iPhone 13 Pro/125495189459', 
        'https://www.ebay.com/Bose QuietComfort Earbuds/115489650469',  
        'https://www.ebay.com/Nike Air Max Shoes/394117063480',  
        'https://www.ebay.com/Casio G-Shock Watch/203987461893',    
    ]
}


# Data storage
data = []

# Extract product details
def extract_product_data(site, url):
    try:
        driver.get(url)
        time.sleep(3)

        if site == 'Amazon':
            product_name = driver.find_element(By.ID, 'productTitle').text.strip()
            price = driver.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text.strip()

        elif site == 'Flipkart':
            product_name = driver.find_element(By.CLASS_NAME, 'B_NuCI').text.strip()
            price = driver.find_element(By.CLASS_NAME, '_30jeq3').text.strip()

        elif site == 'eBay':
            product_name = driver.find_element(By.CSS_SELECTOR, 'h1.x-item-title__mainTitle').text.strip()
            price = driver.find_element(By.CSS_SELECTOR, 'span.x-price-primary').text.strip()

        elif site == 'Myntra':
            product_name = driver.find_element(By.CLASS_NAME, 'pdp-title').text.strip()
            price = driver.find_element(By.CLASS_NAME, 'pdp-price').text.strip()

        elif site == 'AJIO':
            product_name = driver.find_element(By.CLASS_NAME, 'prod-name').text.strip()
            price = driver.find_element(By.CLASS_NAME, 'prod-sp').text.strip()

        else:
            product_name, price = 'N/A', 'N/A'

        data.append({'Site': site, 'Product Name': product_name, 'Price': price, 'URL': url})
        print(f"Scraped from {site}: {product_name} - {price}")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Failed to extract data from {site}: {e}")

# Loop through sites and products
for site, links in urls.items():
    for link in links:
        extract_product_data(site, link)
        time.sleep(2)

# Save to CSV
driver.quit()
df = pd.DataFrame(data)
df.to_csv('products_scraped.csv', index=False)

print("Scraping completed! Data saved to 'products_scraped.csv'")
