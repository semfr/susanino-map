"""
Публикация канона `data/objects.json` в GitHub через Contents API.

Порядок (см. спек, B3): сперва коммит в GitHub → при успехе вызывающий код
обновляет локальные данные. Если коммит упал — данные не трогаем.

build_commit_payload — чистая функция (формирование тела PUT), без config/сети.
publish_objects — сетевой вызов на aiohttp; config импортируется ЛЕНИВО внутри,
т.к. config.py читает os.environ при импорте.
"""
import base64
import json
from typing import Any

import aiohttp

# Сообщение коммита (audit: правка приходит через бота-админку).
COMMIT_MESSAGE = "data: правка объекта через бота"

_API_BASE = "https://api.github.com"
_TIMEOUT = aiohttp.ClientTimeout(total=30)


def build_commit_payload(content_str: str, message: str, sha: str, branch: str) -> dict[str, Any]:
    """
    Тело PUT-запроса для GitHub Contents API (обновление файла).

    Чистая функция: контент кодируется в base64 (utf-8), без обращения к config/сети.

    :param content_str: новое содержимое файла (текст).
    :param message: сообщение коммита.
    :param sha: текущий blob-sha файла (обязателен при обновлении существующего файла).
    :param branch: ветка для коммита.
    :return: словарь {message, content (base64), sha, branch}.
    """
    encoded = base64.b64encode(content_str.encode("utf-8")).decode("ascii")
    return {
        "message": message,
        "content": encoded,
        "sha": sha,
        "branch": branch,
    }


async def publish_objects(objects: list[dict]) -> str:
    """
    Публикует список объектов как `data/objects.json` в репозиторий на GitHub.

    Шаги:
      1. GET текущего файла — берём blob-sha.
      2. PUT нового содержимого (build_commit_payload).
      3. При 200/201 возвращаем commit html_url, иначе raise с текстом ответа.

    config импортируется лениво (config.py читает os.environ при импорте).

    :raises RuntimeError: если GitHub вернул не-успешный статус.
    :return: html_url созданного коммита.
    """
    import config  # ленивый импорт: модуль читает os.environ при импорте

    content_str = json.dumps(objects, ensure_ascii=False, indent=2)

    path = config.DATA_FILE_IN_REPO
    contents_url = f"{_API_BASE}/repos/{config.GITHUB_REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    async with aiohttp.ClientSession(timeout=_TIMEOUT, headers=headers) as session:
        # 1) Текущий sha файла
        async with session.get(contents_url, params={"ref": config.GITHUB_BRANCH}) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"GitHub GET {resp.status}: {text}")
            current = await resp.json()
        sha = current["sha"]

        # 2) PUT нового содержимого
        payload = build_commit_payload(content_str, COMMIT_MESSAGE, sha, config.GITHUB_BRANCH)
        async with session.put(contents_url, json=payload) as resp:
            text = await resp.text()
            if resp.status not in (200, 201):
                raise RuntimeError(f"GitHub PUT {resp.status}: {text}")
            data = json.loads(text)

    return data["commit"]["html_url"]
