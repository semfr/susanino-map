"""
Inline-режим бота (A4): @susanino_map_bot <запрос> в любом чате.

Объекты отдаются как InlineQueryResultArticle:
  title = name, description = shortName / начало description,
  message text = краткий текст карточки + ссылка на страницу объекта на сайте.

build_inline_results — ЧИСТАЯ функция: без импорта config и без сети.
Хэндлер inline_query лениво берёт config и data_loader внутри.
"""
from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

router = Router()

# Максимум результатов в инлайн-ответе (Telegram допускает до 50; держим компактно).
MAX_RESULTS = 20
# Сколько секунд Telegram кэширует инлайн-ответ.
INLINE_CACHE_TIME = 300
# До скольких символов обрезаем описание-фолбэк.
_DESCRIPTION_LIMIT = 120


def _object_matches(obj: dict, query_lc: str) -> bool:
    """
    Проверяет, подходит ли объект под запрос (регистронезависимо).
    Ищем подстроку в name, shortName и тегах.
    """
    haystack: list[str] = []

    name = obj.get("name")
    if name:
        haystack.append(str(name))

    short_name = obj.get("shortName")
    if short_name:
        haystack.append(str(short_name))

    for tag in obj.get("tags", []) or []:
        haystack.append(str(tag))

    blob = " ".join(haystack).lower()
    return query_lc in blob


def _result_description(obj: dict) -> str:
    """Описание для строки результата: shortName или начало description."""
    short_name = obj.get("shortName")
    if short_name:
        return str(short_name)

    description = obj.get("description") or ""
    description = str(description).strip()
    if len(description) > _DESCRIPTION_LIMIT:
        description = description[:_DESCRIPTION_LIMIT].rstrip() + "…"
    return description


def _message_text(obj: dict, site_base_url: str) -> str:
    """
    Краткий текст карточки для вставляемого сообщения + ссылка на сайт.
    Без HTML-разметки, чтобы не зависеть от parse_mode инлайн-результата.
    """
    lines: list[str] = []

    name = obj.get("name", "")
    if name:
        lines.append(str(name))

    # Короткое пояснение: shortName, иначе description.
    short_name = obj.get("shortName")
    description = obj.get("description")
    subtitle = short_name or description
    if subtitle and str(subtitle) != str(name):
        lines.append(str(subtitle))

    address = obj.get("address")
    if address:
        lines.append(f"📍 {address}")

    slug = obj.get("slug") or obj.get("id", "")
    site_base_url = (site_base_url or "").rstrip("/")
    lines.append("")
    lines.append(f"🌐 {site_base_url}/object/{slug}")

    return "\n".join(lines)


def build_inline_results(
    objects: list[dict],
    query: str | None,
    site_base_url: str,
    bot_username: str,
) -> list[InlineQueryResultArticle]:
    """
    Чистая фабрика инлайн-результатов.

    Фильтрует объекты по query (по name/shortName/tags, регистронезависимо).
    Пустой/None query -> все объекты. Не более MAX_RESULTS результатов.

    bot_username принимается для совместимости контракта (может быть полезен
    в будущем для switch_pm/deep-link), на сами результаты сейчас не влияет.
    """
    query_lc = (query or "").strip().lower()

    if query_lc:
        matched = [obj for obj in objects if _object_matches(obj, query_lc)]
    else:
        matched = list(objects)

    matched = matched[:MAX_RESULTS]

    results: list[InlineQueryResultArticle] = []
    for obj in matched:
        obj_id = str(obj.get("id", ""))
        title = str(obj.get("name", "")) or obj_id
        description = _result_description(obj)
        message_text = _message_text(obj, site_base_url)

        results.append(
            InlineQueryResultArticle(
                id=obj_id,
                title=title,
                description=description or None,
                input_message_content=InputTextMessageContent(
                    message_text=message_text,
                ),
            )
        )

    return results


@router.inline_query()
async def inline_query(query: InlineQuery) -> None:
    """
    Хэндлер инлайн-запроса: отдаёт объекты как статьи.
    config и data_loader импортируются лениво, чтобы чистая логика
    (build_inline_results) оставалась независимой от окружения.
    """
    import config
    from services.data_loader import get_objects

    results = build_inline_results(
        get_objects(),
        query.query,
        config.SITE_BASE_URL,
        config.BOT_USERNAME,
    )
    await query.answer(results, cache_time=INLINE_CACHE_TIME, is_personal=False)
