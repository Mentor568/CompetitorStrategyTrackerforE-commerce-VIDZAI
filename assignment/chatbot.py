import streamlit as st
from streamlit_chat import message as chat_message
import json

# Initialize chat history
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# UI Controls
if "response_variation" not in st.session_state:
    st.session_state.response_variation = 0.7
if "text_limit" not in st.session_state:
    st.session_state.text_limit = 50
if "enable_stream" not in st.session_state:
    st.session_state.enable_stream = False
if "json_mode" not in st.session_state:
    st.session_state.json_mode = False

# Page title
st.title("Seasonal Outfit Guide")

# Sidebar controls
st.sidebar.header("Settings")
st.session_state.response_variation = st.sidebar.slider(
    "Response Variation", 0.0, 1.0, 0.7, 0.1
)
st.session_state.text_limit = st.sidebar.slider(
    "Max Response Length", 10, 100, 50, 10
)
st.session_state.enable_stream = st.sidebar.checkbox("Stream Response")
st.session_state.json_mode = st.sidebar.checkbox("Show Response in JSON Format")

# Outfit suggestions dictionary
outfit_suggestions = {
    "summer": "Stay cool in light, breathable fabrics like cotton and linen. Opt for shorts, loose t-shirts, and sunglasses!",
    "winter": "Bundle up with wool sweaters, thermal wear, and a warm coat. Accessories like scarves and gloves are essential!",
    "spring": "Spring calls for layering! Try a light jacket, floral prints, and comfy sneakers for a fresh look!",
    "autumn": "Go for cozy sweaters, ankle boots, and earthy tones. A trench coat makes for a stylish fall outfit!"
}

# Function to process user queries
def get_response():
    user_input = st.session_state.user_query.strip().lower()
    if user_input:
        bot_reply = outfit_suggestions.get(user_input, "I’d love to help! Which season’s fashion are you looking for?")
        
        # Trim response if exceeding max token limit
        if len(bot_reply) > st.session_state.text_limit:
            bot_reply = bot_reply[:st.session_state.text_limit]
        
        # Format as JSON if enabled
        if st.session_state.json_mode:
            bot_reply = json.dumps({"response": bot_reply}, indent=4)
        
        # Store conversation history
        st.session_state.chat_log.append({"message": user_input, "is_user": True})
        st.session_state.chat_log.append({"message": bot_reply, "is_user": False})

# User input field
st.text_input("Ask about seasonal outfits (e.g., 'summer', 'winter', 'spring', 'autumn'):", key="user_query", on_change=get_response)

# Display chat history
for index, chat in enumerate(st.session_state.chat_log):
    if st.session_state.enable_stream:
        # Simulate streaming response (word-by-word display)
        words = chat["message"].split()
        for idx, word in enumerate(words):
            chat_message(message=word, is_user=chat["is_user"], key=f"stream_{index}_{idx}")
    else:
        chat_message(**chat, key=str(index))