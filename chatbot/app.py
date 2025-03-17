import streamlit as st
import requests
import json

# API Configuration
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

st.title("🐾 Animal Knowledge Chatbot")
st.write("Ask me anything about animals!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a bot that provides general knowledge about animals."}]

user_input = st.text_input("Type your question here:")
if st.button("Ask"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        data = {
            "model": "qwen-2.5-32b",
            "messages": st.session_state.messages,
            "temperature": 0.7,
            "response_format": {"type": "json_object"}
        }

        response = requests.post(API_URL, data=json.dumps(data), headers=headers).json()

        if "choices" in response and response["choices"]:
            chatbot_response = response["choices"][0]["message"]["content"]
            st.write(f"🤖 Chatbot: {chatbot_response}")
            st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
