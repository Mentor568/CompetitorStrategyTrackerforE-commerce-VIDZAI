import requests
import json

# API Key (Hardcoded)
API_KEY = "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"

API_URL = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Initial System Prompt for Mental Wellness Guidance
messages = [
    {
        "role": "system",
        "content": "You are a mental wellness chatbot. Provide advice on stress management, mindfulness techniques, emotional well-being, and self-care tips in JSON format."
    }
]

# Function to format the response properly
def format_response(response_data):
    result = []
    for key, value in response_data.items():
        if isinstance(value, list):
            formatted_list = []
            for item in value:
                if isinstance(item, dict):
                    formatted_list.append(
                        f"Title: {item.get('title', 'N/A')}, Description: {item.get('description', 'N/A')}, "
                        f"Steps: {', '.join(item.get('steps', []))}, "
                        f"Resources: {', '.join(item.get('resources', []))}"
                    )
                else:
                    formatted_list.append(str(item))
            result.append(f"- {key.capitalize()}: \n  - " + "\n  - ".join(formatted_list))
        elif isinstance(value, dict):
            nested_info = ", ".join(f"{k}: {v}" for k, v in value.items())
            result.append(f"- {key.capitalize()}: {nested_info}")
        else:
            result.append(f"- {key.capitalize()}: {value}")
    return "\n".join(result)

# Chat Loop for User Interaction
while True:
    user_prompt = input("Ask me anything about mental wellness: ")
    if user_prompt.lower() in ["exit", "quit", "bye"]:
        print("Take care! Remember to prioritize your well-being.")
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
        wellness_response = output["message"]["content"]
        parsed_response = json.loads(wellness_response)

        print("\nMental Wellness Guidance:")
        print(format_response(parsed_response))

        messages.append({"role": "assistant", "content": wellness_response})
    except Exception as e:
        print(f"Error: {e}\nPlease try again.")