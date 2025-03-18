import streamlit as st
from music_chatbot import get_music_recommendation


st.set_page_config(page_title="🎵 Music Recommender Bot", page_icon="🎧")
st.title("🎧 Music Recommendation Chatbot")
st.write("Tell me your mood or activity, and I'll recommend some songs!")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


st.write("### Chat History")
for sender, message in st.session_state["chat_history"]:
    st.markdown(f"**{sender}:** {message}")


user_input = st.text_input("You:", "")


if st.button("Send") and user_input.strip():
    response = get_music_recommendation(user_input)

   
    st.session_state["chat_history"].append(("You", user_input))
    st.session_state["chat_history"].append(("Bot", response))

    
    st.rerun()  # ✅ Fixed line


if st.button("Clear Chat"):
    st.session_state["chat_history"] = []
    st.rerun()  # ✅ Fixed line
