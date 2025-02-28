import streamlit as st 
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Google Gemini API
GOOGLE_API_KEY = "AIzaSyBs3dKPB0IZgZ0NUifqkQCHfiqH0K6lHaI"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.title("AI-Powered Data Analysis Assistant")

uploaded_file = st.file_uploader("Upload a file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.write(df.head())
    
    if st.button("Generate AI Insights"):
        data_summary = df.describe().to_string()
        prompt = f"Analyze this dataset and generate insights:\n\n{data_summary}"
        response = model.generate_content(prompt)
        st.write("### AI Insights")
        st.write(response.text)
    
    # Sidebar for Graph Options
    st.sidebar.header("Choose Graph Type")
    graph_type = st.sidebar.selectbox("Select a plot type", ["Histogram", "Bar Chart", "Line Graph", "Scatter Plot"])
    all_columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select columns", all_columns, default=all_columns[:2])
    
    if st.sidebar.button("Generate Plot"):
        if len(selected_columns) < 1:
            st.warning("Please select at least one column.")
        else:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            if graph_type == "Histogram":
                df[selected_columns].hist(ax=ax, bins=10, color="skyblue")
                plt.title(f"Histogram of {', '.join(selected_columns)}")
                
            elif graph_type == "Bar Chart":
                df[selected_columns[0]].value_counts().plot(kind="bar", ax=ax, color='orange')
                plt.title(f"Bar chart of {selected_columns[0]}")
                
            elif graph_type == "Line Graph":
                df[selected_columns].plot(ax=ax, title="Line Graph")
                
            elif graph_type == "Scatter Plot":
                if len(selected_columns) < 2:
                    st.warning("Scatter plot needs at least 2 columns.")
                else:
                    sns.scatterplot(x=df[selected_columns[0]], y=df[selected_columns[1]], ax=ax)
                    plt.title(f"Scatter Plot: {selected_columns[0]} vs {selected_columns[1]}")
            
            st.pyplot(fig)
