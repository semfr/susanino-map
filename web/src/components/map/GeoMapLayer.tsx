'use client';

import { useMapObjects } from '@/hooks/useMapObjects';
import ObjectMarker from './ObjectMarker';

/**
 * Гео-слой: набор маркеров видимых объектов (GPS) внутри карты.
 * Не имеет собственного MapContainer — рендерится как дети <LeafletMapContainer>.
 */
export default function GeoMapLayer() {
  const { visibleObjects } = useMapObjects();

  return (
    <>
      {visibleObjects.map((obj) => (
        <ObjectMarker key={obj.id} object={obj} />
      ))}
    </>
  );
}
