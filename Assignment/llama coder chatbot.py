import streamlit as st
import requests

# Set up API details (use Hugging Face Inference API)
HF_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
HF_API_KEY = "YOUR_HF_API_KEY"  # Replace with your actual Hugging Face API key

# Function to query the LLaMA 2 model
def generate_code(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt, "parameters": {"max_length": 300, "temperature": 0.7}}

    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "Error: Unable to generate a response. Please try again."

# Streamlit UI Setup
st.set_page_config(page_title="🦙 Llama Coder", layout="centered")
st.title("🦙 Llama Coder - AI Coding Assistant")
st.write("Generate code snippets using LLaMA 2 AI.")

# User input area
prompt = st.text_area("Enter your coding query:", "Write a Python function to sort a list.")

# Generate button
if st.button("Generate Code"):
    with st.spinner("Generating code..."):
        response = generate_code(prompt)
    st.code(response, language="python")

# Sidebar options
st.sidebar.header("About Llama Coder")
st.sidebar.write(
    """
    - Uses **Meta's LLaMA 2** model
    - Supports Python, Java, C++, and more
    - Built with **Streamlit**
    """
)

st.sidebar.markdown("### How to Use:")
st.sidebar.write(
    """
    1. Enter a **coding question or request**.
    2. Click **Generate Code**.
    3. Wait for the AI to generate a response.
    """
)
