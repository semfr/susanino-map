import type { RegionConfig } from '@/types';

/**
 * Результат валидации данных карты.
 */
export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

// Мягкие структурные входные типы: валидатор принимает как реальные
// RegionConfig / MapObject[] / Illustration, так и частичные данные и проверяет
// только нужные ему поля. bounds типизирован строго (используется при разборе).
type ConfigInput = { bounds: RegionConfig['bounds'] };

type ObjectInput = {
  id?: string;
  coordinates?: { real?: { lat?: number; lng?: number } };
};

type AnchorInput = { objectId?: string; x?: number; y?: number };

type IllustrationInput = {
  canvas?: { width?: number; height?: number };
  anchors?: AnchorInput[];
};

/**
 * Валидирует согласованность данных карты: связи anchor->object, попадание
 * координат объектов в bounds и нахождение anchor-точек внутри canvas.
 *
 * @param config        конфиг региона (используется поле bounds = [[minLat,minLng],[maxLat,maxLng]])
 * @param objects       массив объектов карты
 * @param illustration  иллюстрация с canvas и anchors
 */
export function validateMapData(
  config: ConfigInput,
  objects: ObjectInput[],
  illustration: IllustrationInput,
): ValidationResult {
  const errors: string[] = [];

  const objectList = Array.isArray(objects) ? objects : [];
  const anchors = Array.isArray(illustration?.anchors) ? illustration.anchors : [];

  // Множество id известных объектов.
  const objectIds = new Set(objectList.map((o) => o?.id));

  // --- Проверка 1: каждый anchor.objectId есть среди objects ---
  for (const anchor of anchors) {
    const objectId = anchor?.objectId;
    if (!objectIds.has(objectId)) {
      errors.push(
        `Якорь ссылается на несуществующий objectId: "${objectId}"`,
      );
    }
  }

  // --- Проверка 2: координаты объекта внутри bounds ---
  const bounds = config?.bounds;
  const hasBounds =
    Array.isArray(bounds) &&
    Array.isArray(bounds[0]) &&
    Array.isArray(bounds[1]) &&
    bounds[0].length === 2 &&
    bounds[1].length === 2;

  if (!hasBounds) {
    errors.push('Некорректные bounds в config.');
  } else {
    const [[minLat, minLng], [maxLat, maxLng]] = bounds;
    for (const obj of objectList) {
      const real = obj?.coordinates?.real;
      const lat = real?.lat;
      const lng = real?.lng;

      if (typeof lat !== 'number' || Number.isNaN(lat)) {
        errors.push(`Объект "${obj?.id}": отсутствует или некорректна координата lat.`);
        continue;
      }
      if (typeof lng !== 'number' || Number.isNaN(lng)) {
        errors.push(`Объект "${obj?.id}": отсутствует или некорректна координата lng.`);
        continue;
      }
      if (lat < minLat || lat > maxLat || lng < minLng || lng > maxLng) {
        errors.push(
          `Объект "${obj?.id}": координаты (${lat}, ${lng}) вне границ карты.`,
        );
      }
    }
  }

  // --- Проверка 3: canvas > 0 и каждый anchor внутри canvas ---
  const width = illustration?.canvas?.width;
  const height = illustration?.canvas?.height;

  const validWidth = typeof width === 'number' && width > 0;
  const validHeight = typeof height === 'number' && height > 0;

  if (!validWidth || !validHeight) {
    errors.push('Иллюстрация: canvas.width/height должны быть больше 0.');
  } else {
    for (const anchor of anchors) {
      const x = anchor?.x;
      const y = anchor?.y;
      if (typeof x !== 'number' || x < 0 || x > width) {
        errors.push(
          `Якорь "${anchor?.objectId}": x=${x} вне диапазона [0, ${width}].`,
        );
      }
      if (typeof y !== 'number' || y < 0 || y > height) {
        errors.push(
          `Якорь "${anchor?.objectId}": y=${y} вне диапазона [0, ${height}].`,
        );
      }
    }
  }

  return { isValid: errors.length === 0, errors };
}
