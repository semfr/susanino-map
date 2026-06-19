import { describe, it, expect } from 'vitest';
import { validateMapData } from '@/lib/dataValidator';

// Маленькие инлайн-фикстуры под реальные json-формы.
// config: bounds = [[minLat, minLng], [maxLat, maxLng]]
const config = {
  bounds: [
    [58.0, 41.0],
    [59.0, 42.0],
  ] as [[number, number], [number, number]],
};

function makeObject(id: string, lat: number | undefined, lng: number | undefined) {
  return {
    id,
    coordinates: { real: { lat, lng } as { lat?: number; lng?: number } },
  };
}

const validObjects = [
  makeObject('obj-1', 58.5, 41.5),
  makeObject('obj-2', 58.2, 41.8),
];

function makeIllustration(anchors: Array<{ objectId: string; x: number; y: number }>) {
  return {
    canvas: { width: 1000, height: 800 },
    anchors,
  };
}

const validIllustration = makeIllustration([
  { objectId: 'obj-1', x: 100, y: 200 },
  { objectId: 'obj-2', x: 900, y: 700 },
]);

describe('validateMapData', () => {
  it('валидный набор -> isValid true, errors пуст', () => {
    const result = validateMapData(config, validObjects, validIllustration);
    expect(result.isValid).toBe(true);
    expect(result.errors).toEqual([]);
  });

  it('битый anchor.objectId -> isValid false, в errors упомянут objectId', () => {
    const illustration = makeIllustration([
      { objectId: 'obj-1', x: 100, y: 200 },
      { objectId: 'no-such-object', x: 300, y: 400 },
    ]);
    const result = validateMapData(config, validObjects, illustration);
    expect(result.isValid).toBe(false);
    expect(result.errors.some((e) => e.includes('no-such-object'))).toBe(true);
  });

  it('объект вне bounds -> false', () => {
    const objects = [
      makeObject('obj-1', 58.5, 41.5),
      makeObject('obj-2', 60.5, 41.8), // lat > maxLat
    ];
    const illustration = makeIllustration([
      { objectId: 'obj-1', x: 100, y: 200 },
      { objectId: 'obj-2', x: 900, y: 700 },
    ]);
    const result = validateMapData(config, objects, illustration);
    expect(result.isValid).toBe(false);
  });

  it('объект без lng -> false', () => {
    const objects = [
      makeObject('obj-1', 58.5, 41.5),
      makeObject('obj-2', 58.2, undefined), // нет lng
    ];
    const illustration = makeIllustration([
      { objectId: 'obj-1', x: 100, y: 200 },
      { objectId: 'obj-2', x: 900, y: 700 },
    ]);
    const result = validateMapData(config, objects, illustration);
    expect(result.isValid).toBe(false);
  });

  it('anchor с x за пределами canvas.width -> false', () => {
    const illustration = makeIllustration([
      { objectId: 'obj-1', x: 100, y: 200 },
      { objectId: 'obj-2', x: 1200, y: 700 }, // x > canvas.width (1000)
    ]);
    const result = validateMapData(config, validObjects, illustration);
    expect(result.isValid).toBe(false);
  });
});
