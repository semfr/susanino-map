'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { MapProvider } from '@/hooks/useMapObjects';
import CategoryFilter from '@/components/map/CategoryFilter';
import BottomSheetWrapper from '@/components/map/BottomSheetWrapper';

export default function Home() {
  const [MapComponent, setMapComponent] = useState<React.ComponentType | null>(null);

  useEffect(() => {
    import('@/components/map/MapContainer')
      .then((mod) => setMapComponent(() => mod.default))
      .catch((err) => console.error('Failed to load map:', err));
  }, []);

  return (
    <MapProvider>
      <main className="h-screen w-screen relative">
        {MapComponent ? (
          <MapComponent />
        ) : (
          <div className="h-full w-full bg-stone-100 flex items-center justify-center text-stone-400">
            Загрузка карты...
          </div>
        )}
        <Link
          href="/catalog"
          className="absolute top-4 right-4 z-[500] flex items-center gap-1.5 px-4 py-2 bg-white/90 backdrop-blur-sm rounded-full text-sm font-medium text-stone-700 shadow-md"
        >
          <span>☰ Список</span>
        </Link>
        <CategoryFilter />
        <BottomSheetWrapper />
      </main>
    </MapProvider>
  );
}
