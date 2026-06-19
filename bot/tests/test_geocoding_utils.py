"""
Тесты для построителей ссылок на карты (services.geocoding).
Чистый Python: проверяем формат URL без сети и aiogram.
"""
from urllib.parse import urlparse, parse_qs

import pytest

from services.geocoding import yandex_maps_url, google_maps_url, route_url

# Тестовая точка: Сусанинский краеведческий музей
LAT = 58.1472
LNG = 41.5892
CYR_NAME = "Сусанинский музей"


# --- yandex_maps_url ---------------------------------------------------------

def test_yandex_host():
    """Хост должен быть yandex.ru/maps."""
    parsed = urlparse(yandex_maps_url(LAT, LNG))
    assert parsed.netloc == "yandex.ru"
    assert parsed.path.startswith("/maps")


def test_yandex_contains_lat_lng():
    """Широта и долгота присутствуют в URL."""
    url = yandex_maps_url(LAT, LNG)
    assert str(LAT) in url
    assert str(LNG) in url


def test_yandex_name_percent_encoded():
    """Кириллический name закодирован percent-encoding; нет сырой кириллицы."""
    url = yandex_maps_url(LAT, LNG, name=CYR_NAME)
    # Сырой кириллицы в URL быть не должно
    assert all(ord(ch) < 128 for ch in url)
    # Имя присутствует в percent-encoded виде (через параметр text)
    qs = parse_qs(urlparse(url).query)
    assert qs.get("text") == [CYR_NAME]
    assert "%" in url


def test_yandex_no_name_no_text():
    """Без name параметр text отсутствует."""
    qs = parse_qs(urlparse(yandex_maps_url(LAT, LNG)).query)
    assert "text" not in qs


# --- google_maps_url ---------------------------------------------------------

def test_google_host():
    """Хост должен быть www.google.com/maps."""
    parsed = urlparse(google_maps_url(LAT, LNG))
    assert parsed.netloc == "www.google.com"
    assert parsed.path.startswith("/maps")


def test_google_query_format():
    """Формат query=lat,lng и api=1."""
    qs = parse_qs(urlparse(google_maps_url(LAT, LNG)).query)
    assert qs.get("api") == ["1"]
    assert qs.get("query") == [f"{LAT},{LNG}"]


def test_google_contains_lat_lng():
    url = google_maps_url(LAT, LNG)
    assert str(LAT) in url
    assert str(LNG) in url


# --- route_url ---------------------------------------------------------------

@pytest.mark.parametrize("provider,host", [
    ("yandex", "yandex.ru"),
    ("google", "www.google.com"),
])
def test_route_host_by_provider(provider, host):
    """provider переключает хост маршрута."""
    parsed = urlparse(route_url(LAT, LNG, provider=provider))
    assert parsed.netloc == host


def test_route_contains_lat_lng():
    for provider in ("yandex", "google"):
        url = route_url(LAT, LNG, provider=provider)
        assert str(LAT) in url
        assert str(LNG) in url


def test_route_provider_changes_url():
    """Смена provider меняет URL."""
    assert route_url(LAT, LNG, provider="yandex") != route_url(LAT, LNG, provider="google")


def test_route_default_is_yandex():
    """По умолчанию provider=yandex."""
    assert route_url(LAT, LNG) == route_url(LAT, LNG, provider="yandex")
