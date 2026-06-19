"""
Загрузка и кэширование данных из JSON-файлов.
Данные загружаются один раз при импорте модуля.
"""
import json
from pathlib import Path
from typing import Any

from config import DATA_DIR

# --- Загрузка данных при импорте ---

def _load_json(filename: str) -> Any:
    path = DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


_config: dict = _load_json("config.json")
_categories: list[dict] = _load_json("categories.json")
_objects: list[dict] = _load_json("objects.json")

# Индексы для быстрого поиска
_objects_by_id: dict[str, dict] = {obj["id"]: obj for obj in _objects}
_objects_by_category: dict[str, list[dict]] = {}
for _obj in _objects:
    _cat_id = _obj.get("categoryId", "")
    _objects_by_category.setdefault(_cat_id, []).append(_obj)


# --- Публичные функции ---

def get_config() -> dict:
    """Возвращает конфиг карты (config.json)."""
    return _config


def get_categories() -> list[dict]:
    """Возвращает список категорий, отсортированный по sortOrder."""
    return sorted(_categories, key=lambda c: c.get("sortOrder", 999))


def get_objects() -> list[dict]:
    """Возвращает полный список объектов."""
    return _objects


def get_object_by_id(obj_id: str) -> dict | None:
    """Возвращает объект по id или None, если не найден."""
    return _objects_by_id.get(obj_id)


def get_objects_by_category(category_id: str) -> list[dict]:
    """Возвращает список объектов заданной категории."""
    return _objects_by_category.get(category_id, [])


def update_objects(new_objects: list[dict]) -> None:
    """
    Обновляет данные объектов «на лету» после успешной публикации в GitHub.

    Перестраивает in-memory список и индексы (_objects, _objects_by_id,
    _objects_by_category) и переписывает локальный DATA_DIR/objects.json
    (utf-8, ensure_ascii=False, indent=2), чтобы локальная копия совпадала
    с каноном до следующего `git reset --hard origin/master`.

    Вызывается только ПОСЛЕ успешного коммита (см. спек B3, атомарность).
    """
    global _objects, _objects_by_id, _objects_by_category

    _objects = new_objects
    _objects_by_id = {obj["id"]: obj for obj in _objects}

    _objects_by_category = {}
    for obj in _objects:
        cat_id = obj.get("categoryId", "")
        _objects_by_category.setdefault(cat_id, []).append(obj)

    path = DATA_DIR / "objects.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_objects, f, ensure_ascii=False, indent=2)
