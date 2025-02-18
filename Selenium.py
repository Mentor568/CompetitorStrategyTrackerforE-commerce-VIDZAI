from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())

# List of URLs to scrape
urls = {
    'Amazon': 'https://www.amazon.in/s?k=iphone+16pro+max&crid=3UBXC9NNTCFN7&sprefix=iphon%2Caps%2C419&ref=nb_sb_ss_ts-doa-p_1_5',
    'Flipkart': 'https://www.flipkart.com/search?q=iphone%2016%20pro%20max&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
}

# Data storage
data = []

# Function to extract product details
def extract_details(site_name, url):
    driver.get(url)
    try:
        # Handle Flipkart pop-up
        if site_name == 'Flipkart':
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, 'button._2KpZ6l._2doB4z')
                close_button.click()
            except:
                pass  # Pop-up not found

        if site_name == 'Amazon':
            product_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.a-size-medium'))
            ).text.strip()
            product_price = driver.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text.strip()

        elif site_name == 'Flipkart':
            product_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div._4rR01T'))
            ).text.strip()
            product_price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div._30jeq3'))
            ).text.strip()

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
df.to_csv('iphone_16_pro_max_prices.csv', index=False)

print("Data extraction complete. Saved to 'iphone_16_pro_max_prices.csv'.")