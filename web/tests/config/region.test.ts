import { describe, it, expect } from 'vitest';
import { config, objects, getDefaultIllustration } from '@/config/region';
import { validateMapData } from '@/lib/dataValidator';

describe('region config — иллюстрации (боевые данные)', () => {
  it('иллюстрация по умолчанию — guide-susanino', () => {
    expect(getDefaultIllustration().id).toBe('guide-susanino');
  });

  it('у иллюстрации по умолчанию 8 якорей', () => {
    expect(getDefaultIllustration().anchors.length).toBe(8);
  });

  it('каждый anchor.objectId присутствует среди objects', () => {
    const objectIds = new Set(objects.map((o) => o.id));
    for (const anchor of getDefaultIllustration().anchors) {
      expect(objectIds.has(anchor.objectId)).toBe(true);
    }
  });

  it('validateMapData проходит на боевых данных', () => {
    const result = validateMapData(config, objects, getDefaultIllustration());
    expect(result.isValid).toBe(true);
  });
});
