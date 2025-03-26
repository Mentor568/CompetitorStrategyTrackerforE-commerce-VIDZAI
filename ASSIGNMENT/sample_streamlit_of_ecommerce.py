import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# heading
st.title("E-Commerce Competitor Strategy Dashboard")

# Sidebar 
product = st.sidebar.selectbox("Select a Product", ["Product A", "Product B", "Product C"])

# Data 
data = {
    "Product A": {
        "Competitor": ["Competitor A", "Competitor B", "Competitor C"],
        "Price": [100, 120, 110],
        "Discount": [10, 15, 5],
        "Sentiment": ["Positive", "Neutral", "Negative"]
    },
    "Product B": {
        "Competitor": ["Competitor A", "Competitor B", "Competitor C"],
        "Price": [200, 190, 210],
        "Discount": [20, 25, 15],
        "Sentiment": ["Neutral", "Positive", "Negative"]
    },
    "Product C": {
        "Competitor": ["Competitor A", "Competitor B", "Competitor C"],
        "Price": [300, 320, 310],
        "Discount": [30, 35, 25],
        "Sentiment": ["Negative", "Neutral", "Positive"]
    }
}

# table
selected_data = data[product]
df = pd.DataFrame(selected_data)
st.subheader(f"Competitor Data for {product}")
st.table(df)

#  graph chart
st.subheader("Customer Sentiment Analysis")
sentiment_counts = df['Sentiment'].value_counts()
plt.figure(figsize=(6, 4))
plt.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'gray', 'red'])
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.title(f"Sentiment Analysis for {product}")

# render above chart
st.pyplot(plt)

# recommendation  at bottom
st.subheader("Strategic Recommendation")
if product == "Product A":
    st.write("Focus on increasing discounts to match Competitor B's offer and address negative customer sentiment.")
elif product == "Product B":
    st.write("Leverage the positive sentiment around Competitor B to enhance your product's perception.")
elif product == "Product C":
    st.write("Work on competitive pricing and improving customer sentiment to counter Competitor A.")

# Clear the plot after every change of product to give graph chart for selected product
plt.clf()
