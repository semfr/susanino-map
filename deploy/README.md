# Деплой

## Веб-сайт
Деплоится автоматически на **GitHub Pages** через `.github/workflows/deploy.yml`
при каждом push в `master`. URL: https://semfr.github.io/susanino-map/
(статический экспорт Next.js, basePath `/susanino-map`). Своего сервера для веба не нужно.

## Бот (Telegram, polling) — VPS
Бот — фоновый процесс, только исходящие запросы к Telegram. Не нужны nginx, домен, TLS.
Деплой тянет код из публичного git-репозитория; секрет (токен) хранится только в `.env` на сервере.

### Первый деплой
1. Зайти на сервер: `ssh root@<vps-ip>`
2. Скачать и запустить скрипт (он склонирует репо в `/opt/susanino-map`, поставит зависимости,
   на шаге 5 остановится из-за отсутствия `.env`):
   ```bash
   curl -fsSL https://raw.githubusercontent.com/semfr/susanino-map/master/deploy/deploy-bot.sh -o /tmp/deploy-bot.sh
   bash /tmp/deploy-bot.sh   # упадёт на шаге 5: нет .env — это ожидаемо
   ```
3. Создать `.env` с токеном:
   ```bash
   cp /opt/susanino-map/bot/.env.example /opt/susanino-map/bot/.env
   nano /opt/susanino-map/bot/.env        # вписать BOT_TOKEN=...
   ```
4. Повторно запустить скрипт — он создаст systemd-сервис и запустит бота:
   ```bash
   bash /tmp/deploy-bot.sh
   ```

### Обновление (после новых коммитов)
```bash
bash /tmp/deploy-bot.sh   # git reset --hard origin/master + restart
```

### Управление
```bash
systemctl status susanino-bot
systemctl restart susanino-bot
journalctl -u susanino-bot -f      # логи
```

### Данные
Бот читает `config.json/categories.json/objects.json` из `DATA_DIR`
(по умолчанию `/opt/susanino-map/data`). Источник истины — `web/src/data/*`;
синхронизация в корневой `data/` делается локально `python tools/sync_data.py`
перед коммитом. На сервер данные приезжают вместе с git-pull.
