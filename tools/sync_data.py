#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single-source синхронизация данных карты Сусанино.

КАНОН (источник истины): корневой data/  — его читает бот (DATA_DIR = bot/../data)
и правит будущая админка через бота (вариант A: JSON + git).
Назначение (генерируемое зеркало для статической сборки): web/src/data/

ВНИМАНИЕ: для веба это делается автоматически — `npm run dev` / `npm run build`
вызывают `web/scripts/sync-data.mjs` (хуки predev/prebuild). Этот Python-скрипт —
ручной эквивалент того же направления (на случай работы без Node).

Копирование (не перемещение). Существующие файлы перезаписываются.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # .../susanino-map
SRC_DIR = ROOT / "data"                             # КАНОН (корневой data/)
DST_DIR = ROOT / "web" / "src" / "data"             # зеркало для сборки

JSON_FILES = ["config.json", "categories.json", "objects.json"]
ILLUSTRATIONS = "illustrations"


def main() -> int:
    if not SRC_DIR.exists():
        print(f"ОШИБКА: канон не найден: {SRC_DIR}")
        return 1

    DST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Канон:      {SRC_DIR}")
    print(f"Зеркало:    {DST_DIR}")
    print("-" * 60)

    copied_files = 0

    # 1) Одиночные JSON-файлы
    for name in JSON_FILES:
        src = SRC_DIR / name
        if not src.exists():
            print(f"  ПРОПУСК (нет в каноне): {name}")
            continue
        dst = DST_DIR / name
        shutil.copy2(src, dst)
        copied_files += 1
        print(f"  OK json: {name} -> {dst}")

    # 2) Папка illustrations целиком
    src_ill = SRC_DIR / ILLUSTRATIONS
    if src_ill.exists() and src_ill.is_dir():
        dst_ill = DST_DIR / ILLUSTRATIONS
        shutil.copytree(src_ill, dst_ill, dirs_exist_ok=True)
        ill_count = sum(1 for _ in dst_ill.rglob("*") if _.is_file())
        print(f"  OK dir : {ILLUSTRATIONS}/ -> {dst_ill} ({ill_count} файлов)")
    else:
        ill_count = 0
        print(f"  ПРОПУСК (нет папки): {ILLUSTRATIONS}/")

    print("-" * 60)
    print(f"Синхронизировано JSON-файлов: {copied_files}")
    print(f"Синхронизировано файлов в illustrations/: {ill_count}")
    print("Готово.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
