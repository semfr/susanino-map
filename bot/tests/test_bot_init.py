"""
Smoke-тест: конструирование Bot тем же способом, что и в bot.py.
Ловит несовместимости aiogram API (напр., убранный из инициализатора parse_mode
в aiogram 3.7 — теперь только через default=DefaultBotProperties(...)).
Сети не требует — Bot() при создании запросов не делает.
"""
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


def test_bot_constructs_with_default_parse_mode():
    bot = Bot(
        token="123456789:AAEhdummytokendummytokendummytoken00",
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    assert bot is not None
    assert bot.token.startswith("123456789:")
