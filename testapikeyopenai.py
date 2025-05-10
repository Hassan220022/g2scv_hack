from openai import OpenAI
import os

# Get the API key from environment variable
# You should set this using: export OPENAI_API_KEY="your-api-key"
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("⚠️ No API key found. Please set the OPENAI_API_KEY environment variable.")
    print("Example: export OPENAI_API_KEY='your-api-key'")
    exit(1)

# Initialize the client
client = OpenAI(api_key=api_key)

try:
    # Use the new client API format
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ],
        max_tokens=10
    )
    print("✅ OpenAI API key is valid.")
    print("Response:", response.choices[0].message.content)

except Exception as e:
    if "authentication" in str(e).lower() or "invalid api key" in str(e).lower():
        print("❌ Invalid OpenAI API key.")
    else:
        print("⚠️ An error occurred:", str(e))
