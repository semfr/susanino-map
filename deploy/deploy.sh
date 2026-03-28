#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "=== Building web ==="
cd web && npm run build && cd ..
echo "=== Deploying to VPS ==="
rsync -avz --delete web/out/ user@vps:/var/www/susanino-map/
rsync -avz data/ user@vps:/opt/susanino-data/
rsync -avz bot/ user@vps:/opt/susanino-bot/
echo "=== Restarting bot ==="
ssh user@vps "systemctl restart susanino-bot"
echo "=== Done! ==="
