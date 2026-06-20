"""Compare responses from different models on the same prompt."""
from aiwave import AIWave
from concurrent.futures import ThreadPoolExecutor

client = AIWave(api_key="***")
models_to_test = ["deepseek-chat", "glm-5", "qwen-3"]
prompt = "Explain the difference between SQL and NoSQL in 2 sentences."

def ask_model(model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

print(f"Prompt: {prompt}\n")
with ThreadPoolExecutor() as executor:
    results = list(executor.map(ask_model, models_to_test))

for model, answer in zip(models_to_test, results):
    print(f"=== {model} ===")
    print(answer)
    print()
