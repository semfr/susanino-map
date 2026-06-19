'use client';

import { Marker, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import { anchorToLatLng } from '@/lib/anchorCoords';
import { objects } from '@/config/region';
import { useMapObjects } from '@/hooks/useMapObjects';
import type { Illustration } from '@/types';

interface IllustratedMapLayerProps {
  illustration: Illustration;
}

/**
 * Лубок-слой: для каждого якоря рисуем числовой badge на холсте CRS.Simple.
 * Позиция якоря: anchorToLatLng({x,y}) — инвариант {x,y} -> L.latLng(y, x).
 * Клик по бейджу выбирает соответствующий объект.
 * Если объект по anchor.objectId не найден — пропускаем (не падаем).
 */
function makeBadgeIcon(badge: number): L.DivIcon {
  return L.divIcon({
    className: 'lubok-badge',
    html: `<span style="display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:9999px;background:#b91c1c;color:#fff;font-weight:700;font-size:14px;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.4);">${badge}</span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

export default function IllustratedMapLayer({ illustration }: IllustratedMapLayerProps) {
  const { setSelectedObject } = useMapObjects();

  return (
    <>
      {illustration.anchors.map((anchor) => {
        const obj = objects.find((o) => o.id === anchor.objectId);
        if (!obj) return null;

        const position = anchorToLatLng(
          { x: anchor.x, y: anchor.y },
          illustration.canvas.height,
        );

        return (
          <Marker
            key={anchor.objectId}
            position={position}
            icon={makeBadgeIcon(anchor.badge)}
            eventHandlers={{
              click: () => {
                setSelectedObject(obj);
              },
            }}
          >
            <Tooltip direction="top" offset={[0, -14]} opacity={0.95}>
              <span className="text-sm font-medium">{obj.shortName || obj.name}</span>
            </Tooltip>
          </Marker>
        );
      })}
    </>
  );
}
