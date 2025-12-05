"""Configuration loading module."""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration."""

    ollama_host: str = "http://localhost:11434"
    model: str = "qwen3-vl:8b"
    system_prompt: str = "Describe this image in detail."
    temperature: float = 0.7
    supported_extensions: list[str] = field(
        default_factory=lambda: [".jpg", ".jpeg", ".png", ".webp", ".gif"]
    )
    description_suffix: str = ""


def load_config(config_path: Path | None = None, suffix: str | None = None) -> Config:
    """Load configuration from .env and optional YAML file.

    Priority (highest to lowest):
        1. CLI arguments (suffix)
        2. Environment variables (.env)
        3. YAML config file
        4. Default values

    Args:
        config_path: Path to YAML configuration file.
        suffix: Suffix to append to descriptions (from CLI).

    Returns:
        Config: The loaded configuration object.
    """
    # Start with defaults
    ollama_host = Config.ollama_host
    model = Config.model
    system_prompt = Config.system_prompt
    temperature = Config.temperature
    supported_extensions = Config().supported_extensions
    description_suffix = Config.description_suffix

    # Load from YAML if exists
    if config_path is None:
        config_path = Path("config.yaml")

    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        system_prompt = data.get("system_prompt", system_prompt)
        temperature = data.get("temperature", temperature)
        supported_extensions = data.get("supported_extensions", supported_extensions)

    # Override with environment variables
    ollama_host = os.getenv("OLLAMA_HOST", ollama_host)
    model = os.getenv("OLLAMA_MODEL", model)

    # Override suffix with CLI argument if provided
    if suffix is not None:
        description_suffix = suffix

    return Config(
        ollama_host=ollama_host,
        model=model,
        system_prompt=system_prompt,
        temperature=temperature,
        supported_extensions=supported_extensions,
        description_suffix=description_suffix,
    )
