from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# List of URLs to scrape
urls = {
    'Amazon': 'https://www.amazon.in/dp/B0CWRW2BMV',
    'Myntra': 'https://www.myntra.com/casual-shoes/puma/puma-men-court-shatter-low-sneakers/27953916/buy',
    'AJIO': 'https://www.ajio.com/puma-court-shatter-low-sneakers/p/469515577_white'
}

# Data storage
data = []

# Function to extract product details
def extract_details(site_name, url):
    driver.get(url)
    try:
        if site_name == 'Amazon':
            product_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'productTitle'))
            ).text.strip()
            product_price = driver.find_element(By.CLASS_NAME, 'a-price-whole').text.strip()

        elif site_name == 'Myntra':
            product_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pdp-title'))
            ).text.strip()
            product_price = driver.find_element(By.CLASS_NAME, 'pdp-price').text.strip()

        elif site_name == 'AJIO':
            product_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'prod-name'))
            ).text.strip()
            product_price = driver.find_element(By.CLASS_NAME, 'prod-sp').text.strip()

        else:
            product_name = 'N/A'
            product_price = 'N/A'

        data.append({
            'Site': site_name,
            'Product Name': product_name,
            'Price': product_price
        })

    except Exception as e:
        print(f"Error extracting data from {site_name}: {e}")

# Iterate over URLs and extract data
for site, link in urls.items():
    extract_details(site, link)

# Close the WebDriver
driver.quit()

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('puma_sneakers_prices.csv', index=False)

print("Data extraction complete. Saved to 'puma_sneakers_prices.csv'.")
