"""
Разбор start-payload Telegram для deep-link «сайт → бот».

Формат ссылки: https://t.me/susanino_map_bot?start=obj_<id>
Telegram передаёт всё после `start=` как аргумент команды /start.
Здесь только чистый разбор payload — без сети, aiogram и config.
"""
import re

# Префикс deep-link и whitelist символов id (как у slug объектов: латиница в нижнем
# регистре, цифры, дефис). Допускаем дефисы внутри, но требуем непустой id.
_PAYLOAD_RE = re.compile(r"^obj_([a-z0-9-]+)$")


def parse_start_payload(raw: str | None) -> str | None:
    """
    Извлекает id объекта из start-payload.

    Args:
        raw: Сырой аргумент команды /start (может быть None или пустым).

    Returns:
        id объекта, если raw имеет вид `obj_<id>` (id = [a-z0-9-]+);
        иначе None (пустое значение, мусор, неверный префикс, недопустимые символы).
    """
    if not raw:
        return None
    match = _PAYLOAD_RE.match(raw)
    if match is None:
        return None
    return match.group(1)
