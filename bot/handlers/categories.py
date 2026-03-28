"""
Обработчик выбора категории (callback cat:{id}).
"""
from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.inline import categories_keyboard, objects_keyboard
from services.data_loader import get_categories, get_objects_by_category

router = Router()


def _get_category_by_id(category_id: str) -> dict | None:
    for cat in get_categories():
        if cat["id"] == category_id:
            return cat
    return None


@router.callback_query(lambda c: c.data and c.data.startswith("cat:"))
async def category_selected(callback: CallbackQuery) -> None:
    category_id = callback.data.split(":", 1)[1]
    cat = _get_category_by_id(category_id)

    if cat is None:
        await callback.answer("Категория не найдена.", show_alert=True)
        return

    objects = get_objects_by_category(category_id)

    if not objects:
        await callback.answer()
        await callback.message.edit_text(
            f"{cat.get('emoji', '')} <b>{cat['name']}</b>\n\nОбъектов пока нет.",
            parse_mode="HTML",
            reply_markup=categories_keyboard(),
        )
        return

    emoji = cat.get("emoji", "")
    text = f"{emoji} <b>{cat['name']}</b>\n\nОбъектов: {len(objects)}"

    await callback.answer()
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=objects_keyboard(objects),
    )


@router.callback_query(lambda c: c.data == "back:categories")
async def back_to_categories(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=categories_keyboard(),
    )
