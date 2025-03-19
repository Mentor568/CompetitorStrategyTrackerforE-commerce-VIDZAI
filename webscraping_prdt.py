import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Initialize CSV file if it doesn't exist
if not os.path.exists("reviews.csv"):
    pd.DataFrame(columns=["product_name", "reviews", "source"]).to_csv("reviews.csv", index=False)

def scrape_reviews(reviews_link, product_name):
    # Configure Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-software-rasterizer")  # Suppress WebGL warning

    # Initialize WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.set_window_size(1920, 1080)
    driver.get(reviews_link)
    reviews_data = []
    wait = WebDriverWait(driver, 10)
    time.sleep(5)

    # Retry logic for page loading
    retry = 0
    while retry < 3:
        try:
            driver.save_screenshot("screenshot.png")
            wait.until(EC.presence_of_element_located((By.ID, "cm-cr-dp-review-list")))
            break
        except Exception as e:
            print(f"Retry {retry + 1}: {e}")
            retry += 1
            driver.get(reviews_link)
            time.sleep(5)

    # Extract reviews
    try:
        reviews = driver.find_element(By.ID, "cm-cr-dp-review-list")
        reviews = reviews.find_elements(By.TAG_NAME, "li")
        for item in reviews:
            review_text = item.get_attribute("innerText")
            reviews_data.append({"product_name": product_name, "reviews": review_text, "source": "Amazon"})
    except Exception as e:
        print(f"Error extracting reviews: {e}")

    driver.quit()
    return reviews_data

# List of review page links and corresponding product names
review_links = {
    "LG 108 cm (43 inches) 4K Ultra HD Smart LED TV": "https://www.amazon.in/Lenovo-IdeaPad-13420H-Backlit-82XD003NIN/dp/B0C9HTBMLW/ref=sr_1_3?crid=3I314GGGAMRAL&dib=eyJ2IjoiMSJ9.ZRrDvDIqrXzWnVOfzFzg7F8MBlYTCsL41UKf-ra1e3ldVJI0KpQNEB2YM3Af-SibI1fl5-m4PlYjOAnxWzyam9LbOJh9o6aY5pxft8jvkfzxeTOGwoAf_5sgw5Nj_XbmAJXtRItGuGeUPEOHtYG7TL5AD0FYIcvUjoZNEEHxKX7Ti4kwNgR4Xo2dEkYGulPAehlSJp0x5kL1cze0HU9RHnTe2oZzpdTqSxkr5HYsxx0.9Y_CgizCCY9CObSIsim0YSKg6usSLlYjdNvzl8MAaMI&dib_tag=se&keywords=lenovo%2Bideapad%2Bslim%2B5%2B13th%2Bgen%2Bintel%2Bcore%2Bi5%2B14%22(35.5cm)&nsdOptOutParam=true&qid=1742303424&sprefix=%2Caps%2C213&sr=8-3&th=1#customerReviews",
    "Samsung Galaxy S23 5G(Phantom Black, 128 GB)": "https://www.amazon.in/dp/B0BT9DVZLZ?ref=cm_sw_r_cp_ud_dp_J979JS5TZNNNNT5W0GH5&ref_=cm_sw_r_cp_ud_dp_J979JS5TZNNNNT5W0GH5&social_share=cm_sw_r_cp_ud_dp_J979JS5TZNNNNT5W0GH5&th=1#customerReviews",
    "Lenovo IdeaPad Slim 5 13th Gen Intel Core i5 14\"(35.5cm)": "https://www.amazon.in/dp/B0C9HTBMLW?ref=cm_sw_r_cp_ud_dp_AQ2GQVECESG99GWAZ59D&ref_=cm_sw_r_cp_ud_dp_AQ2GQVECESG99GWAZ59D&social_share=cm_sw_r_cp_ud_dp_AQ2GQVECESG99GWAZ59D&th=1#customerReviews",
    "JBL Tune 760NC Active  Noise Cancelling": "https://www.amazon.in/dp/B096FYLJ6M?ref=cm_sw_r_cp_ud_dp_WCG91B58JDYPCKG5TPXB&ref_=cm_sw_r_cp_ud_dp_WCG91B58JDYPCKG5TPXB&social_share=cm_sw_r_cp_ud_dp_WCG91B58JDYPCKG5TPXB&th=1#customerReviews",
    "LG 322 L 3 Star Frost-Free Smart Inverter Double Door Refrigerator": "https://www.amazon.in/LG-Frost-Free-Refrigerator-GL-S342SDSX-Convertible/dp/B0C8NTDY55/ref=sr_1_3?crid=60KI0WLRMZRD&dib=eyJ2IjoiMSJ9.knGwNgOdGUWLTblYSbhy4Pe8kmojxOLODG9j8ZQ-hpFF5lvJB_STTW1qCepZJXYh0gXLneIuJVNIBGJqcP3o7bcQqVh0W0-5JQgR5WWiWEz0i9tPRnd8TkELEMTJ7vdNsZfBFxBqojfwaWKIHCJGGdSvmBD64mLkabhbqa_8EQdLIFCLND4UWE5BNSEieOrF55L8KHjArooLk21xK_MxiEn1baMd-Lgq0DFiPbUUFwI.B7sZEaI0LNALVkesefb0xbdclqdRUWd_eKlZESbe49M&dib_tag=se&keywords=lg%2B322%2Bl%2B3%2Bstar%2Bfrost-free%2Bsmart%2Binverter%2Bdouble%2Bdoor%2Brefrigerator&nsdOptOutParam=true&qid=1742308307&sprefix=%2Caps%2C188&sr=8-3&th=1#customerReviews",
    "USHA Maxx Air Ultra 400MM Table Fan (Light Blue)": "https://www.amazon.in/dp/B0C2V2JVPV?ref=cm_sw_r_cp_ud_dp_XQ6RQN767HFW9SZRAK8Z&ref_=cm_sw_r_cp_ud_dp_XQ6RQN767HFW9SZRAK8Z&social_share=cm_sw_r_cp_ud_dp_XQ6RQN767HFW9SZRAK8Z&th=1#customerReviews"
}

# Main loop to scrape reviews for each product
all_reviews = []
for product_name, reviews_link in review_links.items():
    print(f"Scraping reviews for: {product_name}")
    reviews_data = scrape_reviews(reviews_link, product_name)
    all_reviews.extend(reviews_data)

# Save all reviews to CSV
pd.DataFrame(all_reviews).to_csv("reviews.csv", index=False)

print("All reviews extraction completed and data saved to 'reviews.csv'.")