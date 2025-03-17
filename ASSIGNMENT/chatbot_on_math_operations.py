import streamlit as st
import re
import json
import random

# Function to generate chat messages
def chat_bot(prompt, temperature=0.7, max_tokens=150, frequency=0.0, json_output=False):
    """
    Simulates a chatbot to solve simple math problems.
    Includes temperature, max_tokens, and frequency parameters.
    Frequency now reduces repetition as it increases.
    """
    try:
        # Use regular expressions to extract numbers and operators
        match = re.search(r"(\d+)\s*([+\-*/])\s*(\d+)", prompt)
        
        if match:
            num1, operator, num2 = match.groups()
            num1, num2 = float(num1), float(num2)
            
            # Perform the basic mathematical operation
            if operator == "+":
                result = f"{num1} + {num2} = {num1 + num2}"
            elif operator == "-":
                result = f"{num1} - {num2} = {num1 - num2}"
            elif operator == "*":
                result = f"{num1} * {num2} = {num1 * num2}"
            elif operator == "/":
                if num2 != 0:
                    result = f"{num1} / {num2} = {num1 / num2}"
                else:
                    result = "Error: Division by zero is not allowed."
            else:
                result = "Unsupported operation."
            
            # Apply randomness based on temperature
            if temperature > 0.5:
                variations = [
                    result,
                    f"The answer is: {result}",
                    f"After calculation: {result}",
                    f"Here's the result: {result}"
                ]
                result = random.choices(variations, weights=[1 - temperature, temperature, temperature, temperature])[0]
            
            # Modify repetition based on frequency
            # Higher frequency reduces repetition
            if frequency < 0.5:  # Low frequency allows a moderate amount of repetition
                result += f" | Repeated: {result}"
            elif frequency < 0.8:  # Moderate frequency reduces repetition further
                result = f"Here is the result: {result}"
            else:  # High frequency eliminates repetition entirely
                result = result
            
            # Truncate the result based on max_tokens
            if len(result) > max_tokens:
                result = result[:max_tokens] + "..."
            
            # Return result in JSON format if selected
            if json_output:
                response_data = {
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "frequency": frequency,
                    "result": result
                }
                return json.dumps(response_data, indent=2)  # Return JSON string
            else:
                # Return normal result
                return result
        else:
            error_message = "I'm not sure I understand. Could you please provide a simple math problem?"
            if json_output:
                return json.dumps({"error": error_message}, indent=2)
            else:
                return error_message
    except Exception as e:
        error_message = f"Error: {e}"
        if json_output:
            return json.dumps({"error": error_message}, indent=2)
        else:
            return error_message

# Streamlit app
st.title("Enhanced Math Chatbot with Streamlit")
st.write("Solve simple math problems with support for randomness, token truncation, and JSON output.")

# User input
prompt = st.text_area("Enter your math problem (e.g., '2 + 3')", value="2 + 3", height=150)
temperature = st.slider("Select Temperature (Randomness)", 0.0, 1.0, 0.7, step=0.1)
max_tokens = st.slider("Max Token Length", 10, 500, 150, step=10)
frequency = st.slider("Frequency (Repetition Control)", 1.0, 0.0, 1.0, step=0.1)
json_output = st.checkbox("Return JSON Format")

# Button to generate response
if st.button("Solve"):
    st.subheader("Bot's Response:")
    with st.spinner("Solving..."):
        response = chat_bot(prompt, temperature=temperature, max_tokens=max_tokens, frequency=frequency, json_output=json_output)
        st.text_area("Response", response, height=250)
