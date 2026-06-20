from setuptools import setup, find_packages

setup(
    name="aiwave",
    version="0.1.0",
    description="AIWave API — One API key for 50+ Chinese AI models (DeepSeek, GLM, Kimi, etc.), OpenAI compatible",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="AIWave",
    author_email="support@aiwave.live",
    url="https://aiwave.live",
    packages=find_packages(),
    install_requires=["openai>=1.0.0"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai, llm, deepseek, glm, kimi, openai, api, chinese-ai, aiwave",
)
