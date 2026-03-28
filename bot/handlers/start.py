"""
Обработчик команды /start.
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from keyboards.inline import categories_keyboard

router = Router()

WELCOME_TEXT = (
    "👋 Добро пожаловать в бот <b>Карты Сусанинского района</b>!\n\n"
    "Здесь вы найдёте:\n"
    "🏛 Музеи и исторические места\n"
    "⛪ Храмы\n"
    "🌿 Природные объекты\n"
    "🍽 Кафе и рестораны\n"
    "🏠 Места для ночлега\n"
    "🎨 Народные ремёсла\n\n"
    "Выберите категорию или отправьте своё местоположение, "
    "чтобы найти ближайшие объекты."
)


def _main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Reply-клавиатура с кнопкой геолокации."""
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Что рядом", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    return kb


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=_main_reply_keyboard(),
    )
    await message.answer(
        "Выберите категорию:",
        reply_markup=categories_keyboard(),
    )
