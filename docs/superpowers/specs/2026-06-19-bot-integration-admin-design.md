# Спек: интеграция бот ↔ сайт (п.6) + админка через бота (п.7)

Дата: 2026-06-19. Проект: Карта Сусанино (`susanino-map`). Репо: `semfr/susanino-map` (public).
Сайт: GitHub Pages `https://semfr.github.io/susanino-map` (basePath `/susanino-map`), сборка по push в `master` через `.github/workflows/deploy.yml`.
Бот: VPS Fornex, polling, systemd `susanino-bot`, читает канон `data/*.json` напрямую, обновляется `git reset --hard origin/master`.

Источник истины данных — корневой `data/objects.json`. Веб-зеркало `web/src/data/` генерируется на build.

---

## Часть A — связка бот ↔ сайт (модель «гибрид»: companion-хребет + витринные выигрыши)

### A1. Deep-link сайт → бот (по объекту)
- Формат: `https://t.me/susanino_map_bot?start=obj_<id>` (id вида `susanino-museum`; дефисы в start-payload допустимы).
- Бот: `/start` разбирает аргумент. Если `obj_<id>` и объект существует → сразу карточка объекта (переиспользовать рендер `handlers/objects.py`). Иначе обычный welcome.
- Сайт: кнопка «Открыть в Telegram-боте» на странице `/object/[slug]` и в bottom-sheet карты.

### A2. Фикс ссылок бот → сайт
- Убрать хардкод `https://susanino-map.ru`. Ввести `SITE_BASE_URL` (env, дефолт `https://semfr.github.io/susanino-map`).
- `keyboards/inline.py`: кнопка «🌐 На сайте» → `{SITE_BASE_URL}/object/{slug}`.

### A3. Welcome → сайт
- В `/start` инлайн-кнопка «🗺 Открыть карту-лубок на сайте» → `SITE_BASE_URL`.

### A4. Inline-режим (главный витринный множитель)
- `@susanino_map_bot <запрос>` в любом чате → объекты как `InlineQueryResultArticle` (title=name, description=shortName/description, message text = текст карточки + ссылка на сайт, reply_markup с «На сайте»/«Маршрут»).
- Добавить `inline_query` в `allowed_updates` бота; включить inline у @BotFather (ручной ops-шаг).

### A5. Полный каталог
- Уже есть (категории → объекты → карточка, «что рядом», маршруты). Новой стройки нет — проверить целостность.

---

## Часть B — админка через бота (п.7)

### B1. Доступ
- `ADMIN_IDS: set[int]` из env (`192201651` кладётся в `.env` на VPS, **не в код**). Гард на всех admin-хэндлерах: `from_user.id in ADMIN_IDS`, иначе игнор.

### B2. Диалог (FSM, меню по кнопкам)
```
/admin → [список объектов] → объект → [поля + текущие значения]
      → выбрать поле → бот просит новое значение → превью «было → стало»
      → [✅ Опубликовать] / [✖️ Отмена] → публикация → «Сайт обновится за ~1–2 мин»
```
- Whitelist редактируемых полей (только текстовые оперативные):
  `name`, `shortName`, `description`, `fullDescription`, `address`,
  `contacts.phone`, `contacts.website`, `schedule.regular`, `schedule.days`,
  `pricing.adult` (int), `pricing.notes`, `tags` (список через запятую).
- Фото/координаты/slug/категория — вне MVP.

### B3. Запись данных (ядро)
- `services/object_editor.py` — **чистая логика** (TDD):
  - `EDITABLE_FIELDS: dict[str, FieldSpec]` — whitelist (label, путь, тип, required).
  - `get_field_value(obj, field_key) -> str` — текущее значение для превью.
  - `apply_edit(obj, field_key, raw_value) -> (new_obj, old_display, new_display)` —
    валидация типа/whitelist (raise ValueError при нарушении), bump `meta.updatedAt` = сегодня.
- `services/github_publish.py`:
  - `build_commit_payload(content_str, message, sha, branch) -> dict` — чистая (base64 content + тело PUT).
  - `async publish_objects(objects) -> str` — GET текущего sha файла → PUT нового контента → вернуть commit html_url; raise при ошибке. Через `aiohttp` (уже есть у aiogram).
- **Порядок (атомарность):** сперва коммит в GitHub (канон) → при успехе `data_loader.update_objects(...)` (in-memory + локальный `DATA_DIR/objects.json`). Коммит упал → ничего не меняем, сообщить админу. Следующий `git reset --hard origin/master` сводит локальное с origin без конфликта.

### B4. Конфиг/секреты (`.env`, не код)
- `GITHUB_TOKEN` — fine-grained PAT, scope = Contents:RW **только** на `semfr/susanino-map` (без workflows).
- `GITHUB_REPO="semfr/susanino-map"`, `GITHUB_BRANCH="master"`, `DATA_FILE_IN_REPO="data/objects.json"`.
- `ADMIN_IDS`, `SITE_BASE_URL`, `BOT_USERNAME="susanino_map_bot"`.
- Обновить `.env.example` плейсхолдерами. Зависимостей не добавлять.

### B5. Guardrails
- Whitelist полей на сервере (не только в UI), валидация типа/длины, превью+подтверждение, admin-гард,
  минимальный scope токена, audit: id админа + поле + объект в commit message + `updatedAt`.

---

## Контракт интерфейсов (агреемент между модулями)

- `config`: `ADMIN_IDS: set[int]`, `GITHUB_TOKEN: str`, `GITHUB_REPO: str`, `GITHUB_BRANCH: str`,
  `DATA_FILE_IN_REPO: str`, `SITE_BASE_URL: str`, `BOT_USERNAME: str` (+ существующие `BOT_TOKEN`, `DATA_DIR`).
- `services/deeplink.py`: `parse_start_payload(raw: str | None) -> str | None` (id из `obj_<id>`, id = `[a-z0-9-]+`).
- `services/object_editor.py`: `EDITABLE_FIELDS`, `get_field_value`, `apply_edit` (см. B3).
- `services/github_publish.py`: `build_commit_payload`, `publish_objects` (см. B3).
- `services/data_loader.py`: добавить `update_objects(new_objects: list[dict]) -> None` (перестроить индексы + записать локальный файл).
- `handlers/inline.py`: `build_inline_results(objects, query, site_base_url, bot_username) -> list`, хэндлер `inline_query`.
- `handlers/admin.py`: router `/admin` (admin-only), FSM, callbacks `adm:*`.
- Сайт: `web/src/lib/botLink.ts` → `botDeepLink(objectId): string` (+ vitest-тест), кнопки на странице объекта и в bottom-sheet.

## Тестирование (TDD, pytest для бота / vitest для веба)
Чистые функции: `parse_start_payload`, `object_editor` (apply_edit, валидация, whitelist, updatedAt),
`build_commit_payload`/base64, `build_inline_results`, `botDeepLink`. Сетевые вызовы — за моками.

## Очерёдность реализации
A (п.6) первой — дёшево и даёт ценность. B (п.7) второй — секрет + запись.

## Ops-шаги (вне кода, на деплое)
1. Fine-grained PAT (`semfr/susanino-map`, Contents RW) → VPS `.env` `GITHUB_TOKEN`.
2. `ADMIN_IDS=192201651` в VPS `.env`.
3. Включить inline у @BotFather (`/setinline`).
4. Передеплоить бота (`deploy-bot.sh`).

## Вне MVP (YAGNI / следующие этапы)
Telegram Mini App; правка фото/координат; кастомный домен `susanino-map.ru`; мультиадмин/роли; полнотекстовый поиск в боте (закрывает inline).
