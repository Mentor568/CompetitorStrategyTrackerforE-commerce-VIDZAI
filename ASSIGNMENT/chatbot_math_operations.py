import streamlit as st
from streamlit_chat import message as st_message
import ast
import random
import json

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Initialize control parameters
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7  # Default randomness
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 50  # Default maximum output tokens
if "stream_response" not in st.session_state:
    st.session_state.stream_response = False  # Toggle for response streaming
if "output_json" not in st.session_state:
    st.session_state.output_json = False  # Toggle for JSON output

st.title("Advanced Chatbot with Math Operations")

# Sidebar for adjusting controls
st.sidebar.title("Output Controls")
st.session_state.temperature = st.sidebar.slider(
    "Temperature (Randomness)", 0.0, 1.0, 0.7, 0.1
)
st.session_state.max_tokens = st.sidebar.slider(
    "Max Tokens (Output Length)", 10, 100, 50, 10
)
st.session_state.stream_response = st.sidebar.checkbox("Enable Response Streaming")
st.session_state.output_json = st.sidebar.checkbox("Enable JSON Output")

# Function to evaluate mathematical expressions safely
def evaluate_expression(expression):
    try:
        # Allow only basic operations (addition, subtraction, multiplication, division)
        allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.operator, ast.unaryop)
        node = ast.parse(expression, mode='eval')
        if all(isinstance(n, allowed_nodes) for n in ast.walk(node)):
            result = eval(expression)
            return f"The result is: {result}"  # Return result as string
        else:
            return "Unsupported operation. Please use basic math operations only."
    except Exception:
        return "Invalid mathematical expression. Please check your input."

# Function to generate chatbot responses
def generate_answer():
    user_message = st.session_state.input_text.strip()
    if user_message:
        predefined_responses = {
            "hello": "Hi there! How can I assist you today?",
            "how are you": "I'm just a bot, but I'm here to help!",
            "bye": "Goodbye! Have a great day!",
        }

        if user_message.lower() in predefined_responses:
            message_bot = predefined_responses[user_message.lower()]
        else:
            # Check for math operations
            try:
                # Attempt to evaluate the input as a mathematical expression
                if any(op in user_message for op in "+-*/") or user_message.replace(" ", "").isnumeric():
                    message_bot = evaluate_expression(user_message)
                else:
                    # Generate a randomized response if not math-related
                    responses = [
                        "I'm here to help with that!",
                        "Could you clarify your question?",
                        "That's interesting! Let's dive into it.",
                        "I'd love to assist you further!",
                    ]
                    random.seed(int(st.session_state.temperature * 100))  # Adjust seed with temperature
                    message_bot = random.choice(responses)
            except Exception as e:
                message_bot = f"Error processing your request: {e}"

        # Truncate response to max tokens if enabled
        if len(message_bot) > st.session_state.max_tokens:
            message_bot = message_bot[:st.session_state.max_tokens]

        # Format response as JSON if enabled
        if st.session_state.output_json:
            message_bot = json.dumps({"response": message_bot}, indent=4)

        # Append user and bot messages to chat history
        st.session_state.history.append({"message": user_message, "is_user": True})
        st.session_state.history.append({"message": message_bot, "is_user": False})

# Input field for user messages with on_change callback
st.text_input("Talk to the bot(give input as 2+2,3*4,8/4,4-5...)", key="input_text", on_change=generate_answer)

# Display chat history
for i, chat in enumerate(st.session_state.history):
    if st.session_state.stream_response:
        # Simulate streaming response (for demonstration, split by word)
        parts = chat["message"].split()
        for j, part in enumerate(parts):
            st_message(message=part, is_user=chat["is_user"], key=f"stream_{i}_{j}")
    else:
        st_message(**chat, key=str(i))  # Unpack dictionary for standard messages
