import { describe, it, expect } from 'vitest';
import { resolveInitialMapMode } from '@/lib/mapMode';
import type { Illustration } from '@/types';

const ill = (over: Partial<Illustration> = {}): Illustration => ({
  id: 'guide',
  title: 'Лубок',
  file: 'x.webp',
  canvas: { width: 100, height: 100 },
  anchors: [],
  ...over,
});

describe('resolveInitialMapMode', () => {
  it('старт = лубок, когда есть иллюстрация по умолчанию', () => {
    expect(resolveInitialMapMode(ill())).toBe('illustration');
  });

  it('старт = навигатор, когда иллюстрации нет', () => {
    expect(resolveInitialMapMode(undefined)).toBe('geo');
  });
});
