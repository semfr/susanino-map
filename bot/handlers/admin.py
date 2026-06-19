"""
FSM-админка через бота (часть B спеки).

Поток:
    /admin -> гард админа -> список объектов
          -> карточка объекта с текущими значениями полей и кнопками полей
          -> выбор поля -> бот просит новое значение
          -> превью «было -> стало» -> [Опубликовать]/[Отмена]
          -> публикация в GitHub -> обновление локальных данных.

Все обращения к config — лениво ВНУТРИ хэндлеров (config.py читает
os.environ при импорте). EDITABLE_FIELDS берём из services.object_editor.
"""
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from services.data_loader import get_object_by_id, get_objects, update_objects
from services.object_editor import (
    EDITABLE_FIELDS,
    apply_edit,
    get_field_value,
)

logger = logging.getLogger(__name__)

router = Router()

# Максимальная длина значения в превью (чтобы не упереться в лимит сообщения).
_PREVIEW_MAX = 400


class AdminEdit(StatesGroup):
    """Состояния диалога редактирования."""

    waiting_value = State()      # ждём новое значение поля
    waiting_confirm = State()    # ждём подтверждения публикации


# --- Вспомогательные функции построения клавиатур/текста ---


def _is_admin(user_id: int | None, admin_ids: set[int]) -> bool:
    """Проверка прав администратора."""
    return user_id is not None and user_id in admin_ids


def _field_label(field_key: str) -> str:
    """Человекочитаемая подпись поля (label из FieldSpec, иначе ключ)."""
    spec = EDITABLE_FIELDS.get(field_key)
    label = None
    if spec is not None:
        # FieldSpec может быть dataclass/объектом или dict — пробуем оба.
        label = getattr(spec, "label", None)
        if label is None and isinstance(spec, dict):
            label = spec.get("label")
    return label or field_key


def _objects_keyboard() -> InlineKeyboardMarkup:
    """Инлайн-список объектов (callback adm:obj:<id>)."""
    rows: list[list[InlineKeyboardButton]] = []
    for obj in get_objects():
        title = obj.get("name") or obj.get("shortName") or obj.get("id", "")
        rows.append(
            [
                InlineKeyboardButton(
                    text=title,
                    callback_data=f"adm:obj:{obj['id']}",
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _truncate(value: str) -> str:
    """Обрезает длинное значение для показа в сообщении."""
    if len(value) > _PREVIEW_MAX:
        return value[:_PREVIEW_MAX] + "…"
    return value


def _object_card(obj: dict) -> tuple[str, InlineKeyboardMarkup]:
    """
    Карточка объекта: текущие значения редактируемых полей + кнопки полей.
    Кнопка поля -> callback adm:fld:<id>:<field_key>.
    """
    obj_id = obj["id"]
    title = obj.get("name") or obj.get("id", "")

    lines = [f"<b>{title}</b>", "", "Текущие значения полей:"]
    rows: list[list[InlineKeyboardButton]] = []

    for field_key in EDITABLE_FIELDS:
        label = _field_label(field_key)
        try:
            current = get_field_value(obj, field_key)
        except Exception:  # noqa: BLE001 — поле могло быть пустым/отсутствовать
            current = ""
        shown = _truncate(current) if current else "—"
        lines.append(f"\n<b>{label}:</b> {shown}")
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"✏️ {label}",
                    callback_data=f"adm:fld:{obj_id}:{field_key}",
                )
            ]
        )

    rows.append(
        [InlineKeyboardButton(text="⬅️ К списку", callback_data="adm:list")]
    )
    text = "\n".join(lines)
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def _confirm_keyboard() -> InlineKeyboardMarkup:
    """Кнопки подтверждения публикации."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Опубликовать", callback_data="adm:confirm"
                ),
                InlineKeyboardButton(
                    text="✖️ Отмена", callback_data="adm:cancel"
                ),
            ]
        ]
    )


# --- Хэндлеры ---


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext) -> None:
    """Точка входа в админку. Не-админу — молча ничего."""
    from config import ADMIN_IDS  # лениво: config читает env при импорте

    if not _is_admin(message.from_user.id if message.from_user else None, ADMIN_IDS):
        return  # молчим для не-админов

    await state.clear()
    await message.answer(
        "🛠 <b>Админка</b>\n\nВыберите объект для редактирования:",
        parse_mode="HTML",
        reply_markup=_objects_keyboard(),
    )


@router.callback_query(F.data == "adm:list")
async def adm_list(callback: CallbackQuery, state: FSMContext) -> None:
    """Вернуться к списку объектов."""
    from config import ADMIN_IDS

    if not _is_admin(callback.from_user.id, ADMIN_IDS):
        await callback.answer()
        return

    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        "🛠 <b>Админка</b>\n\nВыберите объект для редактирования:",
        parse_mode="HTML",
        reply_markup=_objects_keyboard(),
    )


@router.callback_query(F.data.startswith("adm:obj:"))
async def adm_object(callback: CallbackQuery, state: FSMContext) -> None:
    """Карточка объекта с полями."""
    from config import ADMIN_IDS

    if not _is_admin(callback.from_user.id, ADMIN_IDS):
        await callback.answer()
        return

    obj_id = callback.data.split(":", 2)[2]
    obj = get_object_by_id(obj_id)
    if obj is None:
        await callback.answer("Объект не найден.", show_alert=True)
        return

    await state.clear()
    await callback.answer()
    text, keyboard = _object_card(obj)
    await callback.message.edit_text(
        text, parse_mode="HTML", reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("adm:fld:"))
async def adm_field(callback: CallbackQuery, state: FSMContext) -> None:
    """Выбор поля: показать текущее значение и попросить новое."""
    from config import ADMIN_IDS

    if not _is_admin(callback.from_user.id, ADMIN_IDS):
        await callback.answer()
        return

    # adm:fld:<id>:<field_key> — id может содержать дефисы, field_key — нет.
    _, _, obj_id, field_key = callback.data.split(":", 3)

    if field_key not in EDITABLE_FIELDS:
        await callback.answer("Поле недоступно для редактирования.", show_alert=True)
        return

    obj = get_object_by_id(obj_id)
    if obj is None:
        await callback.answer("Объект не найден.", show_alert=True)
        return

    try:
        current = get_field_value(obj, field_key)
    except Exception:  # noqa: BLE001
        current = ""

    # Сохраняем контекст редактирования в FSM.
    await state.update_data(obj_id=obj_id, field_key=field_key)
    await state.set_state(AdminEdit.waiting_value)

    await callback.answer()
    label = _field_label(field_key)
    shown = _truncate(current) if current else "—"
    await callback.message.edit_text(
        f"Поле <b>{label}</b>\n\n"
        f"Текущее значение:\n{shown}\n\n"
        f"Отправьте новое значение сообщением.",
        parse_mode="HTML",
    )


@router.message(AdminEdit.waiting_value)
async def adm_receive_value(message: Message, state: FSMContext) -> None:
    """Получили новое значение -> превью «было -> стало»."""
    from config import ADMIN_IDS

    if not _is_admin(message.from_user.id if message.from_user else None, ADMIN_IDS):
        return

    data = await state.get_data()
    obj_id = data.get("obj_id")
    field_key = data.get("field_key")

    obj = get_object_by_id(obj_id) if obj_id else None
    if obj is None or not field_key:
        await state.clear()
        await message.answer("Сессия редактирования потеряна. Наберите /admin заново.")
        return

    raw_value = message.text or ""

    try:
        new_obj, old_display, new_display = apply_edit(obj, field_key, raw_value)
    except ValueError as exc:
        # Нарушение whitelist/типа/длины — сообщаем причину, остаёмся в вводе.
        await message.answer(
            f"❌ Не удалось применить: {exc}\n\nОтправьте корректное значение."
        )
        return

    # Сохраняем подготовленный объект в FSM для публикации.
    await state.update_data(new_obj=new_obj)
    await state.set_state(AdminEdit.waiting_confirm)

    label = _field_label(field_key)
    await message.answer(
        f"Поле <b>{label}</b>\n\n"
        f"Было:\n{_truncate(old_display) or '—'}\n\n"
        f"Стало:\n{_truncate(new_display) or '—'}\n\n"
        f"Опубликовать изменение?",
        parse_mode="HTML",
        reply_markup=_confirm_keyboard(),
    )


@router.callback_query(AdminEdit.waiting_confirm, F.data == "adm:confirm")
async def adm_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    """Публикация: сперва GitHub-коммит, при успехе — локальное обновление."""
    from config import ADMIN_IDS, SITE_BASE_URL  # noqa: F401 (ленивая загрузка)
    from services import github_publish

    if not _is_admin(callback.from_user.id, ADMIN_IDS):
        await callback.answer()
        return

    data = await state.get_data()
    new_obj = data.get("new_obj")
    obj_id = data.get("obj_id")
    if not new_obj or not obj_id:
        await state.clear()
        await callback.answer()
        await callback.message.edit_text(
            "Сессия редактирования потеряна. Наберите /admin заново."
        )
        return

    await callback.answer("Публикую…")

    # Полный список объектов с заменённым редактируемым объектом.
    objects = [
        new_obj if obj.get("id") == obj_id else obj
        for obj in get_objects()
    ]

    try:
        commit_url = await github_publish.publish_objects(objects)
    except Exception as exc:  # noqa: BLE001 — любая сетевая/API-ошибка
        logger.exception("Публикация в GitHub не удалась")
        await callback.message.edit_text(
            f"❌ Не удалось опубликовать: {exc}\n\n"
            f"Локальные данные не изменены. Попробуйте позже."
        )
        # Состояние оставляем, чтобы можно было повторить подтверждение.
        return

    # Коммит прошёл — обновляем локальные данные (in-memory + файл).
    update_objects(objects)
    await state.clear()

    await callback.message.edit_text(
        "✅ Опубликовано. Сайт обновится за ~1–2 мин.\n\n"
        f"Коммит: {commit_url}",
        disable_web_page_preview=True,
    )


@router.callback_query(F.data == "adm:cancel")
async def adm_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """Отмена: сбросить состояние."""
    from config import ADMIN_IDS

    if not _is_admin(callback.from_user.id, ADMIN_IDS):
        await callback.answer()
        return

    await state.clear()
    await callback.answer("Отменено")
    await callback.message.edit_text(
        "Отменено. Наберите /admin, чтобы начать заново."
    )
