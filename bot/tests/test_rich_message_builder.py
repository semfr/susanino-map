"""
Тесты построителя rich-карточки объекта под Telegram Bot API 10.1.

Модуль не делает сети/отправки — только формирует HTML и метаданные локации.
Контракт: build_object_rich_message(obj: dict) -> dict
  -> { "html": str, "has_location": bool, и при наличии координат "lat","lng" }
"""
from services.rich_message_builder import build_object_rich_message


# --- Фикстуры данных ---

def _full_object() -> dict:
    """Полный объект с координатами, адресом, телефоном и часами работы."""
    return {
        "name": "Краеведческий музей",
        "description": "Музей в селе Сусанино.",
        "address": "Костромская обл., с. Сусанино, ул. Ленина, д. 31",
        "contacts": {"phone": "+7 (49434) 9-05-20"},
        "schedule": {"regular": "Ежедневно 09:00–17:30"},
        "coordinates": {"real": {"lat": 58.1472, "lng": 41.5892}},
    }


# --- Кейс 1: полный объект ---

def test_full_object_html_contains_escaped_name():
    obj = _full_object()
    result = build_object_rich_message(obj)
    assert "Краеведческий музей" in result["html"]


def test_full_object_has_tg_map_with_lat_and_long():
    obj = _full_object()
    result = build_object_rich_message(obj)
    html = result["html"]
    assert "<tg-map" in html
    assert 'lat="58.1472"' in html
    assert 'long="41.5892"' in html
    assert "</tg-map>" in html


def test_full_object_has_location_true_and_coords_returned():
    obj = _full_object()
    result = build_object_rich_message(obj)
    assert result["has_location"] is True
    assert result["lat"] == 58.1472
    assert result["lng"] == 41.5892


def test_full_object_lists_address_phone_hours():
    obj = _full_object()
    html = build_object_rich_message(obj)["html"]
    assert "Костромская обл., с. Сусанино, ул. Ленина, д. 31" in html
    assert "+7 (49434) 9-05-20" in html
    assert "Ежедневно 09:00–17:30" in html


# --- Кейс 2: объект без coordinates.real ---

def test_object_without_real_coords_has_no_location():
    obj = {"name": "Без координат", "description": "Текст."}
    result = build_object_rich_message(obj)
    assert result["has_location"] is False
    assert "<tg-map" not in result["html"]
    assert "lat" not in result
    assert "lng" not in result


def test_object_with_empty_real_coords_has_no_location():
    obj = {
        "name": "Пустые координаты",
        "coordinates": {"real": {}},
    }
    result = build_object_rich_message(obj)
    assert result["has_location"] is False
    assert "<tg-map" not in result["html"]


# --- Кейс 3: спецсимволы в name экранируются ---

def test_special_chars_in_name_are_escaped():
    obj = {"name": "Кафе & <Бар> \"Уют\""}
    html = build_object_rich_message(obj)["html"]
    assert "&amp;" in html
    assert "&lt;Бар&gt;" in html
    # Сырые непарные символы не должны протекать в HTML
    assert "& <" not in html
    assert "<Бар>" not in html


# --- Устойчивость: отсутствующие поля не валят построитель ---

def test_missing_optional_fields_do_not_crash():
    obj = {"name": "Минимальный"}
    result = build_object_rich_message(obj)
    assert isinstance(result["html"], str)
    assert result["has_location"] is False


def test_description_is_escaped():
    obj = {"name": "Имя", "description": "Описание с <тегом> & амперсандом"}
    html = build_object_rich_message(obj)["html"]
    assert "&lt;тегом&gt;" in html
    assert "&amp;" in html
