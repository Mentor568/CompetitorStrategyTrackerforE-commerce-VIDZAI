import streamlit as st
import pandas as pd
import numpy as np
import time

# Page Config
st.set_page_config(page_title="India Smartphone Sales", layout="wide")

# Title
st.title("📱 India Smartphone Sales Dashboard")
st.markdown("Track smartphone sales across different regions in India.")

# Sidebar Filters
st.sidebar.header("Filters")
region = st.sidebar.selectbox("Select Region", ["All", "North", "South", "East", "West", "Central"])
brand = st.sidebar.selectbox("Select Brand", ["All", "Samsung", "Apple", "Xiaomi", "OnePlus", "Realme", "Vivo"])

# Generate Sample Data
np.random.seed(42)
data = pd.DataFrame({
    'Region': np.random.choice(["North", "South", "East", "West", "Central"], 50),
    'Brand': np.random.choice(["Samsung", "Apple", "Xiaomi", "OnePlus", "Realme", "Vivo"], 50),
    'Sales': np.random.randint(10000, 500000, 50)
})

# Apply Filters
if region != "All":
    data = data[data["Region"] == region]
if brand != "All":
    data = data[data["Brand"] == brand]

# Display Data
st.subheader("📊 Sales Data")
st.write(data)

# Show Total Sales
st.subheader("💰 Total Sales")
st.metric(label="Total Sales", value=f"₹{data['Sales'].sum():,.2f}")

# Progress Bar Simulation
st.subheader("⏳ Loading Data...")
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)
st.success("Data Loaded!")

# Map Visualization (Random Points in India)
st.subheader("🗺️ Sales Distribution")
locations = pd.DataFrame({
    "latitude": np.random.uniform(8.0, 37.0, 10),
    "longitude": np.random.uniform(68.0, 97.0, 10)
})
st.map(locations)
