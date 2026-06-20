# AIWave Model Reference

Full list of supported models and their capabilities.

**[Get API key ¡ú](https://aiwave.live)**

## DeepSeek

| Model ID | Type | Context | Pricing |
|----------|------|---------|---------|
| `deepseek-v4-pro` | Chat | 128K | Premium |
| `deepseek-chat` (V3) | Chat | 64K | Standard |
| `deepseek-reasoner` (R1) | Reasoning | 64K | Premium |

## GLM (Zhipu)

| Model ID | Type | Context | Pricing |
|----------|------|---------|---------|
| `glm-5.1` | Chat | 128K | Premium |
| `glm-5` | Chat | 128K | Standard |
| `glm-4-flash` | Chat | 128K | Budget |

## Kimi (Moonshot)

| Model ID | Type | Context |
|----------|------|---------|
| `kimi-vl-a3b-thinking` | Vision | 128K |
| `kimi-thinking` | Reasoning | 128K |

## ERNIE (Baidu)

| Model ID | Type | Context |
|----------|------|---------|
| `ernie-4.5` | Chat | 128K |
| `ernie-speed` | Chat | 8K |

## Qwen (Alibaba)

| Model ID | Type | Context |
|----------|------|---------|
| `qwen-3` | Chat | 128K |
| `qwen-3-vl` | Vision | 128K |

*50+ more models available. [View full list ¡ú](https://aiwave.live/pricing)*

## Usage

All models are OpenAI-compatible. Just change the `model` parameter:

```python
from aiwave import AIWave
client = AIWave()

# Switch models by changing one parameter
response = client.chat.completions.create(
    model="deepseek-chat",  # or glm-5, qwen-3, etc.
    messages=[{"role": "user", "content": "Hello!"}]
)
```
