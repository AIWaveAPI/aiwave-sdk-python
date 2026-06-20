"""Streaming chat completion example."""
from aiwave import AIWave

client = AIWave(api_key="***")

stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Write a short poem about AI"}],
    stream=True
)

print("Streaming response:\n")
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
