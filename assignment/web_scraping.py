from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
import pandas as pd
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.common.exceptions import NoSuchElementException, TimeoutException # type: ignore
import time
import sys
from tqdm import tqdm  # type: ignore # For progress bar

# Chrome options for headless mode and mimicking a real browser
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Initialize WebDriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# List of URLs to scrape (5 products per company)
urls = {
    'Amazon': [
        'https://www.amazon.in/Sony-Bluetooth-Headphones-Multipoint-Connectivity/dp/B0BS1PRC4L',
        'https://www.amazon.in/Samsung-Galaxy-Ultra-Green-Storage/dp/B0BT9CXXXX',
        'https://www.amazon.in/Samsung-Galaxy-F55-Raisin-Black/dp/B0D5VMSM5D',
        'https://www.amazon.in/OnePlus-Nord-Gray-128GB-Storage/dp/B09WQYFLRX',
        'https://www.amazon.in/Canon-EOS-1500D-Digital-Camera/dp/B07BS4TJ43'
    ],
    
    'Myntra': [
        'https://www.myntra.com/tshirts/adidas+originals/adidas-originals-melange-effect-3-stripes-slim-raglan-tee/30381310/buy',
        'https://www.myntra.com/sunglasses/ray-ban/ray-ban-men-uv-protected-green-lens-pilot-sunglasses---0rb3432i00159/256699/buy',
        'https://www.myntra.com/casual-shoes/puma/puma-smashic-brand-logo-printed-casual-sneakers-shoes/21767244/buy',
        'https://www.myntra.com/watches/fossil/fossil-women-rose-gold-toned-ryeanalogue-watch-bq3691/14872768/buy',
        'https://www.myntra.com/backpacks/skybags/skybags-unisex-kids-blue--green-brand-logo-print-backpack/14303964/buy'
    ]
}

# Data storage
data = []

# Function to clean text (remove extra spaces and newlines)
def clean_text(text):
    return ' '.join(text.split()).strip()

# Function to display a spinner animation
def spinner_animation(message):
    spinner = ['-', '\\', '|', '/']
    for _ in range(10):  # Run for 10 iterations
        for char in spinner:
            sys.stdout.write(f"\r{message} {char}")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")  # Clear the spinner line

# Function to display a checkmark animation
def checkmark_animation(message):
    for _ in range(3):  # Blink the checkmark 3 times
        sys.stdout.write(f"\r{message} ✓")
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write(f"\r{message}  ")
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write(f"\r{message} ✓\n")

# Function to extract product details
def extract_details(site_name, url):
    print(f"\nScraping data from {site_name}...")
    spinner_animation("Loading page")  # Spinner animation while loading the page

    driver.get(url)
    time.sleep(5)  # Wait for the page to load completely

    try:
        if site_name == 'Amazon':
            product_name = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'productTitle'))
            ).text.strip()
            product_price = driver.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text.strip()

        elif site_name == 'Myntra':
            product_name = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.pdp-title'))
            ).text.strip()
            product_price = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.pdp-price'))
            ).text.strip()

        elif site_name == 'Nykaa':
            product_name = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-at="product-name"].css-175ipe2'))
            ).text.strip()
            product_price = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-at="sp-pdp"]'))
            ).text.strip()

        elif site_name == 'AJIO':
            product_name = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'prod-name'))
            ).text.strip()
            product_price = driver.find_element(By.CLASS_NAME, 'prod-sp').text.strip()

        else:
            product_name = 'N/A'
            product_price = 'N/A'

        # Clean the extracted text to remove extra spaces and newlines
        product_name = clean_text(product_name)
        product_price = clean_text(product_price)

        # Print the extracted data
        print(f"Extracted from {site_name}:")
        print(f"Product Name: {product_name}")
        print(f"Price: {product_price}")
        print("-" * 40)

        # Append data to the list
        data.append({
            'Site': site_name,
            'Product Name': product_name,
            'Price': product_price
        })

        # Display checkmark animation for successful extraction
        checkmark_animation(f"Data extracted from {site_name}")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error extracting data from {site_name}: {e}")
        driver.save_screenshot(f'{site_name}_error.png')
        print("Saving page source for debugging...")
        with open(f'{site_name}_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

# Iterate over URLs and extract data for each product
print("Starting data extraction...")
for site, links in tqdm(urls.items(), desc="Overall Progress", unit="site"):
    for link in links:
        extract_details(site, link)
        time.sleep(5)  # Add a delay between requests to avoid being blocked

# Close the WebDriver
driver.quit()

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('prices5.csv', index=False)

print("\nData extraction complete. Saved to 'prices5.csv'.")