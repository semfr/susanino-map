"""
Фабрики инлайн-клавиатур для бота.
"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def categories_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора категории.
    Callback data: cat:{category_id}
    """
    from services.data_loader import get_categories

    builder = InlineKeyboardBuilder()
    for cat in get_categories():
        emoji = cat.get("emoji", "")
        label = f"{emoji} {cat['name']}".strip()
        builder.button(text=label, callback_data=f"cat:{cat['id']}")
    builder.adjust(2)
    return builder.as_markup()


def objects_keyboard(objects: list[dict]) -> InlineKeyboardMarkup:
    """
    Клавиатура со списком объектов.
    Callback data: obj:{object_id}
    """
    builder = InlineKeyboardBuilder()
    for obj in objects:
        builder.button(text=obj.get("shortName") or obj["name"], callback_data=f"obj:{obj['id']}")
    builder.adjust(1)
    builder.button(text="◀ Назад к категориям", callback_data="back:categories")
    builder.adjust(1)
    return builder.as_markup()


def object_actions_keyboard(obj: dict) -> InlineKeyboardMarkup:
    """
    Клавиатура действий для конкретного объекта.
    Кнопки: [На сайте] [Маршрут] [Назад к списку]
    """
    from config import SITE_BASE_URL  # лениво: config читает os.environ при импорте

    builder = InlineKeyboardBuilder()

    # Ссылка на страницу объекта на сайте (базовый URL — из конфига)
    slug = obj.get("slug", obj["id"])
    site_url = f"{SITE_BASE_URL}/object/{slug}"
    builder.button(text="🌐 На сайте", url=site_url)

    # Ссылка на Яндекс.Карты (маршрут)
    coords = obj.get("coordinates", {}).get("real", {})
    lat = coords.get("lat")
    lng = coords.get("lng")
    if lat is not None and lng is not None:
        maps_url = f"https://yandex.ru/maps/?rtext=~{lat},{lng}&rtt=auto"
        builder.button(text="🗺 Маршрут", url=maps_url)

    # Кнопка возврата к списку категории
    category_id = obj.get("categoryId", "")
    builder.button(text="◀ Назад к списку", callback_data=f"cat:{category_id}")

    builder.adjust(2, 1)
    return builder.as_markup()
