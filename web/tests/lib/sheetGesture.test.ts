import { describe, it, expect } from 'vitest';
import { clampSheetOffset, shouldDismissSheet } from '@/lib/sheetGesture';

describe('clampSheetOffset', () => {
  it('тянем вниз — смещение сохраняется', () => {
    expect(clampSheetOffset(120)).toBe(120);
  });

  it('тянем вверх — лист не уезжает выше нуля', () => {
    expect(clampSheetOffset(-80)).toBe(0);
  });
});

describe('shouldDismissSheet', () => {
  it('закрываем при сдвиге больше порога', () => {
    expect(shouldDismissSheet({ deltaY: 140 })).toBe(true);
  });

  it('не закрываем при малом сдвиге', () => {
    expect(shouldDismissSheet({ deltaY: 40 })).toBe(false);
  });

  it('закрываем при резком флике вниз даже с небольшим сдвигом', () => {
    expect(shouldDismissSheet({ deltaY: 50, velocity: 1.2 })).toBe(true);
  });

  it('флик вверх не закрывает', () => {
    expect(shouldDismissSheet({ deltaY: 50, velocity: -1.2 })).toBe(false);
  });
});
