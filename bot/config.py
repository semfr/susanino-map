import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из директории бота
load_dotenv(Path(__file__).parent / ".env")

BOT_TOKEN: str = os.environ["BOT_TOKEN"]

# Директория с данными (относительно директории бота)
DATA_DIR: Path = Path(__file__).parent.parent / "data"
