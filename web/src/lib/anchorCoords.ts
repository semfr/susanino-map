/**
 * Преобразование пиксельного якоря иллюстрации в координату Leaflet CRS.Simple.
 *
 * Якорь {x, y} задан в системе изображения: origin — верхний-левый угол холста,
 * y растёт ВНИЗ. Карта лубка строится на bounds [[0,0],[H,W]] (CRS.Simple), где
 * верх изображения соответствует МАКСИМАЛЬНОЙ широте (ImageOverlay рисует холст
 * так, что его верхний край = north). Поэтому по вертикали нужна инверсия:
 *   lat = canvasHeight - y,  lng = x.
 * Иначе маркеры окажутся зеркально отражёнными относительно растра.
 */
export function anchorToLatLng(
  a: { x: number; y: number },
  canvasHeight: number,
): [number, number] {
  return [canvasHeight - a.y, a.x];
}

/** Обратное преобразование (для отладки кликов по карте). */
export function latLngToAnchor(
  p: [number, number],
  canvasHeight: number,
): { x: number; y: number } {
  return { x: p[1], y: canvasHeight - p[0] };
}
