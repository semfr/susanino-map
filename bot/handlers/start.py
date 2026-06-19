"""
Обработчик команды /start.

Поддерживает deep-link «сайт → бот»: https://t.me/susanino_map_bot?start=obj_<id>.
Если аргумент команды разбирается в id существующего объекта — сразу показываем
его карточку (переиспользуя рендер из handlers.objects). Иначе обычный welcome.
"""
from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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


def _site_inline_keyboard(site_base_url: str) -> InlineKeyboardMarkup:
    """Инлайн-кнопка «Открыть карту-лубок на сайте»."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗺 Открыть карту-лубок на сайте",
                    url=site_base_url,
                )
            ]
        ]
    )


async def _send_welcome(message: Message) -> None:
    """Обычный welcome: приветствие + кнопка сайта + категории."""
    import config  # лениво: config читает os.environ при импорте

    await message.answer(
        WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=_main_reply_keyboard(),
    )
    await message.answer(
        "Выберите категорию:",
        reply_markup=categories_keyboard(),
    )
    await message.answer(
        "Или откройте интерактивную карту-лубок на сайте:",
        reply_markup=_site_inline_keyboard(config.SITE_BASE_URL),
    )


@router.message(CommandStart(deep_link=True))
async def cmd_start_deeplink(message: Message, command: CommandObject) -> None:
    """
    /start с deep-link payload. Если payload вида obj_<id> и объект найден —
    показываем его карточку. Иначе откатываемся на обычный welcome.
    """
    from services.data_loader import get_object_by_id
    from services.deeplink import parse_start_payload
    from handlers.objects import send_object_card

    obj_id = parse_start_payload(command.args)
    obj = get_object_by_id(obj_id) if obj_id else None

    if obj is not None:
        await send_object_card(message, obj)
        return

    await _send_welcome(message)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обычный /start без deep-link."""
    await _send_welcome(message)
