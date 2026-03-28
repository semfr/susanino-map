"""
Обработчик кнопки «Что рядом».
Принимает геолокацию пользователя и возвращает ближайшие объекты.
"""
from aiogram import Router, F
from aiogram.types import Message

from keyboards.inline import object_actions_keyboard
from services.geo import find_nearest

router = Router()

NEAREST_COUNT = 5


def _format_distance(km: float) -> str:
    """Форматирует расстояние: метры или километры."""
    if km < 1.0:
        return f"{int(km * 1000)} м"
    return f"{km:.1f} км"


@router.message(F.location)
async def handle_location(message: Message) -> None:
    lat = message.location.latitude
    lng = message.location.longitude

    nearest = find_nearest(lat, lng, n=NEAREST_COUNT)

    if not nearest:
        await message.answer("Объекты не найдены.")
        return

    await message.answer(
        f"📍 Ближайшие {len(nearest)} объектов рядом с вами:",
    )

    for obj, dist in nearest:
        name = obj.get("name", "Объект")
        description = obj.get("description", "")
        dist_str = _format_distance(dist)

        text_parts = [f"<b>{name}</b>", f"📏 {dist_str}"]
        if description:
            text_parts.append(description)

        text = "\n".join(text_parts)
        keyboard = object_actions_keyboard(obj)

        await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
