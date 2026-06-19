"""
Тесты чистой логики правок объектов (B3, спек 2026-06-19).

Контракт (services/object_editor.py):
  - EDITABLE_FIELDS: dict[str, FieldSpec] — whitelist (label, путь, тип, required).
  - get_field_value(obj, field_key) -> str — текущее значение для превью.
  - apply_edit(obj, field_key, raw_value) -> (new_obj, old_display, new_display)
      валидация типа/whitelist (raise ValueError), bump meta.updatedAt = сегодня.

Модуль НЕ импортирует config и не делает сети — чистые функции.
"""
import copy
import datetime

import pytest

from services.object_editor import (
    EDITABLE_FIELDS,
    apply_edit,
    get_field_value,
)


# --- Фикстура: репрезентативный объект (структура из data/objects.json) ---

def _museum() -> dict:
    return {
        "id": "susanino-museum",
        "name": "Сусанинский краеведческий музей",
        "shortName": "Краеведческий музей",
        "description": "Музей о подвиге Сусанина.",
        "fullDescription": "Длинное описание музея.",
        "address": "пос. Сусанино, ул. Крупской, д. 31",
        "contacts": {
            "phone": "+7 (49434) 9-05-20",
            "website": "https://kosmuseum.ru/",
            "email": "",
        },
        "schedule": {
            "regular": "Вт–Вс 09:00–17:30",
            "days": "Закрыт по понедельникам",
            "exceptions": "",
        },
        "pricing": {
            "adult": 200,
            "child": 100,
            "currency": "RUB",
            "notes": "Доступен по Пушкинской карте",
        },
        "tags": ["сусанин", "история", "музей"],
        "meta": {"createdAt": "2026-03-28", "updatedAt": "2026-03-28"},
    }


# --- Whitelist EDITABLE_FIELDS ---

def test_whitelist_contains_all_contract_fields():
    expected = {
        "name", "shortName", "description", "fullDescription", "address",
        "contacts.phone", "contacts.website", "schedule.regular",
        "schedule.days", "pricing.adult", "pricing.notes", "tags",
    }
    assert expected.issubset(set(EDITABLE_FIELDS.keys()))


def test_whitelist_specs_have_label_and_type():
    for key, spec in EDITABLE_FIELDS.items():
        assert spec.get("label"), f"у {key} нет label"
        assert spec.get("type") in {"str", "int", "tags"}, f"у {key} плохой type"


# --- get_field_value: превью текущего значения ---

def test_get_value_top_level_str():
    assert get_field_value(_museum(), "name") == "Сусанинский краеведческий музей"


def test_get_value_nested_str():
    assert get_field_value(_museum(), "contacts.phone") == "+7 (49434) 9-05-20"
    assert get_field_value(_museum(), "schedule.regular") == "Вт–Вс 09:00–17:30"


def test_get_value_int_as_str():
    assert get_field_value(_museum(), "pricing.adult") == "200"


def test_get_value_tags_joined_by_comma():
    assert get_field_value(_museum(), "tags") == "сусанин, история, музей"


def test_get_value_missing_returns_empty_string():
    obj = {"name": "Только имя"}
    assert get_field_value(obj, "contacts.phone") == ""
    assert get_field_value(obj, "tags") == ""
    assert get_field_value(obj, "pricing.adult") == ""


def test_get_value_unknown_field_raises():
    with pytest.raises(ValueError):
        get_field_value(_museum(), "coordinates.real.lat")


# --- apply_edit: установка вложенного строкового поля ---

def test_apply_edit_sets_nested_phone():
    obj = _museum()
    new_obj, old_display, new_display = apply_edit(obj, "contacts.phone", "+7 999 000-00-00")
    assert new_obj["contacts"]["phone"] == "+7 999 000-00-00"
    assert old_display == "+7 (49434) 9-05-20"
    assert new_display == "+7 999 000-00-00"


def test_apply_edit_sets_schedule_regular():
    new_obj, old_display, new_display = apply_edit(
        _museum(), "schedule.regular", "Ежедневно 10:00–18:00"
    )
    assert new_obj["schedule"]["regular"] == "Ежедневно 10:00–18:00"
    assert old_display == "Вт–Вс 09:00–17:30"
    assert new_display == "Ежедневно 10:00–18:00"


def test_apply_edit_sets_top_level_name():
    new_obj, _, new_display = apply_edit(_museum(), "name", "Новое имя")
    assert new_obj["name"] == "Новое имя"
    assert new_display == "Новое имя"


def test_apply_edit_creates_missing_nested_container():
    obj = {"name": "Без контактов", "meta": {"updatedAt": "2026-01-01"}}
    new_obj, old_display, new_display = apply_edit(obj, "contacts.website", "https://x.ru")
    assert new_obj["contacts"]["website"] == "https://x.ru"
    assert old_display == ""
    assert new_display == "https://x.ru"


# --- apply_edit: int-валидация цены ---

def test_apply_edit_price_int_ok():
    new_obj, old_display, new_display = apply_edit(_museum(), "pricing.adult", "350")
    assert new_obj["pricing"]["adult"] == 350
    assert isinstance(new_obj["pricing"]["adult"], int)
    assert old_display == "200"
    assert new_display == "350"


def test_apply_edit_price_strips_spaces():
    new_obj, _, new_display = apply_edit(_museum(), "pricing.adult", "  500  ")
    assert new_obj["pricing"]["adult"] == 500
    assert new_display == "500"


def test_apply_edit_price_non_int_raises():
    with pytest.raises(ValueError):
        apply_edit(_museum(), "pricing.adult", "дорого")


def test_apply_edit_price_float_raises():
    with pytest.raises(ValueError):
        apply_edit(_museum(), "pricing.adult", "199.99")


# --- apply_edit: отказ вне whitelist ---

def test_apply_edit_field_outside_whitelist_raises():
    with pytest.raises(ValueError):
        apply_edit(_museum(), "coordinates.real.lat", "59.0")


def test_apply_edit_business_field_outside_whitelist_raises():
    with pytest.raises(ValueError):
        apply_edit(_museum(), "business.tier", "paid")


# --- apply_edit: tags из строки через запятую ---

def test_apply_edit_tags_from_comma_string():
    new_obj, old_display, new_display = apply_edit(
        _museum(), "tags", "церковь, архитектура, XVII век"
    )
    assert new_obj["tags"] == ["церковь", "архитектура", "XVII век"]
    assert old_display == "сусанин, история, музей"
    assert new_display == "церковь, архитектура, XVII век"


def test_apply_edit_tags_strips_and_drops_empty():
    new_obj, _, _ = apply_edit(_museum(), "tags", "  один ,, два ,  , три  ")
    assert new_obj["tags"] == ["один", "два", "три"]


def test_apply_edit_tags_empty_string_gives_empty_list():
    new_obj, _, new_display = apply_edit(_museum(), "tags", "   ")
    assert new_obj["tags"] == []
    assert new_display == ""


# --- apply_edit: required-поле пустым нельзя ---

def test_apply_edit_required_name_empty_raises():
    with pytest.raises(ValueError):
        apply_edit(_museum(), "name", "   ")


def test_apply_edit_optional_field_empty_ok():
    # contacts.phone не required — пустое значение допустимо
    new_obj, _, new_display = apply_edit(_museum(), "contacts.phone", "")
    assert new_obj["contacts"]["phone"] == ""
    assert new_display == ""


# --- apply_edit: бамп meta.updatedAt ---

def test_apply_edit_bumps_updated_at_to_today():
    today = datetime.date.today().isoformat()
    new_obj, _, _ = apply_edit(_museum(), "name", "Имя")
    assert new_obj["meta"]["updatedAt"] == today


def test_apply_edit_creates_meta_if_absent():
    today = datetime.date.today().isoformat()
    obj = {"name": "Без меты"}
    new_obj, _, _ = apply_edit(obj, "name", "Новое")
    assert new_obj["meta"]["updatedAt"] == today


# --- apply_edit: неизменность исходного obj ---

def test_apply_edit_does_not_mutate_source():
    obj = _museum()
    snapshot = copy.deepcopy(obj)
    apply_edit(obj, "name", "Совсем другое")
    apply_edit(obj, "pricing.adult", "999")
    apply_edit(obj, "tags", "a, b")
    assert obj == snapshot, "исходный объект не должен меняться"


def test_apply_edit_nested_dict_is_deep_copied():
    obj = _museum()
    new_obj, _, _ = apply_edit(obj, "contacts.phone", "+7 000")
    # правка нового объекта не должна затрагивать вложенный dict исходного
    assert obj["contacts"]["phone"] == "+7 (49434) 9-05-20"
    assert new_obj["contacts"] is not obj["contacts"]
