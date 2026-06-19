import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из директории бота
load_dotenv(Path(__file__).parent / ".env")

BOT_TOKEN: str = os.environ["BOT_TOKEN"]

# Директория с данными: по умолчанию ../data относительно бота,
# переопределяется переменной окружения DATA_DIR (для нестандартного размещения на сервере).
DATA_DIR: Path = Path(os.environ.get("DATA_DIR") or (Path(__file__).parent.parent / "data"))


def _parse_admin_ids(raw: str | None) -> set[int]:
    """
    Парсит ADMIN_IDS из строки env: id через запятую -> set[int].
    Пустые элементы и пробелы игнорируются. Нечисловые элементы пропускаются.
    Пустой/None -> пустое множество (никто не админ).
    """
    if not raw:
        return set()
    ids: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.add(int(part))
        except ValueError:
            # Мусор в env не должен валить старт бота — просто пропускаем.
            continue
    return ids


# --- Админка и публикация (часть B спеки) ---

# Telegram-id администраторов (через запятую в env ADMIN_IDS). Пусто по умолчанию.
ADMIN_IDS: set[int] = _parse_admin_ids(os.environ.get("ADMIN_IDS"))

# Fine-grained PAT с правом Contents:RW только на репо semfr/susanino-map.
# Держим в .env, НЕ в коде. По умолчанию пусто (публикация недоступна).
GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")

# Репозиторий канона, ветка и путь к файлу данных внутри репо.
GITHUB_REPO: str = os.environ.get("GITHUB_REPO", "semfr/susanino-map")
GITHUB_BRANCH: str = os.environ.get("GITHUB_BRANCH", "master")
DATA_FILE_IN_REPO: str = os.environ.get("DATA_FILE_IN_REPO", "data/objects.json")

# Базовый URL сайта (GitHub Pages) для ссылок «На сайте» и deep-link.
SITE_BASE_URL: str = os.environ.get("SITE_BASE_URL", "https://semfr.github.io/susanino-map")

# Username бота без @ (для inline/deep-link).
BOT_USERNAME: str = os.environ.get("BOT_USERNAME", "susanino_map_bot")
