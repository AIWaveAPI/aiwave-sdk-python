import re
from pathlib import Path

from setuptools import setup, find_packages

# Single source of truth for the version: pyproject.toml [project].version.
# This file previously carried its own literal, which drifted two releases
# behind pyproject.toml and left aiwave.__version__ reporting 0.2.0 in the
# published 0.2.1 wheel. setuptools ignores this argument when [project] is
# present, so the copy could go stale without anyone noticing.
_version = re.search(
    r'^version\s*=\s*"([^"]+)"',
    Path(__file__).with_name("pyproject.toml").read_text(encoding="utf-8"),
    re.MULTILINE,
).group(1)

setup(
    name="aiwave",
    version=_version,
    description="AIWave client for compatible chat requests and AI video routes",
    long_description=open("README.md", encoding="utf-8").read(),
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
