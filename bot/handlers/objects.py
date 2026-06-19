"""
Обработчик просмотра объекта (callback obj:{id}).
Отправляет фото (если файл существует) или текст + кнопки действий.
"""
from pathlib import Path

from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from keyboards.inline import object_actions_keyboard
from services.data_loader import get_object_by_id
from services.rich_message_builder import build_object_rich_message
from services.rich_api import send_rich_message

router = Router()

# Директория веб-части проекта (где хранятся изображения)
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_WEB_PUBLIC = _PROJECT_ROOT / "web" / "public"


def _build_object_text(obj: dict) -> str:
    """Формирует текст карточки объекта."""
    lines: list[str] = []

    name = obj.get("name", "")
    lines.append(f"<b>{name}</b>")

    description = obj.get("fullDescription") or obj.get("description", "")
    if description:
        lines.append("")
        lines.append(description)

    address = obj.get("address", "")
    if address:
        lines.append("")
        lines.append(f"📍 {address}")

    schedule = obj.get("schedule", {})
    regular = schedule.get("regular", "")
    days = schedule.get("days", "")
    if regular:
        lines.append(f"🕐 {regular}")
    if days:
        lines.append(f"   {days}")

    pricing = obj.get("pricing", {})
    adult_price = pricing.get("adult", 0)
    notes = pricing.get("notes", "")
    if adult_price:
        lines.append(f"💰 Взрослый: {adult_price} ₽")
    elif notes:
        lines.append(f"💰 {notes}")

    contacts = obj.get("contacts", {})
    phone = contacts.get("phone", "")
    website = contacts.get("website", "")
    if phone:
        lines.append(f"📞 {phone}")
    if website:
        lines.append(f"🔗 {website}")

    return "\n".join(lines)


def _find_local_photo(obj: dict) -> Path | None:
    """
    Ищет главное фото объекта среди локальных файлов.
    Возвращает Path, если файл существует, иначе None.
    """
    photos: list[dict] = obj.get("photos", [])
    # Ищем главное фото
    main_photo = next((p for p in photos if p.get("isMain")), None)
    if main_photo is None and photos:
        main_photo = photos[0]
    if main_photo is None:
        return None

    src: str = main_photo.get("src", "")
    if not src:
        return None

    # src вида /images/objects/{id}/main.webp
    # Пробуем найти файл относительно web/public
    relative = src.lstrip("/")
    local_path = _WEB_PUBLIC / relative
    if local_path.exists():
        return local_path
    return None


@router.callback_query(lambda c: c.data and c.data.startswith("obj:"))
async def object_selected(callback: CallbackQuery) -> None:
    obj_id = callback.data.split(":", 1)[1]
    obj = get_object_by_id(obj_id)

    if obj is None:
        await callback.answer("Объект не найден.", show_alert=True)
        return

    await callback.answer()

    text = _build_object_text(obj)
    keyboard = object_actions_keyboard(obj)
    photo_path = _find_local_photo(obj)

    if photo_path is not None:
        # Отправляем сообщение с фото
        await callback.message.answer_photo(
            photo=FSInputFile(str(photo_path)),
            caption=text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        # Скрываем предыдущее сообщение (убираем кнопки)
        try:
            await callback.message.delete()
        except Exception:
            pass
    else:
        # Фото нет — пробуем rich-карточку (Bot API 10.1) со встроенной картой,
        # при любой ошибке откатываемся на обычное текстовое сообщение.
        rich = build_object_rich_message(obj)
        sent = await send_rich_message(
            callback.bot,
            callback.message.chat.id,
            rich["html"],
            keyboard,
        )
        if sent:
            # rich пришёл новым сообщением — убираем кнопки у предыдущего
            try:
                await callback.message.delete()
            except Exception:
                pass
        else:
            await callback.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
