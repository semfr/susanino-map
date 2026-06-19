import type { Illustration } from '@/types';

/** Режимы карты: навигатор (geo, OSM+GPS) и лубок (illustration). */
export type MapMode = 'geo' | 'illustration';

/**
 * Стартовый режим карты.
 * Лубок — узнаваемое ядро продукта, поэтому при наличии иллюстрации по умолчанию
 * приложение открывается именно в нём; если иллюстраций нет — fallback на навигатор.
 */
export function resolveInitialMapMode(
  defaultIllustration: Illustration | undefined,
): MapMode {
  return defaultIllustration ? 'illustration' : 'geo';
}
