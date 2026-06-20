"""Basic chat completion example using AIWave SDK."""
from aiwave import AIWave

# Initialize client (set AIWAVE_API_KEY env var or pass directly)
client = AIWave(api_key="***")

# List available models
print("Available models (first 10):")
models = client.models.list()
for m in models.data[:10]:
    print(f"  {m.id:30s} | {m.owned_by}")

# Chat completion
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Explain quantum entanglement in one paragraph."}
    ],
    temperature=0.7,
    max_tokens=500
)

print("\n" + "=" * 60)
print("Response:")
print(response.choices[0].message.content)
print(f"\nModel: {response.model}, Tokens: {response.usage.total_tokens}")
