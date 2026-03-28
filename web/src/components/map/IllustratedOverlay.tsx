'use client';

import { ImageOverlay } from 'react-leaflet';
import { config } from '@/config/region';

interface IllustratedOverlayProps {
  visible: boolean;
}

export default function IllustratedOverlay({ visible }: IllustratedOverlayProps) {
  if (!visible) return null;

  return (
    <ImageOverlay
      url={config.map.illustrationFile}
      bounds={config.map.illustrationBounds}
      opacity={0.85}
      zIndex={10}
    />
  );
}
