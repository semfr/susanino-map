"""
Построитель rich-карточки объекта под Telegram Bot API 10.1.

Чистый Python: НЕ ходит в сеть и ничего не отправляет — только формирует
HTML-строку и метаданные локации. Весь пользовательский текст экранируется
через html.escape, чтобы спецсимволы (& < >) не ломали разметку.

Карта в Bot API 10.1 встраивается тегом:
    <tg-map lat=".." long=".." zoom="15"></tg-map>

Контракт:
    build_object_rich_message(obj: dict) -> dict
    Возвращает { "html": str, "has_location": bool }
    и при наличии координат дополнительно "lat", "lng".
"""
import html
from typing import Any

# Зум карты по умолчанию для встраиваемого <tg-map>.
_DEFAULT_MAP_ZOOM = 15


def _esc(value: Any) -> str:
    """Безопасно приводит значение к строке и экранирует HTML-спецсимволы."""
    return html.escape(str(value))


def _extract_real_coords(obj: dict) -> tuple[float, float] | None:
    """
    Достаёт (lat, lng) из coordinates.real, если обе координаты заданы.
    Возвращает None, если блока нет или координаты неполные/пустые.
    """
    coords = obj.get("coordinates")
    if not isinstance(coords, dict):
        return None
    real = coords.get("real")
    if not isinstance(real, dict):
        return None
    lat = real.get("lat")
    lng = real.get("lng")
    if lat is None or lng is None:
        return None
    return lat, lng


def build_object_rich_message(obj: dict) -> dict:
    """
    Формирует rich-карточку объекта для Telegram Bot API 10.1.

    Args:
        obj: словарь объекта карты (как в objects.json).

    Returns:
        dict с ключами:
          - "html": готовая HTML-строка карточки;
          - "has_location": bool, есть ли реальные координаты;
          - "lat", "lng": присутствуют только при наличии координат.
    """
    parts: list[str] = []

    # Заголовок (name) — обязательный по смыслу, но отсутствие не валит построитель.
    name = obj.get("name")
    if name:
        parts.append(f"<b>{_esc(name)}</b>")

    # Описание.
    description = obj.get("description")
    if description:
        parts.append(_esc(description))

    # Координаты -> блок встраиваемой карты <tg-map>.
    coords = _extract_real_coords(obj)
    has_location = coords is not None
    if coords is not None:
        lat, lng = coords
        parts.append(
            f'<tg-map lat="{_esc(lat)}" long="{_esc(lng)}" '
            f'zoom="{_DEFAULT_MAP_ZOOM}"></tg-map>'
        )

    # Адрес / телефон / часы — списком при наличии.
    details: list[str] = []

    address = obj.get("address")
    if address:
        details.append(f"Адрес: {_esc(address)}")

    contacts = obj.get("contacts")
    phone = contacts.get("phone") if isinstance(contacts, dict) else None
    if phone:
        details.append(f"Телефон: {_esc(phone)}")

    schedule = obj.get("schedule")
    hours = schedule.get("regular") if isinstance(schedule, dict) else None
    if hours:
        details.append(f"Часы работы: {_esc(hours)}")

    if details:
        parts.append("\n".join(details))

    result: dict = {
        "html": "\n\n".join(parts),
        "has_location": has_location,
    }
    if coords is not None:
        result["lat"], result["lng"] = coords

    return result
