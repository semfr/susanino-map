"""
Тесты UI-хелпера replace_message (handlers/ui.py).

replace_message заменяет текущее сообщение новым контентом:
  - текстовое сообщение -> edit_text на месте;
  - если редактирование невозможно (photo/rich — нет текста, Telegram бросает
    TelegramBadRequest "there is no text in the message to edit") -> answer новым
    сообщением + delete старого.

Async-хелпер гоняем через asyncio.run (pytest-asyncio в проекте нет).
"""
import asyncio
from unittest.mock import AsyncMock, Mock

from aiogram.exceptions import TelegramBadRequest

from handlers.ui import replace_message


def _no_text_error() -> TelegramBadRequest:
    """Воспроизводит ошибку Telegram при edit_text на сообщении без текста."""
    return TelegramBadRequest(
        method=Mock(),
        message="Bad Request: there is no text in the message to edit",
    )


def test_edits_in_place_for_text_message():
    """Текстовое сообщение редактируется на месте; новое не шлётся, старое не удаляется."""
    msg = AsyncMock()
    asyncio.run(replace_message(msg, "Список", reply_markup="kb"))

    msg.edit_text.assert_awaited_once()
    msg.answer.assert_not_awaited()
    msg.delete.assert_not_awaited()


def test_falls_back_to_resend_when_no_text():
    """Если edit_text невозможен (photo/rich) — шлём новое сообщение и удаляем старое."""
    msg = AsyncMock()
    msg.edit_text.side_effect = _no_text_error()

    asyncio.run(replace_message(msg, "Список", reply_markup="kb"))

    msg.answer.assert_awaited_once()
    msg.delete.assert_awaited_once()


def test_resend_survives_delete_failure():
    """Если удалить старое сообщение нельзя — новое всё равно отправлено, ошибка не всплывает."""
    msg = AsyncMock()
    msg.edit_text.side_effect = _no_text_error()
    msg.delete.side_effect = _no_text_error()

    # Не должно бросить наружу.
    asyncio.run(replace_message(msg, "Список"))

    msg.answer.assert_awaited_once()
