import streamlit as st
import pandas as pd
import plotly.express as px

competitor_data = pd.DataFrame({
    "Competitor": ["Competitor A", "Competitor B", "Competitor C"],
    "Price": [100, 120, 95],
    "Discount": [10, 15, 5],
    "Sentiment": ["Positive", "Neutral", "Negative"]
})

sentiment_data = pd.DataFrame({
    "Sentiment": ["Positive", "Negative"],
    "Count": [1, 1]  # Corrected count values
})


st.set_page_config(page_title="E-Commerce Competitor Strategy Dashboard", layout="wide")


st.sidebar.header("Select a Product")
product_selected = st.sidebar.selectbox("Choose a product to analyze:", ["Product A"])

st.title("E-Commerce Competitor Strategy Dashboard")

st.subheader(f"Competitor Analysis for {product_selected}")
st.dataframe(competitor_data)


st.subheader("Customer Sentiment Analysis")
st.write("### Sentiment Analysis Results")
fig = px.bar(sentiment_data, x='Sentiment', y='Count', color='Sentiment', text='Count')
fig.update_traces(textposition='outside')  # Display count values outside bars
st.plotly_chart(fig, use_container_width=True)


st.subheader("Strategic Recommendations")
st.write("To develop competitive strategies for Product A based on the Competitor Data and Sentiment Analysis, we should focus on three major aspects: pricing, promotions, and customer satisfaction.")
