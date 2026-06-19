"""
Тесты для разбора start-payload Telegram (services.deeplink).
Чистая функция: без сети, aiogram и config.
"""
import pytest

from services.deeplink import parse_start_payload


# --- Валидный payload --------------------------------------------------------

def test_valid_simple_id():
    """obj_<id> с простым id -> id."""
    assert parse_start_payload("obj_museum") == "museum"


def test_valid_id_with_hyphens():
    """Дефисы внутри id допустимы."""
    assert parse_start_payload("obj_susanino-museum") == "susanino-museum"


def test_valid_id_with_digits():
    """Цифры в id допустимы."""
    assert parse_start_payload("obj_obj-12-3") == "obj-12-3"


# --- Невалидный payload -> None ----------------------------------------------

def test_none_returns_none():
    """None -> None."""
    assert parse_start_payload(None) is None


def test_empty_string_returns_none():
    """Пустая строка -> None."""
    assert parse_start_payload("") is None


def test_no_prefix_returns_none():
    """Строка без префикса obj_ -> None."""
    assert parse_start_payload("foo") is None


def test_wrong_prefix_returns_none():
    """Неверный префикс -> None."""
    assert parse_start_payload("object_museum") is None


def test_empty_id_returns_none():
    """obj_ без id -> None."""
    assert parse_start_payload("obj_") is None


def test_uppercase_id_returns_none():
    """Заглавные буквы вне whitelist -> None."""
    assert parse_start_payload("obj_Bad") is None


def test_underscore_in_id_returns_none():
    """Подчёркивание/верхний регистр в id -> None (id = [a-z0-9-])."""
    assert parse_start_payload("obj_Bad_UPPER") is None


def test_garbage_returns_none():
    """Произвольный мусор -> None."""
    assert parse_start_payload("!!!") is None


def test_id_with_space_returns_none():
    """Пробел в id -> None."""
    assert parse_start_payload("obj_a b") is None


def test_only_prefix_underscore_variants():
    """obj без подчёркивания -> None."""
    assert parse_start_payload("obj") is None
