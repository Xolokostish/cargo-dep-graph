"""Получение зависимостей Rust-пакета (Cargo)."""

import re
import urllib.request
from typing import List

from src.errors import FetchError

CRATES_IO_API = "https://crates.io/api/v1/crates"


def fetch_cargo_toml(package: str) -> str:
    """Скачивает Cargo.toml пакета с crates.io."""
    url = f"{CRATES_IO_API}/{package}"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "cargo-dep-graph/1.0"},
        )
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        raise FetchError(
            f"Не удалось получить {package}: {e}"
        ) from e


def parse_dependencies(toml_content: str) -> List[str]:
    """Парсит секцию [dependencies] из Cargo.toml."""
    deps: List[str] = []
    in_deps = False
    pattern = re.compile(r'^([a-zA-Z0-9_-]+)\s*=')
    for line in toml_content.splitlines():
        stripped = line.strip()
        if stripped == "[dependencies]":
            in_deps = True
            continue
        if stripped.startswith("[") and in_deps:
            break
        if in_deps and pattern.match(stripped):
            name = pattern.match(stripped).group(1)
            deps.append(name)
    return deps


def get_direct_deps(package: str) -> List[str]:
    """Возвращает прямые зависимости пакета."""
    toml = fetch_cargo_toml(package)
    return parse_dependencies(toml)
