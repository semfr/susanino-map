'use client';

import { getYandexMapsRouteUrl } from '@/lib/navigation';
import type { MapObject } from '@/types';

interface NavigateButtonProps {
  object: MapObject;
}

export default function NavigateButton({ object }: NavigateButtonProps) {
  const { lat, lng } = object.coordinates.real;
  const url = getYandexMapsRouteUrl(lat, lng, object.name);

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center justify-center gap-2 w-full py-3.5 px-4 rounded-xl bg-blue-600 text-white font-semibold text-base active:bg-blue-700 transition-colors"
    >
      <span>🗺</span>
      <span>Построить маршрут</span>
    </a>
  );
}
