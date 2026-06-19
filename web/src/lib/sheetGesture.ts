export interface DismissInput {
  /** Сдвиг по вертикали от начала жеста, px. Вниз — положительно. */
  deltaY: number;
  /** Скорость в момент отпускания, px/ms. Вниз — положительно. */
  velocity?: number;
}

/** Порог закрытия по расстоянию, px. */
export const DISMISS_DISTANCE = 100;
/** Порог закрытия по скорости (флик), px/ms. */
export const DISMISS_VELOCITY = 0.6;

/** Смещение листа при перетаскивании: тянем только вниз, вверх не уезжает. */
export function clampSheetOffset(deltaY: number): number {
  return deltaY > 0 ? deltaY : 0;
}

/** Закрывать ли лист по завершении жеста (по расстоянию ИЛИ по флику вниз). */
export function shouldDismissSheet({ deltaY, velocity = 0 }: DismissInput): boolean {
  if (velocity <= -DISMISS_VELOCITY) return false; // явный флик вверх — оставляем открытым
  if (velocity >= DISMISS_VELOCITY && deltaY > 0) return true; // резкий флик вниз
  return deltaY >= DISMISS_DISTANCE; // медленный, но достаточный сдвиг
}
