"""
Чистая логика правок объектов карты (B3, спек 2026-06-19).

Модуль НЕ импортирует config и не делает сети — только валидация и
трансформация словарей. Используется админкой бота (handlers/admin.py)
и публикацией (services/github_publish.py).

Контракт:
  - EDITABLE_FIELDS: dict[str, FieldSpec] — whitelist редактируемых полей.
  - get_field_value(obj, field_key) -> str — текущее значение для превью.
  - apply_edit(obj, field_key, raw_value) -> (new_obj, old_display, new_display)
      глубокая копия объекта, валидация типа/whitelist (ValueError при нарушении),
      бамп meta.updatedAt = сегодня (datetime.date.today().isoformat()).

Whitelist (только текстовые/оперативные поля; фото/координаты/slug/категория — вне MVP):
  name, shortName, description, fullDescription, address,
  contacts.phone, contacts.website, schedule.regular, schedule.days,
  pricing.adult (int), pricing.notes, tags (список из строки через запятую).
"""
import copy
import datetime

# --- Whitelist редактируемых полей ---
#
# FieldSpec:
#   label    — человекочитаемое имя поля (для кнопок/превью в боте)
#   path     — путь к значению как кортеж ключей в объекте
#   type     — "str" | "int" | "tags"
#   required — нельзя сохранять пустым (после strip)
EDITABLE_FIELDS: dict[str, dict] = {
    "name": {
        "label": "Название",
        "path": ("name",),
        "type": "str",
        "required": True,
    },
    "shortName": {
        "label": "Короткое название",
        "path": ("shortName",),
        "type": "str",
        "required": False,
    },
    "description": {
        "label": "Краткое описание",
        "path": ("description",),
        "type": "str",
        "required": False,
    },
    "fullDescription": {
        "label": "Полное описание",
        "path": ("fullDescription",),
        "type": "str",
        "required": False,
    },
    "address": {
        "label": "Адрес",
        "path": ("address",),
        "type": "str",
        "required": False,
    },
    "contacts.phone": {
        "label": "Телефон",
        "path": ("contacts", "phone"),
        "type": "str",
        "required": False,
    },
    "contacts.website": {
        "label": "Сайт",
        "path": ("contacts", "website"),
        "type": "str",
        "required": False,
    },
    "schedule.regular": {
        "label": "Часы работы",
        "path": ("schedule", "regular"),
        "type": "str",
        "required": False,
    },
    "schedule.days": {
        "label": "Дни / выходные",
        "path": ("schedule", "days"),
        "type": "str",
        "required": False,
    },
    "pricing.adult": {
        "label": "Цена (взрослый), ₽",
        "path": ("pricing", "adult"),
        "type": "int",
        "required": False,
    },
    "pricing.notes": {
        "label": "Примечание к цене",
        "path": ("pricing", "notes"),
        "type": "str",
        "required": False,
    },
    "tags": {
        "label": "Теги (через запятую)",
        "path": ("tags",),
        "type": "tags",
        "required": False,
    },
}


def _get_spec(field_key: str) -> dict:
    """Возвращает спецификацию поля или ValueError, если поле вне whitelist."""
    spec = EDITABLE_FIELDS.get(field_key)
    if spec is None:
        raise ValueError(f"Поле '{field_key}' не разрешено к редактированию")
    return spec


def _read_raw(obj: dict, path: tuple) -> object:
    """Читает сырое значение по пути; None, если что-то отсутствует."""
    cur: object = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def _display(value: object, field_type: str) -> str:
    """Приводит значение к человекочитаемой строке для превью."""
    if value is None:
        return ""
    if field_type == "tags":
        if isinstance(value, (list, tuple)):
            return ", ".join(str(t) for t in value)
        return str(value)
    if field_type == "int":
        return "" if value == "" else str(value)
    return str(value)


def get_field_value(obj: dict, field_key: str) -> str:
    """
    Возвращает текущее значение поля как строку для превью.
    Для tags — элементы через запятую. Для отсутствующего — пустая строка.
    ValueError, если поле вне whitelist.
    """
    spec = _get_spec(field_key)
    raw = _read_raw(obj, spec["path"])
    return _display(raw, spec["type"])


def _parse_value(raw_value: str, field_type: str) -> object:
    """
    Преобразует и валидирует сырой ввод по типу поля.
    Возвращает (value_for_storage). ValueError при нарушении типа.
    """
    if field_type == "int":
        text = (raw_value or "").strip()
        try:
            return int(text)
        except (TypeError, ValueError):
            raise ValueError(f"Ожидается целое число, получено: '{raw_value}'")
    if field_type == "tags":
        parts = [p.strip() for p in (raw_value or "").split(",")]
        return [p for p in parts if p]
    # str
    return raw_value if raw_value is not None else ""


def _set_raw(obj: dict, path: tuple, value: object) -> None:
    """Записывает значение по пути, создавая недостающие вложенные словари."""
    cur = obj
    for key in path[:-1]:
        nxt = cur.get(key)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[key] = nxt
        cur = nxt
    cur[path[-1]] = value


def apply_edit(obj: dict, field_key: str, raw_value: str):
    """
    Применяет правку поля к глубокой копии объекта.

    Возвращает (new_obj, old_display, new_display).
    Raise ValueError при: поле вне whitelist; нарушение типа (pricing.adult);
    пустое значение в required-поле.
    Бампит meta.updatedAt = сегодня (ISO-дата).
    Исходный obj не изменяется.
    """
    spec = _get_spec(field_key)
    field_type = spec["type"]

    # Превью «было» — по исходному объекту
    old_display = get_field_value(obj, field_key)

    # Валидация required (по строковому представлению после strip)
    if spec.get("required") and not (raw_value or "").strip():
        raise ValueError(f"Поле '{spec['label']}' обязательно и не может быть пустым")

    # Преобразование/валидация типа (может бросить ValueError)
    value = _parse_value(raw_value, field_type)

    # Глубокая копия, чтобы не мутировать исходник
    new_obj = copy.deepcopy(obj)
    _set_raw(new_obj, spec["path"], value)

    # Бамп даты обновления (создаём meta при отсутствии)
    meta = new_obj.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        new_obj["meta"] = meta
    meta["updatedAt"] = datetime.date.today().isoformat()

    new_display = _display(value, field_type)
    return new_obj, old_display, new_display
