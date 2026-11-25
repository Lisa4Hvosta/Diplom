"""Конфигурация проекта: адреса и ключи вынесены в .env."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ApiConfig:
    """Настройки доступа к API kinopoisk.dev."""

    base_url: str
    api_key: str
    timeout: float


def load_api_config() -> ApiConfig:
    """Читает настройки API из переменных окружения."""
    return ApiConfig(
        base_url=os.getenv("KINOPOISK_API_URL", "https://api.kinopoisk.dev"),
        api_key=os.getenv("KINOPOISK_TOKEN", ""),
        timeout=float(os.getenv("API_TIMEOUT", "10")),
    )
