// Single-source данных карты.
// Канон — корневой каталог ../data (его читает бот и правит админка через бота).
// web/src/data — генерируемое зеркало для статической сборки Next.js; редактировать вручную НЕ нужно.
// Скрипт зеркалит канон перед dev и build (хуки predev/prebuild в package.json).
import { cp, rm, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(here, '../../data'); // канон: <repo>/data
const DST = resolve(here, '../src/data'); // зеркало: <repo>/web/src/data

if (!existsSync(SRC)) {
  console.error(`[sync-data] нет каталога-источника: ${SRC}`);
  process.exit(1);
}

await rm(DST, { recursive: true, force: true });
await mkdir(DST, { recursive: true });
await cp(SRC, DST, { recursive: true });
console.log(`[sync-data] ${SRC} -> ${DST}`);
