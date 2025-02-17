from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

def get_product_price(driver, site, product):
    driver.get(site)
    time.sleep(3)  # Allow page to load
    
    search_box = driver.find_element(By.NAME, "q")  # Adjust according to site's search box element
    search_box.send_keys(product)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Wait for results to load
    
    try:
        price_element = driver.find_element(By.CSS_SELECTOR, ".a-price-whole, ._30jeq3, .price, .product-price")  # Adjust selectors
        price = price_element.text
    except:
        price = "Not found"
    
    return price

def main():
    product = input("Enter product name: ")
    sites = [
        "https://www.amazon.com", 
        "https://www.flipkart.com", 
        "https://www.apple.com/shop", 
        "https://www.bestbuy.com", 
        "https://www.ebay.com"
    ]
    
    driver = webdriver.Chrome()
    
    data = []
    for site in sites:
        price = get_product_price(driver, site, product)
        data.append([site, price])
    
    driver.quit()
    
    with open("product_prices.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Website", "Price"])
        writer.writerows(data)
    
    print("CSV file created: product_prices.csv")

if __name__ == "__main__":
    main()
