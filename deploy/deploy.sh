#!/usr/bin/env bash
# УСТАРЕЛО — не использовать. Старый rsync-деплой выгружал на сервер всю папку bot/
# (включая секрет bot_api.txt) и предполагал свой веб-сервер.
# Теперь:
#   - веб задеплоен на GitHub Pages (.github/workflows/deploy.yml);
#   - бот деплоится на VPS из git без выгрузки секретов: deploy/deploy-bot.sh.
# Инструкция: deploy/README.md
echo "Этот скрипт устарел. Деплой бота: см. deploy/README.md (deploy/deploy-bot.sh на сервере)."
exit 1
