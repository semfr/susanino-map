"""
UI-хелперы для хэндлеров бота.

replace_message — безопасная «замена» текущего сообщения новым контентом.
Нужна для навигации (кнопки «Назад к списку» и т.п.): карточка объекта может
быть отправлена как photo/rich-сообщение, у которого НЕТ текста — тогда
edit_text падает с TelegramBadRequest "there is no text in the message to edit".
В этом случае шлём новое сообщение и удаляем старое (паттерн как в objects.send_object_card).
"""
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message


async def replace_message(
    message: Message,
    text: str,
    reply_markup=None,
    parse_mode: str = "HTML",
) -> None:
    """
    Заменяет сообщение `message` новым текстом + клавиатурой.

    1. Пытается отредактировать на месте (edit_text) — для текстовых сообщений.
    2. Если редактирование невозможно (photo/rich — нет текста), отправляет новое
       сообщение и удаляет старое. Невозможность удалить старое не считается ошибкой.
    """
    try:
        await message.edit_text(
            text, parse_mode=parse_mode, reply_markup=reply_markup
        )
        return
    except TelegramBadRequest:
        # У сообщения нет редактируемого текста (фото/медиа/rich) — пересоздаём.
        pass

    await message.answer(text, parse_mode=parse_mode, reply_markup=reply_markup)
    try:
        await message.delete()
    except TelegramBadRequest:
        # Старое сообщение могло устареть/быть неудаляемым — не критично.
        pass
