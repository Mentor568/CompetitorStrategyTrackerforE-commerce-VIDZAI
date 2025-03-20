import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit Page Config
st.set_page_config(page_title="E-Commerce Strategy Dashboard", layout="wide")

# Sidebar: Product Selection
st.sidebar.header("Select a Product")
product = st.sidebar.selectbox("Choose a product to analyze:", ["Product A", "Product B", "Product C"])

# Main Title
st.title("E-Commerce Competitor Strategy Dashboard")

# Sample Data
competitor_data = {
    "Competitor": ["Competitor A", "Competitor B", "Competitor C"],
    "Price": [105, 130, 90],
    "Discount": [12, 18, 7],
    "Sentiment": ["Positive", "Neutral", "Negative"],
}

df = pd.DataFrame(competitor_data)

# Display Competitor Analysis Table
st.subheader(f"Competitor Analysis for {product}")
st.dataframe(df)

# Customer Sentiment Analysis
st.subheader("Customer Sentiment Analysis")

sentiment_data = pd.DataFrame({
    "Sentiment": ["Positive", "Negative"],
    "Count": [2, 2]
})

# Sentiment Bar Chart
fig = px.bar(sentiment_data, x="Sentiment", y="Count", title="Sentiment Analysis Results", text="Count")
fig.update_traces(marker_color=['#4caf50', '#f44336'])
st.plotly_chart(fig, use_container_width=True)

# Strategic Recommendations
st.subheader("Strategic Recommendations")
st.write(
    f"""
    To develop competitive strategies for **{product}** based on the Competitor Data and Sentiment Analysis, consider these strategies:

    - **Competitor A:** Competitive pricing and positive sentiment — consider matching price or improving product features.
    - **Competitor B:** High price with discounts — explore bundling or loyalty programs to win price-sensitive customers.
    - **Competitor C:** Lowest price but negative sentiment — an opportunity to differentiate on quality and service.
    """
)

# Run this script using: `streamlit run script_name.py`
