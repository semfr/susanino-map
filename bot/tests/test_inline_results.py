"""
Тесты чистой функции build_inline_results (inline-режим бота, A4).

Контракт:
  build_inline_results(objects, query, site_base_url, bot_username)
    -> list[InlineQueryResultArticle]

Функция чистая: не импортирует config, не ходит в сеть.
Сетевые типы aiogram создаются как обычные объекты (без обращения к Telegram).
"""
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from handlers.inline import build_inline_results

SITE = "https://semfr.github.io/susanino-map"
BOT = "susanino_map_bot"


# --- Фикстуры данных ---

def _objects() -> list[dict]:
    return [
        {
            "id": "susanino-museum",
            "slug": "susanino-kraevedcheskiy-muzey",
            "name": "Краеведческий музей",
            "shortName": "Краеведческий музей",
            "description": "Музей в селе Сусанино.",
            "tags": ["история", "музей"],
        },
        {
            "id": "ivan-susanin-monument",
            "slug": "pamyatnik-ivanu-susaninu",
            "name": "Памятник Ивану Сусанину",
            "shortName": "Памятник Сусанину",
            "description": "Монумент народному герою.",
            "tags": ["памятник", "история"],
        },
        {
            "id": "voskresenskaya-church",
            "slug": "voskresenskaya-cerkov",
            "name": "Воскресенская церковь",
            "description": "Та самая церковь с картины Саврасова «Грачи прилетели».",
            "tags": ["храм", "живопись"],
        },
    ]


# --- Тип результата ---

def test_returns_list_of_inline_article_results():
    results = build_inline_results(_objects(), "", SITE, BOT)
    assert isinstance(results, list)
    assert results
    for r in results:
        assert isinstance(r, InlineQueryResultArticle)


# --- Пустой запрос -> все объекты ---

def test_empty_query_returns_all_objects():
    objs = _objects()
    results = build_inline_results(objs, "", SITE, BOT)
    assert len(results) == len(objs)


def test_none_query_returns_all_objects():
    objs = _objects()
    results = build_inline_results(objs, None, SITE, BOT)
    assert len(results) == len(objs)


# --- Фильтр по подстроке имени (регистронезависимо) ---

def test_filter_by_name_substring_case_insensitive():
    results = build_inline_results(_objects(), "церковь", SITE, BOT)
    ids = [r.id for r in results]
    assert ids == ["voskresenskaya-church"]


def test_filter_by_name_uppercase_query():
    results = build_inline_results(_objects(), "МУЗЕЙ", SITE, BOT)
    ids = [r.id for r in results]
    assert ids == ["susanino-museum"]


# --- Фильтр по shortName ---

def test_filter_by_short_name():
    # "Памятник Сусанину" есть в shortName второго объекта
    results = build_inline_results(_objects(), "сусанину", SITE, BOT)
    ids = [r.id for r in results]
    assert "ivan-susanin-monument" in ids


# --- Фильтр по тегу ---

def test_filter_by_tag():
    results = build_inline_results(_objects(), "храм", SITE, BOT)
    ids = [r.id for r in results]
    assert ids == ["voskresenskaya-church"]


def test_tag_matches_multiple_objects():
    results = build_inline_results(_objects(), "история", SITE, BOT)
    ids = set(r.id for r in results)
    assert ids == {"susanino-museum", "ivan-susanin-monument"}


# --- Нет совпадений ---

def test_no_match_returns_empty_list():
    results = build_inline_results(_objects(), "зоопарк", SITE, BOT)
    assert results == []


# --- Заполнение полей результата ---

def test_result_fields_id_and_title():
    results = build_inline_results(_objects(), "музей", SITE, BOT)
    r = results[0]
    assert r.id == "susanino-museum"
    assert r.title == "Краеведческий музей"


def test_description_uses_short_name_when_present():
    results = build_inline_results(_objects(), "музей", SITE, BOT)
    r = results[0]
    assert r.description == "Краеведческий музей"


def test_description_falls_back_to_description_text():
    # У Воскресенской церкви нет shortName -> берётся начало description
    results = build_inline_results(_objects(), "церковь", SITE, BOT)
    r = results[0]
    assert r.description
    assert "церковь" in r.description.lower() or "Саврасова" in r.description


def test_input_message_content_is_text_with_site_link():
    results = build_inline_results(_objects(), "музей", SITE, BOT)
    r = results[0]
    assert isinstance(r.input_message_content, InputTextMessageContent)
    text = r.input_message_content.message_text
    assert "Краеведческий музей" in text
    # Ссылка на страницу объекта на сайте по slug
    assert f"{SITE}/object/susanino-kraevedcheskiy-muzey" in text


def test_message_text_uses_id_when_slug_missing():
    objs = [{"id": "no-slug-obj", "name": "Без слага"}]
    results = build_inline_results(objs, "", SITE, BOT)
    text = results[0].input_message_content.message_text
    assert f"{SITE}/object/no-slug-obj" in text


# --- Лимит результатов ---

def test_results_are_limited():
    many = [
        {"id": f"obj-{i}", "slug": f"obj-{i}", "name": f"Объект {i}"}
        for i in range(50)
    ]
    results = build_inline_results(many, "", SITE, BOT)
    assert len(results) <= 20


# --- Устойчивость: объект без необязательных полей не валит функцию ---

def test_minimal_object_does_not_crash():
    objs = [{"id": "min", "name": "Минимальный"}]
    results = build_inline_results(objs, "", SITE, BOT)
    assert len(results) == 1
    assert results[0].title == "Минимальный"
