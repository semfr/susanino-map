'use client';

import { useMemo } from 'react';
import { CircleMarker, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import { useMapObjects } from '@/hooks/useMapObjects';
import type { MapObject } from '@/types';

interface ObjectMarkerProps {
  object: MapObject;
}

export default function ObjectMarker({ object }: ObjectMarkerProps) {
  const { categories, setSelectedObject } = useMapObjects();

  const category = useMemo(
    () => categories.find((c) => c.id === object.categoryId),
    [categories, object.categoryId]
  );

  const color = category?.color ?? '#666666';

  return (
    <CircleMarker
      center={[object.coordinates.real.lat, object.coordinates.real.lng]}
      radius={10}
      pathOptions={{
        color: '#ffffff',
        weight: 2,
        fillColor: color,
        fillOpacity: 0.9,
      }}
      eventHandlers={{
        click: () => {
          console.log('Marker clicked:', object.name);
          setSelectedObject(object);
        },
      }}
    >
      <Tooltip direction="top" offset={[0, -12]} opacity={0.95}>
        <span className="text-sm font-medium">{object.shortName || object.name}</span>
      </Tooltip>
    </CircleMarker>
  );
}
