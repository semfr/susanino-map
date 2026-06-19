"""
Тесты публикации правок в GitHub (GitHub Contents API).

Сетевую часть (publish_objects) тестируем за моком aiohttp; основной упор —
на чистую функцию build_commit_payload (формирование тела PUT-запроса).
Контракт:
  build_commit_payload(content_str, message, sha, branch) -> dict
    -> {message, content (base64 utf-8), sha, branch}
"""
import base64

from services.github_publish import build_commit_payload


# --- Чистая функция build_commit_payload ---

def test_payload_has_all_required_fields():
    payload = build_commit_payload("содержимое", "msg", "abc123", "master")
    assert set(payload.keys()) == {"message", "content", "sha", "branch"}


def test_payload_passes_through_message_sha_branch():
    payload = build_commit_payload("x", "правка объекта", "deadbeef", "master")
    assert payload["message"] == "правка объекта"
    assert payload["sha"] == "deadbeef"
    assert payload["branch"] == "master"


def test_content_is_base64_of_utf8_round_trip():
    original = '{"name": "Музей", "emoji": "🏛"}'
    payload = build_commit_payload(original, "m", "s", "master")
    # base64 -> исходная utf-8 строка
    decoded = base64.b64decode(payload["content"]).decode("utf-8")
    assert decoded == original


def test_content_is_pure_base64_without_newlines():
    # GitHub Contents API ждёт строку base64; гарантируем валидный ASCII-base64
    payload = build_commit_payload("a" * 1000, "m", "s", "master")
    content = payload["content"]
    assert isinstance(content, str)
    # стандартный (не urlsafe) алфавит base64
    assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in content)


def test_empty_content_encodes_to_empty_base64():
    payload = build_commit_payload("", "m", "s", "master")
    assert payload["content"] == ""
    assert base64.b64decode(payload["content"]).decode("utf-8") == ""
