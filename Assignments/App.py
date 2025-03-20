import streamlit as st
import requests
import json

# API Setup
API_URL = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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"
}

# Set Streamlit page configuration
st.set_page_config(page_title="Restaurant & Recipe Chatbot", layout="centered")

# Title
st.title("Restaurant & Recipe Chatbot")
st.write("Get personalized restaurant and recipe recommendations!")

# User input
user_prompt = st.text_input("What are you in the mood for? (e.g., restaurant, recipe, cuisine type):")

if st.button("Get Recommendation") and user_prompt:
    messages = [
        {"role": "system", "content": "You are a friendly chatbot that recommends restaurants and recipes based on user preferences. Respond in JSON format."},
        {"role": "user", "content": user_prompt}
    ]

    data = {
        "model": "qwen-2.5-32b",
        "messages": messages,
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }

    # API Request
    response = requests.post(API_URL, data=json.dumps(data), headers=headers)
    response = response.json()
    
    try:
        output = response["choices"][0]["message"]["content"]
        st.success("Here's a recommendation:")
        st.write(output)
    except Exception as e:
        st.error("Something went wrong! Please try again.")

# Run the app with 'streamlit run script_name.py'