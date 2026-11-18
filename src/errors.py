"""Кастомные исключения приложения."""


class ConfigError(Exception):
    """Базовая ошибка конфигурации."""


class ConfigFileNotFoundError(ConfigError):
    """Файл конфигурации не найден."""


class ConfigParseError(ConfigError):
    """Ошибка разбора CSV."""


class MissingFieldError(ConfigError):
    """Отсутствует обязательное поле."""


class InvalidValueError(ConfigError):
    """Недопустимое значение поля."""


class FetchError(Exception):
    """Ошибка получения данных о пакете."""


class ParseError(Exception):
    """Ошибка парсинга Cargo.toml."""
