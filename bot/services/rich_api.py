"""
Отправка rich-карточки (Telegram Bot API 10.1, метод sendRichMessage) поверх aiogram.

aiogram 3.x не имеет нативного метода sendRichMessage — шлём сырой HTTP-запрос
через aiohttp (зависимость aiogram). Любая ошибка → возвращаем False, чтобы
вызывающий код мог откатиться на обычное сообщение.
"""
import logging
from typing import Any

import aiohttp
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

logger = logging.getLogger(__name__)

_TIMEOUT = aiohttp.ClientTimeout(total=30)


async def send_rich_message(
    bot: Bot,
    chat_id: int,
    html: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> bool:
    """
    Отправляет rich-сообщение через sendRichMessage.

    :return: True при ok=True от Telegram, иначе False (нужен fallback у вызывающего).
    """
    url = f"https://api.telegram.org/bot{bot.token}/sendRichMessage"
    payload: dict[str, Any] = {"chat_id": chat_id, "rich_message": {"html": html}}
    if reply_markup is not None:
        # aiogram-разметка -> API-словарь (pydantic v2)
        payload["reply_markup"] = reply_markup.model_dump(by_alias=True, exclude_none=True)

    try:
        async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
            async with session.post(url, json=payload) as resp:
                data = await resp.json()
        if data.get("ok"):
            return True
        logger.warning("sendRichMessage не ок: %s", data.get("description"))
        return False
    except Exception as exc:  # сеть/таймаут/парсинг — деградируем
        logger.warning("sendRichMessage ошибка: %s", exc)
        return False
