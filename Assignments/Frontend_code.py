import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="E-Commerce Competitor Strategy Dashboard", layout="wide")


# Sidebar
st.sidebar.header("Select a Product")
st.sidebar.write("Choose a product to analyze:")
selected_product = st.sidebar.selectbox("Product Selection", ["Product A", "Product B", "Product C"], index=0)

# Main Title
st.markdown("# E-Commerce Competitor Strategy Dashboard")

# Competitor Analysis Data
competitor_data = pd.DataFrame({
    "Competitor": ["Competitor A", "Competitor B", "Competitor C"],
    "Price": [100, 120, 95],
    "Discount": [10, 15, 5],
    "Sentiment": ["Positive", "Neutral", "Negative"]
})

st.markdown("## Competitor Analysis for " + selected_product)
st.dataframe(competitor_data, hide_index=True)

# Customer Sentiment Analysis
st.markdown("## Customer Sentiment Analysis")
sentiment_counts = pd.DataFrame({
    "Sentiment": ["Positive", "Negative"],
    "Count": [2, 2]  # Example count values
})
fig = px.bar(sentiment_counts, x="Sentiment", y="Count", text="Count", title="Sentiment Analysis Results",
             color_discrete_sequence=["#76C7C0"], height=400)
st.plotly_chart(fig, use_container_width=True)

# Strategic Recommendations
st.markdown("## Strategic Recommendations")
st.write(
    "To develop competitive strategies for " + selected_product +
    " based on the Competitor Data and Sentiment Analysis, we should focus on three major aspects: pricing, promotions, and customer satisfaction."
)
