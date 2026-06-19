"""
Построители ссылок на внешние карты (Яндекс.Карты, Google Maps).

Чистый Python: без aiogram и без обращений к сети. Координаты передаются
как (lat, lng); формат согласован с web/src/data/objects.json (externalLinks)
и контрактом бота.
"""
from urllib.parse import urlencode, quote


def yandex_maps_url(lat: float, lng: float, name: str = "") -> str:
    """
    Deep-link на Яндекс.Карты с центром в точке (lat, lng).

    В параметре `ll` Яндекс ожидает порядок «долгота,широта» (lng,lat).
    Опциональный `name` добавляется как параметр `text` (percent-encoding).
    """
    # ll=lng,lat — порядок, который ожидают Яндекс.Карты
    url = f"https://yandex.ru/maps/?ll={lng},{lat}&z=17"
    if name:
        url += "&text=" + quote(name)
    return url


def google_maps_url(lat: float, lng: float) -> str:
    """
    Ссылка на Google Maps (Maps URLs API) с поиском по координатам.
    Формат: https://www.google.com/maps/search/?api=1&query=lat,lng
    """
    query = urlencode({"api": 1, "query": f"{lat},{lng}"})
    return f"https://www.google.com/maps/search/?{query}"


def route_url(lat: float, lng: float, provider: str = "yandex") -> str:
    """
    Ссылка на построение маршрута до точки (lat, lng).

    provider:
        "yandex" — Яндекс.Карты (rtext до точки),
        "google" — Google Maps Directions (Maps URLs API).
    """
    if provider == "google":
        query = urlencode({"api": 1, "destination": f"{lat},{lng}"})
        return f"https://www.google.com/maps/dir/?{query}"
    # По умолчанию — Яндекс.Карты. rtext=~lat,lng — конечная точка маршрута.
    return f"https://yandex.ru/maps/?rtext=~{lat},{lng}&rtt=auto"
