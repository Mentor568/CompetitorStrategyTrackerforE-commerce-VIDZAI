import streamlit as st  
import pandas as pd  
import numpy as np  
import time  

# Title and welcome message  
st.title("🚀 Welcome to the Fun-O-Meter App! 🎉")  
st.write("Hello, adventurer! 🌟 Get ready for an interactive and exciting experience! 🎭")

# Collect user info  
st.subheader("👋 Who’s Joining the Fun?")  
username = st.text_input("Enter your awesome name:")
if username:
    st.write(f"Nice to meet you, {username}! 🎈 Let's get started!")

# Fun mood selector  
st.subheader("🌈 What's Your Mood Today?")  
mood = st.radio("Pick a mood:", ["😁 Happy", "😴 Sleepy", "🤩 Excited", "🤔 Curious", "😎 Chill"])  
st.write(f"You’re feeling {mood} today! Let's match that energy! ⚡")

# Age guess game  
st.subheader("🔮 Let's Guess Your Age!")  
guess = st.number_input("Enter your best guess for a random number between 1-100:", 1, 100, 50)
real_age = np.random.randint(1, 101)

if st.button("Reveal Age! 🎭"):
    time.sleep(1)
    if guess == real_age:
        st.success(f"🎯 Whoa! You guessed it right! Your age is {real_age}! 🎉")
    else:
        st.error(f"Oops! Not quite. The magic number is {real_age}. Try again! 🔁")

# Surprise animation  
st.subheader("🎁 Click for a Surprise!")  
if st.button("Surprise Me! 🎊"):
    st.snow()
    st.balloons()
    st.success("✨ Surprise! Wishing you a fantastic day ahead! 🌟")

# Interactive bar chart  
st.subheader("📊 Your Personalized Fun Chart")  
st.write("A chart as unique as you are! 🎨")

fun_data = pd.DataFrame(
    np.random.randint(1, 100, size=(10, 3)),  
    columns=["Fun Level", "Energy Boost", "Happiness Score"]  
)
st.bar_chart(fun_data)

# A funny fact to end the session  
st.subheader("😂 Did You Know?")  
facts = [
    "Bananas are berries, but strawberries aren’t! 🍌",
    "A group of flamingos is called a 'flamboyance'! 🦩",
    "Honey never spoils. Archaeologists found 3000-year-old honey that's still edible! 🍯",
    "Wombat poop is cube-shaped. Yes, really! 🦘",
    "Octopuses have three hearts. ❤️❤️❤️"
]

if st.button("Tell Me a Fun Fact! 🤓"):
    st.write(np.random.choice(facts))

# Closing message  
st.write("Thanks for playing along! 🚀 Keep spreading the fun! 😃✨")  
