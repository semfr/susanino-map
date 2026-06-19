'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { MapProvider } from '@/hooks/useMapObjects';
import CategoryFilter from '@/components/map/CategoryFilter';
import BottomSheetWrapper from '@/components/map/BottomSheetWrapper';

// Leaflet тянет browser-only API (window), поэтому только на клиенте.
const MapView = dynamic(() => import('@/components/map/MapContainer'), {
  ssr: false,
  loading: () => (
    <div className="h-full w-full bg-stone-100 flex items-center justify-center text-stone-400">
      Загрузка карты...
    </div>
  ),
});

export default function Home() {
  return (
    <MapProvider>
      <main className="h-screen w-screen relative">
        <MapView />
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
