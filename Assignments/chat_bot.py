import requests
import json

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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"
}

# Define system prompt for restaurant and recipe chatbot
messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot that recommends restaurants and recipes based on user preferences. Respond in JSON format."
    }
]

# Chat loop
while True:
    user_prompt = input("What are you in the mood for? (e.g., restaurant, recipe, cuisine type): ")
    messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    data = {
        "model": "qwen-2.5-32b",
        "messages": messages,
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }

    response = requests.post(API_URL, data=json.dumps(data), headers=headers)
    response = response.json()
    output = response["choices"][0]

    # Display the recommendation
    print("Here's a recommendation:")
    print(output["message"]["content"])

    # Add assistant response to conversation history
    messages.append(
        {
            "role": "assistant",
            "content": output["message"]["content"]
        }
    )
