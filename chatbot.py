import requests
import json

# API Key (Hardcoded)
API_KEY = "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"

API_URL = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Initial System Prompt for Career Guidance
messages = [
    {
        "role": "system",
        "content": "You are a career guidance chatbot. Provide career advice, skill recommendations, and learning resources in JSON format."
    }
]

# Function to format the response properly
def format_response(response_data):
    result = []
    for key, value in response_data.items():
        if isinstance(value, list):
            # Handle nested lists or dicts inside lists
            formatted_list = []
            for item in value:
                if isinstance(item, dict):
                    formatted_list.append(
                        f"Title: {item.get('title', 'N/A')}, Description: {item.get('description', 'N/A')}, "
                        f"Requirements: {', '.join(item.get('requirements', []))}, "
                        f"Learning Resources: {', '.join(item.get('learning_resources', []))}"
                    )
                else:
                    formatted_list.append(str(item))
            result.append(f"- {key.capitalize()}: \n  - " + "\n  - ".join(formatted_list))
        elif isinstance(value, dict):
            # Handle nested dictionaries
            nested_info = ", ".join(f"{k}: {v}" for k, v in value.items())
            result.append(f"- {key.capitalize()}: {nested_info}")
        else:
            result.append(f"- {key.capitalize()}: {value}")
    return "\n".join(result)

# Chat Loop for User Interaction
while True:
    user_prompt = input("Ask me anything about career guidance: ")
    if user_prompt.lower() in ["exit", "quit", "bye"]:
        print("Goodbye! Feel free to ask me anytime.")
        break

    messages.append({"role": "user", "content": user_prompt})

    data = {
        "model": "qwen-2.5-32b",
        "messages": messages,
        "temperature": 0.6,
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(API_URL, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        output = response.json()["choices"][0]

        # Display JSON response in a clear format
        career_response = output["message"]["content"]
        parsed_response = json.loads(career_response)

        print("\nCareer Guidance:")
        print(format_response(parsed_response))

        messages.append({"role": "assistant", "content": career_response})
    except Exception as e:
        print(f"Error: {e}\nPlease try again.")
