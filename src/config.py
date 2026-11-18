"""Чтение и валидация CSV-конфигурации."""

import csv
import os
from typing import Dict

from src.errors import (
    ConfigFileNotFoundError,
    ConfigParseError,
    MissingFieldError,
    InvalidValueError,
)

REQUIRED_FIELDS = [
    "package_name",
    "source",
    "test_mode",
    "output_file",
    "filter_substring",
]

VALID_TEST_MODES = {"on", "off"}


def read_csv(path: str) -> Dict[str, str]:
    """Читает CSV и возвращает словарь."""
    if not os.path.isfile(path):
        raise ConfigFileNotFoundError(
            f"Файл не найден: {path}"
        )
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except csv.Error as e:
        raise ConfigParseError(f"Ошибка CSV: {e}") from e
    if len(rows) != 1:
        raise ConfigParseError(
            "CSV должен содержать ровно одну строку"
        )
    return rows[0]


def validate_config(cfg: Dict[str, str]) -> Dict[str, str]:
    """Валидирует все поля конфигурации."""
    for field in REQUIRED_FIELDS:
        if field not in cfg or not cfg[field].strip():
            raise MissingFieldError(
                f"Отсутствует поле: {field}"
            )
    mode = cfg["test_mode"].strip().lower()
    if mode not in VALID_TEST_MODES:
        raise InvalidValueError(
            f"test_mode должен быть on/off, "
            f"получено: {mode}"
        )
    cfg["test_mode"] = mode
    for key in REQUIRED_FIELDS:
        cfg[key] = cfg[key].strip()
    return cfg


def load_config(path: str) -> Dict[str, str]:
    """Загружает и валидирует конфигурацию."""
    raw = read_csv(path)
    return validate_config(raw)
