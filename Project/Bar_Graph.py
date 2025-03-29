import json
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from transformers import pipeline

API_KEY = "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"  # Groq API Key

def truncate_text(text, max_length=512):
    return text[:max_length]

def load_competitor_data():
    """Load competitor data from a CSV file."""
    data = pd.read_csv("competitor.csv")
    print(data.head())
    return data

def load_reviews_data():
    """Load reviews data from a CSV file."""
    reviews = pd.read_csv("competitor_reviews.csv")
    return reviews

def analyze_sentiment(reviews):
    """Analyze customer sentiment for reviews."""
    sentiment_pipeline = pipeline("sentiment-analysis")
    return sentiment_pipeline(reviews)

def train_predictive_model(data):
    """Train a predictive model for competitor pricing strategy."""
    data["Discount"] = data["Discount"].str.replace("%", "").astype(float)
    data["Price"] = data["Price"].astype(int)
    data["Predicted_Discount"] = data["Discount"] + (data["Price"] * 0.05).round(2)

    X = data[["Price", "Discount"]]
    y = data["Predicted_Discount"]
    print(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, train_size=0.8
    )

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model

import numpy as np
import pandas as pd

def forecast_discounts_arima(data, future_days=5):
    """
    Forecast future discounts using ARIMA.
    :param data: DataFrame containing historical discount data with a 'Date' column.
    :param future_days: Number of days to forecast.
    :return: DataFrame with historical and forecasted discounts.
    """

    # Ensure 'Date' is a datetime index
    data["Date"] = pd.to_datetime(data["Date"], format="%d-%m-%Y", errors="coerce")
    data = data.set_index("Date").sort_index()

    # Ensure 'Discount' is numeric
    data["Discount"] = pd.to_numeric(data["Discount"], errors="coerce")
    data = data.dropna(subset=["Discount"])

    if data.empty:
        raise ValueError("No valid discount data available for forecasting.")

    discount_series = data["Discount"]

    # Train ARIMA model
    model = ARIMA(discount_series, order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast future discounts
    forecast = model_fit.forecast(steps=future_days)

    # Generate future dates starting from the latest date in the dataset
    last_date = discount_series.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=future_days)

    # Create DataFrame for predictions
    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Discount": forecast})
    forecast_df.set_index("Date", inplace=True)

    return forecast_df


def generate_strategy_recommendation(product_name, competitor_data, sentiment):
    """Generate strategic recommendations using an LLM."""
    date = datetime.now()
    prompt = f"""
    You are a highly skilled business strategist specializing in e-commerce. Based on the following details, suggest actionable strategies to optimize pricing, promotions, and customer satisfaction for the selected product:

    1. **Product Name**: {product_name}
    2. **Competitor Data**:
    {competitor_data}
    3. **Sentiment Analysis**:
    {sentiment}
    4. **Today's Date**: {str(date)}

    Provide structured recommendations under these categories:
    1. **Pricing Strategy**
    2. **Promotional Campaign Ideas**
    3. **Customer Satisfaction Recommendations**
    """
    
    data = {"messages": [{"role": "user", "content": prompt}], "model": "llama3-8b-8192", "temperature": 0}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", data=json.dumps(data), headers=headers, timeout=10)
    print(res.content)
    response = res.json()["choices"][0]["message"]["content"]
    return response

####-----------------------Frontend---------------------------##########

st.set_page_config(page_title="E-Commerce Competitor Strategy Dashboard", layout="wide")


def apply_custom_css():
    st.markdown(
        """
        <style>
        body {background: linear-gradient(135deg, #1e1e2f, #23262e); color: white;}
        .stApp {backdrop-filter: blur(10px);}
        .sidebar .stSelectbox {background: rgba(255, 255, 255, 0.2);}
        </style>
        """, unsafe_allow_html=True
    )
apply_custom_css()

st.title("🚀 E-Commerce Competitor Strategy Dashboard")
st.sidebar.header("🔍 Select a Product")

products = [
    "HP 15 AI Laptop",
    "SIHOO High Back Home Office Chair",
    "Blue Heaven Cookie & Souffle Matte Lipstick",
    "U.S. Polo Assn. Men's Sneaker",
    "Oneplus Bullets Z2 Bluetooth Wireless in Ear Earphones with Mic",
    "Baybee Run Battery Operated Jeep",
    "PASLDA Wireless Carplay Adapter",
    "GreenFinity Basil/Sabja Seeds",
    "Apple iPhone 12 (64GB) - Black",
    "PAGALY Ultra HD Projector",
    "Classmate Short Notebook",
    "MiNi CoOlEr"

    ]
selected_product = st.sidebar.selectbox("Choose a product to analyze:", products)

competitor_data = load_competitor_data()
reviews_data = load_reviews_data()

product_data = competitor_data[competitor_data["product_name"] == selected_product]
product_reviews = reviews_data[reviews_data["product_name"] == selected_product]

st.header(f"📊 Competitor Analysis for {selected_product}")
st.subheader("📌 Competitor Data")
st.dataframe(product_data.tail(5), use_container_width=True) 

if not product_reviews.empty:
    product_reviews["reviews"] = product_reviews["reviews"].apply(
    lambda x: truncate_text(str(x), 512) if isinstance(x, str) else ""
    )

    #product_reviews["reviews"] = product_reviews["reviews"].apply(lambda x: truncate_text(x, 512))
    sentiments = analyze_sentiment(product_reviews["reviews"].tolist())
    st.subheader("💬 Customer Sentiment Analysis")
    sentiment_df = pd.DataFrame(sentiments)
    fig = px.bar(sentiment_df, x="label", title="Sentiment Analysis Results", color="label") 
    st.plotly_chart(fig)


st.subheader("📈 Price Fluctuations Over Time")

# Convert 'Date' column to datetime with correct format
product_data["Date"] = pd.to_datetime(product_data["Date"], format="%d-%m-%Y", errors="coerce")

# Drop rows where date conversion failed (if any)
product_data = product_data.dropna(subset=["Date"])

# Create a line chart with scatter points for price fluctuations
fig_price_trends = px.line(
    product_data,
    x="Date",
    y="price",
    markers=True,  # Add scatter points on the line
    title=f"Price Fluctuations for {selected_product}",
    labels={"Price": "Price (₹)", "Date": "Date"},
    color_discrete_sequence=["#FFA07A"],  # Change line color (optional)
)

# Display the line chart
st.plotly_chart(fig_price_trends, use_container_width=True)



st.subheader("🔮 Competitor Discount Forecasting")
product_data_with_predictions = forecast_discounts_arima(product_data)

fig = px.area(
    product_data_with_predictions.reset_index(),  # Ensure index is a column
    x="Date",
    y="Predicted_Discount",
    labels={"Predicted_Discount": "Discount Percentage", "Date": "Date"},
    #title="Competitor Discount Forecasting",
    color_discrete_sequence=["#636EFA"]  # Optional: Change color
)
st.plotly_chart(fig, use_container_width=True)


recommendations = generate_strategy_recommendation(selected_product, product_data_with_predictions, sentiments if not product_reviews.empty else "No reviews available")
st.subheader("📢 Strategic Recommendations")
st.info(recommendations)  