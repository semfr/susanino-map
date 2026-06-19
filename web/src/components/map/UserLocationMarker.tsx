'use client';

import { useEffect, useState } from 'react';
import { CircleMarker, Tooltip } from 'react-leaflet';

/**
 * Маркер «где я» — текущее положение пользователя по geolocation.
 * navigator трогаем ТОЛЬКО в useEffect (SSR-safe), watch очищаем в cleanup.
 */
export default function UserLocationMarker() {
  const [position, setPosition] = useState<[number, number] | null>(null);

  useEffect(() => {
    if (typeof navigator === 'undefined' || !navigator.geolocation) {
      return;
    }

    const watchId = navigator.geolocation.watchPosition(
      (pos) => {
        setPosition([pos.coords.latitude, pos.coords.longitude]);
      },
      (err) => {
        // Тихо игнорируем отказ/ошибку геолокации — маркер просто не появится.
        console.warn('Geolocation error:', err.message);
      },
      { enableHighAccuracy: true, maximumAge: 10000, timeout: 20000 }
    );

    return () => {
      navigator.geolocation.clearWatch(watchId);
    };
  }, []);

  if (!position) return null;

  return (
    <CircleMarker
      center={position}
      radius={8}
      pathOptions={{
        color: '#ffffff',
        weight: 3,
        fillColor: '#2563eb',
        fillOpacity: 1,
      }}
    >
      <Tooltip direction="top" offset={[0, -10]} opacity={0.95}>
        <span className="text-sm font-medium">Вы здесь</span>
      </Tooltip>
    </CircleMarker>
  );
}
