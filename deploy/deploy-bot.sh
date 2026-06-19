#!/usr/bin/env bash
# Боевой деплой Telegram-бота «Карта Сусанино» на VPS (Ubuntu/Debian).
# Запускать НА СЕРВЕРЕ от root. Идемпотентен: повторный запуск = обновление до свежего master.
# Секрет (BOT_TOKEN) НЕ берётся из репозитория — он должен лежать в /opt/susanino-map/bot/.env
# (см. шаг 5). Веб-часть деплоится отдельно на GitHub Pages, здесь только бот (polling, без nginx).
set -euo pipefail

REPO_URL="https://github.com/semfr/susanino-map.git"
APP_DIR="/opt/susanino-map"
SVC_USER="susanino"
SERVICE="susanino-bot"

echo "== 1/7 Системные пакеты =="
apt-get update -y
apt-get install -y python3 python3-venv python3-pip git

echo "== 2/7 Системный пользователь $SVC_USER =="
id -u "$SVC_USER" >/dev/null 2>&1 || useradd --system --create-home --shell /usr/sbin/nologin "$SVC_USER"

echo "== 3/7 Код (git clone/pull) =="
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" fetch --depth 1 origin master
  git -C "$APP_DIR" reset --hard origin/master
else
  git clone --depth 1 "$REPO_URL" "$APP_DIR"
fi

echo "== 4/7 venv + зависимости =="
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip --quiet
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/bot/requirements.txt" --quiet

echo "== 5/7 Секрет .env =="
if [ ! -f "$APP_DIR/bot/.env" ]; then
  echo "!! Нет $APP_DIR/bot/.env с BOT_TOKEN."
  echo "   Создай его и запусти скрипт снова, например:"
  echo "   cp $APP_DIR/bot/.env.example $APP_DIR/bot/.env && nano $APP_DIR/bot/.env"
  exit 1
fi
chmod 600 "$APP_DIR/bot/.env"

echo "== 6/7 Права =="
chown -R "$SVC_USER:$SVC_USER" "$APP_DIR"

echo "== 7/7 systemd =="
cp "$APP_DIR/deploy/susanino-bot.service" "/etc/systemd/system/$SERVICE.service"
systemctl daemon-reload
systemctl enable "$SERVICE" >/dev/null 2>&1 || true
systemctl restart "$SERVICE"
sleep 2
systemctl --no-pager status "$SERVICE" | head -12 || true
echo
echo "== Готово. Логи в реальном времени: journalctl -u $SERVICE -f =="
