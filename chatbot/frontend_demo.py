import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Competitor Strategy Dashboard", layout="wide")

st.sidebar.header("Select a Product")
st.sidebar.write("Choose a product to analyze:")
selected_product = st.sidebar.selectbox("Choose a product", ["Product A", "Product B", "Product C"])  # Example dropdown

st.markdown("""
    <style>
        .css-1d391kg { background-color: #1e1e1e; }
    </style>
    """, unsafe_allow_html=True)

st.title("E-Commerce Competitor Strategy Dashboard")

competitor_data = pd.DataFrame({
    "Competitor": ["Competitor A", "Competitor B", "Competitor C"],
    "Price": [100, 120, 95],
    "Discount": [10, 15, 5],
    "Sentiment": ["Positive", "Neutral", "Negative"]
})

st.subheader(f"Competitor Analysis for {selected_product}")
st.dataframe(competitor_data, use_container_width=True)

st.subheader("Customer Sentiment Analysis")

data = pd.DataFrame({
    "Sentiment": ["Positive", "Negative"],
    "Count": [2, 2]
})

fig = px.bar(data, x="Sentiment", y="Count", title="Sentiment Analysis Results", color="Sentiment")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Strategic Recommendations")
st.write("""
To develop competitive strategies for **Product A** based on the Competitor Data and Sentiment Analysis,
we should focus on three major aspects: **pricing, promotions, and customer satisfaction**.
Here are some strategies to consider:

- Optimize pricing strategies to remain competitive.
- Offer better promotions or discounts to attract customers.
""")
