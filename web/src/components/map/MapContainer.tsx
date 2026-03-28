'use client';

import { MapContainer as LeafletMapContainer, TileLayer, useMapEvents } from 'react-leaflet';
import { config } from '@/config/region';
import { useMapObjects } from '@/hooks/useMapObjects';
import ObjectMarker from './ObjectMarker';

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
  const { visibleObjects } = useMapObjects();

  return (
    <LeafletMapContainer
      center={[config.center.lat, config.center.lng]}
      zoom={config.map.defaultZoom}
      minZoom={config.map.minZoom}
      maxZoom={config.map.maxZoom}
      className="h-full w-full"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <ZoomWatcher />
      {visibleObjects.map((obj) => (
        <ObjectMarker key={obj.id} object={obj} />
      ))}
    </LeafletMapContainer>
  );
}
