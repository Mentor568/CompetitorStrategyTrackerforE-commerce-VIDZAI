import json
import time
import os
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Define product links
links = {
    "Samsung 80 cm (32 inches) HD Ready Smart LED TV UA32T4380AKXXL (Glossy Black)" : "https://amzn.in/d/5Z9eft3",
    "Apple iPhone 16 (Black, 128 GB)": "https://amzn.in/d/7ibZClF",
    "Noise Pro 6 Max Smart Watch": "https://amzn.in/d/93MA7yU",
    "Crompton Optimus 100 Litres Desert Air Cooler for home": "https://amzn.in/d/8T6mZIS",
    "LG 322 L 3 Star Frost-Free Smart Inverter Double Door Refrigerator": "https://amzn.in/d/01AEIEL"
}

# Initialize CSV file if it doesn't exist
if not os.path.exists("competitor_data.csv"):
    pd.DataFrame(columns=["product_name", "Price", "Discount", "Date", "source"]).to_csv("competitor_data.csv", index=False)

def scrape_product_data(link):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(link)
    product_data = {}
    time.sleep(5)

    # Extract product price
    try:
        price_elem = driver.find_element(
            By.XPATH,
            '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]',
        )
        product_data["selling price"] = int("".join(price_elem.text.strip().split(",")))
    except:
        try:
            price_elem = driver.find_element(By.CSS_SELECTOR, ".a-price-whole")
            product_data["selling price"] = int("".join(price_elem.text.strip().split(",")))
        except:
            product_data["selling price"] = 0

    # Extract original price
    try:
        original_price = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span[2]/span/span[2]').text
        product_data["original price"] = int("".join(original_price.strip().split(",")))
    except:
        product_data["original price"] = 0

    # Extract discount
    try:
        discount = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]')
        product_data["discount"] = discount.text.strip()
    except:
        product_data["discount"] = "0%"

    # Add date
    product_data["date"] = time.strftime("%Y-%m-%d")
    driver.quit()
    return product_data

# Main loop to scrape data for each product
for product_name, link in links.items():
    product_data = scrape_product_data(link)

    # Load existing data from CSV file
    price = json.loads(pd.read_csv("competitor_data.csv").to_json(orient="records"))

    # Append new data
    price.append(
        {
            "product_name": product_name,
            "Price": product_data["selling price"],
            "Discount": product_data["discount"],
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Amazon",
        }
    )

    # Save updated data to CSV file
    pd.DataFrame(price).to_csv("competitor_data.csv", mode="w", header=True, index=False)

print("Scraping completed and data saved to CSV file.")