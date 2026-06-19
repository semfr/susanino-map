import { describe, it, expect } from 'vitest';
import { anchorToLatLng, latLngToAnchor } from '@/lib/anchorCoords';

// Высота холста лубка guide_susanino (2520×2560).
const H = 2560;

describe('anchorCoords', () => {
  it('инвертирует вертикаль: {x,y} -> [H - y, x]', () => {
    expect(anchorToLatLng({ x: 988, y: 1132 }, H)).toEqual([H - 1132, 988]);
  });

  it('верхний-левый пиксель {0,0} -> северо-западный угол [H, 0]', () => {
    expect(anchorToLatLng({ x: 0, y: 0 }, H)).toEqual([H, 0]);
  });

  it('нижний-правый край {2520,2560} -> юго-восточный угол [0, 2520]', () => {
    expect(anchorToLatLng({ x: 2520, y: 2560 }, H)).toEqual([0, 2520]);
  });

  it('round-trip latLngToAnchor(anchorToLatLng(a)) === a', () => {
    expect(latLngToAnchor(anchorToLatLng({ x: 988, y: 1132 }, H), H)).toEqual({
      x: 988,
      y: 1132,
    });
  });
});
