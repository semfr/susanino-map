// Deep-link сайт → Telegram-бот по объекту.
// Контракт: https://t.me/<bot>?start=obj_<objectId>
// Бот в /start разбирает payload obj_<id> и сразу открывает карточку объекта.

/** Username бота (без @). Совпадает с BOT_USERNAME в конфиге бота. */
export const BOT_USERNAME = 'susanino_map_bot';

/**
 * Строит deep-link в Telegram-бота для конкретного объекта.
 * id объекта кладётся в start-payload с префиксом obj_ и URL-экранируется
 * (на случай небезопасных символов; боевые id вида susanino-museum проходят как есть).
 */
export function botDeepLink(objectId: string): string {
  const payload = `obj_${encodeURIComponent(objectId)}`;
  return `https://t.me/${BOT_USERNAME}?start=${payload}`;
}
