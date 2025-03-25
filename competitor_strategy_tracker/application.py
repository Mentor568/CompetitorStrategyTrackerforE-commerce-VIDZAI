import streamlit as st  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
from textblob import TextBlob  # type: ignore
import json
import requests
from datetime import datetime
from fpdf import FPDF

# ✅ Set Streamlit page config
st.set_page_config(page_title="Competitor Strategy Tracker", layout="wide")

# ✅ Load Data
price_file = "combined_price_data1.csv"
reviews_file = "combined_reviews_data11.csv"
analyzed_reviews_file = "analyzed_reviews.csv"

@st.cache_data
def load_data():
    price_data = pd.read_csv(price_file)
    reviews_data = pd.read_csv(reviews_file)
    analyzed_reviews = pd.read_csv(analyzed_reviews_file)
    return price_data, reviews_data, analyzed_reviews

price_data, reviews_data, analyzed_reviews = load_data()

# ✅ Ensure the correct review column exists
review_col = next((col for col in reviews_data.columns if "review" in col.lower()), None)
if review_col is None:
    st.error("No review column found in the reviews CSV file!")
    st.stop()

# ✅ Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative"

# ✅ Perform sentiment analysis
reviews_data["Sentiment"] = reviews_data[review_col].apply(analyze_sentiment)

# ✅ Streamlit Title & Welcome Message
st.title("📊 Competitor Strategy Tracker for E-commerce")
st.markdown("### Welcome! Please select a product from the sidebar to begin analysis.")

# ✅ Sidebar - Product Selection
st.sidebar.header("🔍 Filter Products")
product_list = price_data["Product name"].unique()
selected_product = st.sidebar.selectbox("Select a Product", ["Select a product"] + list(product_list))

# ✅ Ensure a product is selected before showing analysis
if selected_product == "Select a product":
    st.warning("Please select a product from the sidebar to view details.")
    st.stop()

# ✅ Filter Data for Selected Product
filtered_price = price_data[price_data["Product name"] == selected_product]
filtered_reviews = reviews_data[reviews_data["Product name"] == selected_product]
filtered_analyzed_reviews = analyzed_reviews[analyzed_reviews["Product name"] == selected_product]

# ✅ Price & Discount Trends - Line Charts
st.subheader(f"📈 Price & Discount Trends for {selected_product}")
col1, col2 = st.columns(2)

with col1:
    fig_price = px.line(
        filtered_price,
        x="date",
        y="price",
        color="source",
        title="Price Trend Over Time",
        markers=True
    )
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    fig_discount = px.line(
        filtered_price,
        x="date",
        y="discount",
        color="source",
        title="Discount Trend Over Time",
        markers=True
    )
    st.plotly_chart(fig_discount, use_container_width=True)

# ✅ Competitor Prices Table
st.subheader("💰 Latest Competitor Prices")
latest_prices = filtered_price.sort_values(by="date", ascending=False).drop_duplicates(subset=["source"])
st.dataframe(latest_prices[["source", "price", "discount"]])

# ✅ Customer Sentiment Analysis
st.subheader("🧠 Customer Sentiment Analysis")

sentiment_counts = filtered_reviews["Sentiment"].value_counts().reset_index()
sentiment_counts.columns = ["Sentiment", "Count"]

fig_sentiment = px.bar(
    sentiment_counts,
    x="Sentiment",
    y="Count",
    title="Sentiment Analysis Results",
    color="Sentiment",
    color_discrete_map={"Positive": "green", "Negative": "red"}
)
st.plotly_chart(fig_sentiment, use_container_width=True)

# ✅ Predicted Discounts (Placeholder Data)
st.subheader("📉 Competitor Current and Predicted Discounts")
predicted_discounts = filtered_price[["date", "source", "discount"]].tail(3)
predicted_discounts.columns = ["Date", "Source", "Predicted_Discount"]
st.dataframe(predicted_discounts)

# ✅ Strategic Recommendations
st.subheader("📢 Strategic Recommendations")

API_KEY = "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"  # Replace with your actual API key
date = datetime.now()

competitor_data = latest_prices.to_string()
sentiment = sentiment_counts.to_string()

prompt = f"""
You are a highly skilled business strategist specializing in e-commerce. Based on the following details, suggest actionable strategies to optimize pricing, promotions, and customer satisfaction for the selected product:

1. *Product Name*: {selected_product}

2. *Competitor Data* (including current prices, discounts, and predicted discounts):
{competitor_data}

3. *Sentiment Analysis*:
{sentiment}

4. *Today's Date*: {str(date)}

### Task:
- Identify key pricing trends.
- Highlight areas for customer satisfaction improvement.
- Optimize pricing strategies for the next 5 days.
- Recommend promotional campaigns aligned with customer sentiment and trends.

Provide recommendations in this format:
1. *Pricing Strategy*
2. *Promotional Campaign Ideas*
3. *Customer Satisfaction Recommendations*
"""

messages = [{"role": "user", "content": prompt}]

data = {
    "messages": messages,
    "model": "llama3-8b-8192",
    "temperature": 0,
}

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

try:
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", data=json.dumps(data), headers=headers, timeout=10)
    res = res.json()

    if "choices" in res and len(res["choices"]) > 0:
        response = res["choices"][0]["message"]["content"]

        with st.expander("🔹 Pricing Strategy", expanded=True):
            st.markdown(f"✅ **Pricing Strategy:**\n\n{response.split('2.')[0]}")

        with st.expander("🎯 Promotional Campaign Ideas", expanded=False):
            st.markdown(f"📢 **Promotional Campaign Ideas:**\n\n{response.split('2.')[1].split('3.')[0]}")

        with st.expander("💡 Customer Satisfaction Recommendations", expanded=False):
            st.markdown(f"😊 **Customer Satisfaction Recommendations:**\n\n{response.split('3.')[1]}")

    else:
        st.error("⚠️ Unable to generate recommendations. Please check the API response.")

except Exception as e:
    st.error(f"Error generating recommendations: {e}")

st.success("✅ Recommendations generated successfully!")

# ✅ Optional Chatbot for Data Queries
st.subheader("💬 Competitor Insights Chatbot (Optional)")
enable_chatbot = st.checkbox("Enable Chatbot")

if enable_chatbot:
    user_query = st.chat_input("Ask me anything about the competitor data!")

    if user_query:
        chat_prompt = f"""
        You are an expert e-commerce analyst. Based on the following product data, answer the user's query in a simple and insightful manner.

        1. **Product Name**: {selected_product}
        2. **Competitor Data**: {competitor_data}
        3. **Sentiment Analysis**: {sentiment}

        ### User Question:
        {user_query}
        """

        chat_messages = [{"role": "user", "content": chat_prompt}]

        chat_data = {
            "messages": chat_messages,
            "model": "llama3-8b-8192",
            "temperature": 0.5,
        }

        try:
            chat_res = requests.post("https://api.groq.com/openai/v1/chat/completions", data=json.dumps(chat_data), headers=headers, timeout=10)
            chat_res = chat_res.json()

            if "choices" in chat_res and len(chat_res["choices"]) > 0:
                chat_response = chat_res["choices"][0]["message"]["content"]
                st.write("🤖 **Chatbot:**", chat_response)
            else:
                st.error("⚠️ Chatbot could not generate a response.")

        except Exception as e:
            st.error(f"Error in chatbot: {e}")
