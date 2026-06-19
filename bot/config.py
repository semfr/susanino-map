import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из директории бота
load_dotenv(Path(__file__).parent / ".env")

BOT_TOKEN: str = os.environ["BOT_TOKEN"]

# Директория с данными: по умолчанию ../data относительно бота,
# переопределяется переменной окружения DATA_DIR (для нестандартного размещения на сервере).
DATA_DIR: Path = Path(os.environ.get("DATA_DIR") or (Path(__file__).parent.parent / "data"))
