'use client';

import { useState } from 'react';
import { MapContainer as LeafletMapContainer, TileLayer, useMapEvents } from 'react-leaflet';
import { config } from '@/config/region';
import { useMapObjects } from '@/hooks/useMapObjects';
import ObjectMarker from './ObjectMarker';
import IllustratedOverlay from './IllustratedOverlay';
import MapControls from './MapControls';

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
  const [layerMode, setLayerMode] = useState<'map' | 'illustration'>('map');

  const toggleLayer = () => {
    setLayerMode((prev) => (prev === 'map' ? 'illustration' : 'map'));
  };

  return (
    <div className="relative h-full w-full">
      <LeafletMapContainer
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
          opacity={layerMode === 'illustration' ? 0.3 : 1}
        />
        <IllustratedOverlay visible={layerMode === 'illustration'} />
        <ZoomWatcher />
        {visibleObjects.map((obj) => (
          <ObjectMarker key={obj.id} object={obj} />
        ))}
      </LeafletMapContainer>

      <MapControls mode={layerMode} onToggle={toggleLayer} />
    </div>
  );
}
