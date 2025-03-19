import json
from datetime import datetime
import pandas as pd

# Mock JSON responses for 5 products from different websites
json_responses = [
    # Product 1: Flipkart
    '''
    {
        "pid": "MOBH4DQFG8NKFRDY",
        "history": {
            "1725974203": 79900.0,
            "1726022470": 79900.0,
            "1726104992": 79900.0
        },
        "price_fetched_at": "2025-03-14T14:30:50.119253Z",
        "lowest_price": 69499.0,
        "highest_price": 79900.0,
        "average_price": 74789.0,
        "drop_chances": 37.0,
        "rating": 4.5,
        "rating_count": 32958,
        "stock": true,
        "price": 74900.0,
        "url": "https://www.flipkart.com/apple-iphone-16-black-128-gb/p/itmb07d67f995271?pid=MOBH4DQFG8NKFRDY",
        "name": "Apple iPhone 16 (Black, 128 GB)",
        "reviews": [
            {"text": "Great phone, excellent camera!", "rating": 5},
            {"text": "Battery life could be better.", "rating": 4}
        ]
    }
    ''',
    # Product 2: Amazon
    '''
    {
        "pid": "B09G9D8KRQ",
        "history": {
            "1672531200": 39999.0,
            "1672617600": 40999.0,
            "1672704000": 41999.0
        },
        "price_fetched_at": "2025-03-13T14:32:30.846653Z",
        "lowest_price": 39999.0,
        "highest_price": 94900.0,
        "average_price": 63930.0,
        "drop_chances": 2.0,
        "rating": 4.5,
        "rating_count": 32958,
        "stock": true,
        "price": 44999.0,
        "url": "https://www.amazon.in/gp/product/B09G9D8KRQ/",
        "name": "Samsung Galaxy S22 (Black, 128 GB)",
        "reviews": [
            {"text": "Amazing display and performance.", "rating": 5},
            {"text": "Heats up during gaming.", "rating": 3}
        ]
    }
    ''',
    # Product 3: Myntra
    '''
    {
        "pid": "MYN123456789",
        "history": {
            "1725974203": 1999.0,
            "1726022470": 1899.0,
            "1726104992": 1799.0
        },
        "price_fetched_at": "2025-03-14T14:30:50.119253Z",
        "lowest_price": 1799.0,
        "highest_price": 1999.0,
        "average_price": 1899.0,
        "drop_chances": 10.0,
        "rating": 4.2,
        "rating_count": 1200,
        "stock": true,
        "price": 1899.0,
        "url": "https://www.myntra.com/shoes/nike-air-max",
        "name": "Nike Air Max Shoes",
        "reviews": [
            {"text": "Very comfortable and stylish.", "rating": 5},
            {"text": "Sole started peeling after a month.", "rating": 2}
        ]
    }
    ''',
    # Product 4: Nykaa
    '''
    {
        "pid": "NYK987654321",
        "history": {
            "1725974203": 1499.0,
            "1726022470": 1399.0,
            "1726104992": 1299.0
        },
        "price_fetched_at": "2025-03-14T14:30:50.119253Z",
        "lowest_price": 1299.0,
        "highest_price": 1499.0,
        "average_price": 1399.0,
        "drop_chances": 13.33,
        "rating": 4.5,
        "rating_count": 2500,
        "stock": true,
        "price": 1399.0,
        "url": "https://www.nykaa.com/lakme-foundation",
        "name": "Lakme Foundation",
        "reviews": [
            {"text": "Great coverage and long-lasting.", "rating": 5},
            {"text": "Shade was a bit off.", "rating": 3}
        ]
    }
    ''',
    # Product 5: Croma
    '''
    {
        "pid": "CRO123456789",
        "history": {
            "1725974203": 49999.0,
            "1726022470": 48999.0,
            "1726104992": 47999.0
        },
        "price_fetched_at": "2025-03-14T14:30:50.119253Z",
        "lowest_price": 47999.0,
        "highest_price": 49999.0,
        "average_price": 48999.0,
        "drop_chances": 4.0,
        "rating": 4.0,
        "rating_count": 500,
        "stock": true,
        "price": 48999.0,
        "url": "https://www.croma.com/sony-bravia-tv",
        "name": "Sony Bravia TV",
        "reviews": [
            {"text": "Excellent picture quality.", "rating": 5},
            {"text": "Sound quality is average.", "rating": 3}
        ]
    }
    '''
]

# Function to process a single product's JSON data
def process_product(json_response):
    data = json.loads(json_response)
    
    # Extract relevant data
    product_name = data.get("name", "Unknown Product")
    source = data.get("url", "Unknown Source")
    price_history = data["history"]
    current_price = data.get("price", 0)
    highest_price = data.get("highest_price", 0)
    reviews = data.get("reviews", [])
    
    # Calculate discount percentage
    discount = 0
    if highest_price > 0:
        discount = round(((highest_price - current_price) / highest_price) * 100, 2)
    
    # Process price history
    history_data = []
    for timestamp, price in price_history.items():
        date = datetime.fromtimestamp(int(timestamp))  # Convert Unix timestamp to date
        formatted_date = date.strftime("%Y-%m-%d")     # Format date as YYYY-MM-DD
        history_data.append({
            "Date": formatted_date,
            "Price": price,
            "Product Name": product_name,
            "Discount (%)": discount,
            "Source": source
        })
    
    # Process reviews
    review_data = []
    for review in reviews:
        review_data.append({
            "Product Name": product_name,
            "Review Text": review.get("text", "No review text"),
            "Rating": review.get("rating", 0),
            "Source": source
        })
    
    return history_data, review_data

# Process all products
all_price_data = []
all_review_data = []
for json_response in json_responses:
    price_data, review_data = process_product(json_response)
    all_price_data.extend(price_data)
    all_review_data.extend(review_data)

# Convert to DataFrames
price_df = pd.DataFrame(all_price_data)
review_df = pd.DataFrame(all_review_data)

# Save to CSV files
price_df.to_csv("price_history.csv", index=False)
review_df.to_csv("reviews.csv", index=False)
print("prices.csv")
print("reviews.csv")

# Combine the two CSV files into one
combined_df = pd.merge(price_df, review_df, on="Product Name", how="outer")

# Rename columns for clarity
combined_df = combined_df.rename(columns={
    "Source_x": "Price Source",
    "Source_y": "Review Source"
})

# Save the combined data to a new CSV file
combined_df.to_csv("Scrapping_data.csv", index=False)
print("Scrapping_data.csv")