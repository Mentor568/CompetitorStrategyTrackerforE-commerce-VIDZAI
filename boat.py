from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def get_product_price(driver, site, product):
    driver.get(site)
    
    try:
        # Close login popup if it appears
        time.sleep(3)
        try:
            close_button = driver.find_element(By.XPATH, "//button[contains(text(), '✕')]")
            close_button.click()
        except:
            pass  # Ignore if popup doesn't exist
        
        # Find the search bar and enter product name
        search_box = driver.find_element(By.XPATH, "//input[contains(@title, 'Search for products')]")
        search_box.send_keys(product)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for price to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._30jeq3"))
        )
        
        # Extract the price
        price_element = driver.find_element(By.CSS_SELECTOR, "div._30jeq3")
        price = price_element.text
        
    except Exception as e:
        price = "Not found"
        print(f"Error: {e}")
    
    return price

def main():
    product = input("Enter product name: ")
    sites = ["https://www.flipkart.com"]
    
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
