import json
from datetime import datetime, timedelta
import pandas as pd
import random

# Mock JSON responses for 5 products from different websites
json_responses = [
    # Product 1: Amazon
    '''
    {
        "pid": "B07VDL5R4N",
        "history": {
            "1725974203": 1299.0,
            "1726022470": 1199.0,
            "1726104992": 1099.0
        },
        "price_fetched_at": "2025-03-14T14:30:50.119253Z",
        "lowest_price": 1099.0,
        "highest_price": 1299.0,
        "average_price": 1199.0,
        "drop_chances": 20.0,
        "rating": 4.5,
        "rating_count": 2000,
        "stock": true,
        "price": 1199.0,
        "url": "https://www.amazon.in/Adidas-Striped-Regular-T-Shirt-FJ9216_White_L/dp/B07VDL5R4N/",
        "name": "Adidas Striped T-Shirt",
        "reviews": [
            {"text": "Comfortable and fits well.", "rating": 5},
            {"text": "Good quality fabric.", "rating": 4}
        ]
    }
    ''',
    # Product 2: Ajio
    '''
    {
        "pid": "469228483_darkgrey",
        "price": 4999.0,
        "name": "Ray-Ban UV-Protected Aviators",
        "url": "https://www.ajio.com/ray-ban-full-rim-uv-protected-aviators/p/469228483_darkgrey",
        "reviews": [
            {"text": "Stylish and lightweight.", "rating": 5},
            {"text": "Lens quality is great.", "rating": 4}
        ]
    }
    ''',
    # Product 3: Myntra
    '''
    {
        "pid": "21767244",
        "price": 3299.0,
        "name": "Puma Smashic Casual Sneakers",
        "url": "https://www.myntra.com/casual-shoes/puma/puma-smashic-brand-logo-printed-casual-sneakers-shoes/21767244/buy",
        "reviews": [
            {"text": "Trendy and durable.", "rating": 5},
            {"text": "Comfortable but narrow fit.", "rating": 3}
        ]
    }
    ''',
    # Product 4: Flipkart
    '''
    {
        "pid": "WATGDCFHRDP2TKPX",
        "price": 10999.0,
        "name": "Fossil Rose Gold Watch",
        "url": "https://www.flipkart.com/fossil-eevie-analog-watch-women/p/itmfd080732390cb?pid=WATGDCFHRDP2TKPX",
        "price_fetched_at": "2025-03-14T14:30:50.119253Z",
        "reviews": [
            {"text": "Elegant design.", "rating": 5},
            {"text": "Strap quality could be better.", "rating": 4}
        ]
    }
    ''',
    # Product 5: Nykaa
    '''
    {
        "pid": "8496130",
        "price": 2299.0,
        "name": "Skybags Flex Backpack",
        "url": "https://www.nykaa.com/skybags-polyester-22l-flex-22l-backpack-cabret/p/8496130",
        "price_fetched_at": "2025-03-14T14:30:50.119253Z",
        "reviews": [
            {"text": "Spacious and stylish.", "rating": 5},
            {"text": "Good for daily use.", "rating": 4}
        ]
    }
    '''
]

# Process each product
price_data = []
review_data = []

for json_response in json_responses:
    data = json.loads(json_response)

    # Generate a random date within the past 30 days
    random_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%d-%m-%Y")

    # Calculate discount percentage
    discount = round(((data.get("highest_price", data["price"]) - data["price"]) / data.get("highest_price", data["price"])) * 100, 2)

    price_data.append({
        "Product Name": data["name"],
        "Price": data["price"],
        "Discount (%)": discount,
        "Date Fetched": random_date,
        "Source": data["url"]
    })

    for review in data.get("reviews", []):
        review_data.append({
            "Product Name": data["name"],
            "Reviews": review["text"],
            "Source": data["url"]
        })

# Convert to DataFrame and Save to CSV
df_prices = pd.DataFrame(price_data)
df_reviews = pd.DataFrame(review_data)

df_prices.to_csv("prices.csv", index=False)
df_reviews.to_csv("reviews.csv", index=False)

print("Data scraping complete. Files saved as 'prices.csv' and 'reviews.csv'")
