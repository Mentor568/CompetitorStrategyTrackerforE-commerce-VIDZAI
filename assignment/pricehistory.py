import pandas as pd
from datetime import datetime

# Sample Data
d = {
    "pid": "DLLH6GPQQTCPQJ4Q",
    "product_name": "Nikon Z50 II Mirrorless Camera with 16-50mm Lens",
    "history": {
        "1741507698": 83999.0,
        "1741575653": 83999.0,
        "1741679743": 83999.0,
        "1741757766": 83999.0,
        "1741891600": 91645.0,
        "1741935086": 91645.0,
        "1742023325": 91645.0,
        "1742102800": 91645.0,
        "1742202360": 91645.0,
        "1742270755": 91645.0
    },
    "highest_price": 91645.0,  # Needed for discount calculation
    "source": "Flipkart",
    "url": "https://www.flipkart.com/nikon-z50-ii-mirrorless-camera-body-16-50-lens/p/itmdc64017735260?pid=DLLH6GPQQTCPQJ4Q"
}

# Convert history to DataFrame
price_history = d["history"]
df = pd.DataFrame(list(price_history.items()), columns=["timestamp", "price"])

# Convert timestamp to readable date format
df["date"] = df["timestamp"].astype(float).apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d'))

# Calculate discount percentage
df["discount"] = ((d["highest_price"] - df["price"]) / d["highest_price"]) * 100

# Add additional columns
df["product_name"] = d["product_name"]
df["source"] = d["source"]

# Reorder columns
df = df[["product_name", "price", "discount", "date", "source"]]

# Save to CSV
csv_filename = "price_history.csv"
df.to_csv(csv_filename, index=False)

print(f"Price history saved to {csv_filename}")

# To load the dataset later:
# df = pd.read_csv("price_history.csv")
