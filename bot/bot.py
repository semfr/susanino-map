"""
Точка входа Telegram-бота карты Сусанинского района.

Запуск:
    python bot.py

Требуется переменная окружения BOT_TOKEN (или файл .env в директории бота).
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers import start, categories, objects, nearby

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Подключаем роутеры (порядок важен: сначала более специфичные)
    dp.include_router(start.router)
    dp.include_router(nearby.router)
    dp.include_router(categories.router)
    dp.include_router(objects.router)

    logger.info("Запуск бота...")
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    asyncio.run(main())
