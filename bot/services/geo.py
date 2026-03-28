"""
Геопространственные вычисления: формула Хаверсина и поиск ближайших объектов.
"""
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Вычисляет расстояние между двумя точками на сфере (формула Хаверсина).
    Возвращает расстояние в километрах.
    """
    R = 6371.0  # Радиус Земли, км
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def find_nearest(lat: float, lng: float, n: int = 5) -> list[tuple[dict, float]]:
    """
    Находит n ближайших объектов к заданным координатам.

    Args:
        lat: Широта пользователя.
        lng: Долгота пользователя.
        n: Количество возвращаемых объектов (по умолчанию 5).

    Returns:
        Список кортежей (объект, расстояние_в_км), отсортированных по возрастанию расстояния.
    """
    # Импортируем здесь, чтобы избежать циклических зависимостей
    from services.data_loader import get_objects

    objects = get_objects()
    results: list[tuple[dict, float]] = []

    for obj in objects:
        coords = obj.get("coordinates", {}).get("real", {})
        obj_lat = coords.get("lat")
        obj_lng = coords.get("lng")
        if obj_lat is None or obj_lng is None:
            continue
        dist = haversine(lat, lng, obj_lat, obj_lng)
        results.append((obj, dist))

    results.sort(key=lambda x: x[1])
    return results[:n]
