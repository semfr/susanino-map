"""
Обработчик выбора категории (callback cat:{id}).
"""
from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.inline import categories_keyboard, objects_keyboard
from services.data_loader import get_categories, get_objects_by_category
from handlers.ui import replace_message

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
        # replace_message: карточка объекта могла быть photo/rich — edit_text бы упал.
        await replace_message(
            callback.message,
            f"{cat.get('emoji', '')} <b>{cat['name']}</b>\n\nОбъектов пока нет.",
            reply_markup=categories_keyboard(),
        )
        return

    emoji = cat.get("emoji", "")
    text = f"{emoji} <b>{cat['name']}</b>\n\nОбъектов: {len(objects)}"

    await callback.answer()
    # replace_message: «Назад к списку» приходит с карточки объекта (photo/rich),
    # у которой нет текста — поэтому не edit_text, а безопасная замена сообщения.
    await replace_message(
        callback.message,
        text,
        reply_markup=objects_keyboard(objects),
    )


@router.callback_query(lambda c: c.data == "back:categories")
async def back_to_categories(callback: CallbackQuery) -> None:
    await callback.answer()
    await replace_message(
        callback.message,
        "Выберите категорию:",
        reply_markup=categories_keyboard(),
    )
