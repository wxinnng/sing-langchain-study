"""Compatibility configuration for running a quick script from the project root."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent

CONDA_ENV_NAME = "langchain1.2"

load_dotenv(PROJECT_ROOT / ".env", override=False)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"缺少环境变量: {name}")
    return value
