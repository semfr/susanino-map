'use client';

import { useState } from 'react';
import {
  MapContainer as LeafletMapContainer,
  TileLayer,
  ImageOverlay,
  useMapEvents,
} from 'react-leaflet';
import L from 'leaflet';
import { config, getDefaultIllustration } from '@/config/region';
import { asset } from '@/lib/asset';
import { useMapObjects } from '@/hooks/useMapObjects';
import GeoMapLayer from './GeoMapLayer';
import UserLocationMarker from './UserLocationMarker';
import IllustratedMapLayer from './IllustratedMapLayer';
import MapModeSwitcher, { type MapMode } from './MapModeSwitcher';

/** Следит за зумом — только в гео-режиме (zoom-фильтр объектов). */
function ZoomWatcher() {
  const { setCurrentZoom } = useMapObjects();

  useMapEvents({
    zoomend: (e) => {
      setCurrentZoom(e.target.getZoom());
    },
  });

  return null;
}

export default function MapContainer() {
  const [mapMode, setMapMode] = useState<MapMode>('geo');
  const illustration = getDefaultIllustration();

  // Bounds лубка в CRS.Simple: [[minLat,minLng],[maxLat,maxLng]] = [[0,0],[H,W]].
  // Верх изображения = maxLat (см. anchorToLatLng — инверсия по вертикали).
  const illustrationBounds: [[number, number], [number, number]] = [
    [0, 0],
    [illustration.canvas.height, illustration.canvas.width],
  ];

  return (
    <div className="relative h-full w-full">
      {mapMode === 'geo' ? (
        <LeafletMapContainer
          key="geo"
          center={[config.center.lat, config.center.lng]}
          zoom={config.map.defaultZoom}
          minZoom={config.map.minZoom}
          maxZoom={config.map.maxZoom}
          className="h-full w-full"
          attributionControl={false}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <GeoMapLayer />
          <UserLocationMarker />
          <ZoomWatcher />
        </LeafletMapContainer>
      ) : (
        <LeafletMapContainer
          key="illustration"
          crs={L.CRS.Simple}
          bounds={illustrationBounds}
          maxBounds={illustrationBounds}
          minZoom={-3}
          maxZoom={2}
          className="h-full w-full"
          attributionControl={false}
        >
          <ImageOverlay
            url={asset(`/images/map/${illustration.file}`)}
            bounds={illustrationBounds}
          />
          <IllustratedMapLayer illustration={illustration} />
        </LeafletMapContainer>
      )}

      <MapModeSwitcher mode={mapMode} onChange={setMapMode} />
    </div>
  );
}
