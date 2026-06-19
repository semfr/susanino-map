#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор пирамиды тайлов для лубочной карты Сусанино под Leaflet CRS.Simple.

Источник: guide_susanino.jpg (2520x2560).
Выход: web/public/tiles/lubok/{z}/{x}/{y}.png

Параметры пирамиды:
  - tileSize = 256
  - уровни z = 0..4, где z=4 — масштаб 1:1 (полное разрешение)
  - на уровне z картинка ресайзится до (W / 2**(4-z), H / 2**(4-z))
  - сетка на z: cols = ceil(scaledW/256), rows = ceil(scaledH/256)
  - тайл (x,y): crop box (x*256, y*256, min((x+1)*256, scaledW), min((y+1)*256, scaledH))
    вставляется в ПРОЗРАЧНЫЙ холст 256x256 RGBA (0,0,0,0) в позицию (0,0) — top-left.
    Центрирование НЕ применяется: оно сдвинуло бы origin и рассинхронило якоря на краях.
  - tms = False (y=0 — ВЕРХНИЙ ряд)

Используется только Pillow (без VIPS/GDAL).
"""

import math
import sys
from pathlib import Path

from PIL import Image

# Снимаем ограничение на размер (карта большая, но не decompression bomb).
Image.MAX_IMAGE_PIXELS = None

# --- Пути ---
ROOT = Path(__file__).resolve().parent.parent          # .../susanino-map
SOURCE = ROOT.parent / "guide_susanino.jpg"            # .../Карта Сусанино/guide_susanino.jpg
OUT_DIR = ROOT / "web" / "public" / "tiles" / "lubok"  # выход тайлов

# --- Параметры пирамиды ---
TILE_SIZE = 256
MAX_ZOOM = 4   # z=4 -> 1:1
MIN_ZOOM = 0


def main() -> int:
    if not SOURCE.exists():
        print(f"ОШИБКА: исходник не найден: {SOURCE}")
        return 1

    src = Image.open(SOURCE)
    base_w, base_h = src.size
    print(f"Исходник: {SOURCE}")
    print(f"Размер исходника: {base_w}x{base_h}, режим {src.mode}")
    print(f"tileSize={TILE_SIZE}, уровни z={MIN_ZOOM}..{MAX_ZOOM} (z={MAX_ZOOM} -> 1:1)")
    print("-" * 60)

    # Работаем с RGBA, чтобы прозрачный фон краёв был корректным.
    src_rgba = src.convert("RGBA")

    total_tiles = 0
    grid_summary = []

    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        divisor = 2 ** (MAX_ZOOM - z)
        scaled_w = max(1, base_w // divisor)
        scaled_h = max(1, base_h // divisor)

        if z == MAX_ZOOM:
            scaled = src_rgba  # 1:1, без ресайза
        else:
            scaled = src_rgba.resize((scaled_w, scaled_h), Image.LANCZOS)

        # фактический размер после ресайза (на случай округлений)
        scaled_w, scaled_h = scaled.size

        cols = math.ceil(scaled_w / TILE_SIZE)
        rows = math.ceil(scaled_h / TILE_SIZE)

        z_dir = OUT_DIR / str(z)

        z_tiles = 0
        for x in range(cols):
            col_dir = z_dir / str(x)
            col_dir.mkdir(parents=True, exist_ok=True)
            for y in range(rows):
                left = x * TILE_SIZE
                upper = y * TILE_SIZE
                right = min((x + 1) * TILE_SIZE, scaled_w)
                lower = min((y + 1) * TILE_SIZE, scaled_h)

                crop = scaled.crop((left, upper, right, lower))

                # Прозрачный холст 256x256, вставка в (0,0) — top-left.
                canvas = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
                canvas.paste(crop, (0, 0))

                canvas.save(col_dir / f"{y}.png", "PNG")
                z_tiles += 1

        total_tiles += z_tiles
        grid_summary.append((z, scaled_w, scaled_h, cols, rows, z_tiles))
        print(f"z={z}: scaled={scaled_w}x{scaled_h}, сетка {cols}x{rows} (cols x rows), тайлов={z_tiles}")

    print("-" * 60)
    print("СВОДКА:")
    for z, sw, sh, cols, rows, n in grid_summary:
        print(f"  z={z}: {sw}x{sh}px -> {cols}cols x {rows}rows = {n} тайлов")
    print(f"  Всего тайлов: {total_tiles}")
    print("-" * 60)
    print("Параметры для Leaflet (CRS.Simple):")
    print(f"  minZoom = {MIN_ZOOM}")
    print(f"  maxZoom = {MAX_ZOOM}")
    print(f"  tileSize = {TILE_SIZE}")
    print(f"  tms = false (y=0 — верхний ряд)")
    print(f"  url = /tiles/lubok/{{z}}/{{x}}/{{y}}.png")
    print(f"  Размеры карты в пикселях (z={MAX_ZOOM}): {base_w}x{base_h}")
    print("Готово.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
