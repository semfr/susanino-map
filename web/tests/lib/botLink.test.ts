import { describe, it, expect } from 'vitest';
import { botDeepLink, BOT_USERNAME } from '@/lib/botLink';

describe('botDeepLink — deep-link сайт → Telegram-бот', () => {
  it('username бота — susanino_map_bot', () => {
    expect(BOT_USERNAME).toBe('susanino_map_bot');
  });

  it('строит ссылку формата https://t.me/<bot>?start=obj_<id>', () => {
    expect(botDeepLink('susanino-museum')).toBe(
      'https://t.me/susanino_map_bot?start=obj_susanino-museum',
    );
  });

  it('сохраняет дефисы в id (start-payload их допускает)', () => {
    expect(botDeepLink('a-b-c')).toBe('https://t.me/susanino_map_bot?start=obj_a-b-c');
  });

  it('использует BOT_USERNAME в домене ссылки', () => {
    expect(botDeepLink('x')).toContain(`https://t.me/${BOT_USERNAME}?start=`);
  });

  it('экранирует небезопасные для URL символы в id', () => {
    // пробелы и спецсимволы не должны попасть в URL сырыми
    expect(botDeepLink('a b')).toBe('https://t.me/susanino_map_bot?start=obj_a%20b');
    expect(botDeepLink('a&b=c')).toBe('https://t.me/susanino_map_bot?start=obj_a%26b%3Dc');
  });

  it('всегда возвращает префикс obj_ в payload', () => {
    expect(botDeepLink('museum')).toContain('start=obj_');
  });
});
