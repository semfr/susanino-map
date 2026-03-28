'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { MapProvider } from '@/hooks/useMapObjects';
import BottomSheetWrapper from '@/components/map/BottomSheetWrapper';
import CategoryFilter from '@/components/map/CategoryFilter';

const MapContainer = dynamic(
  () => import('@/components/map/MapContainer'),
  { ssr: false, loading: () => <div className="h-screen w-screen bg-stone-100" /> }
);

export default function Home() {
  return (
    <MapProvider>
      <main className="h-screen w-screen relative">
        <MapContainer />
        <Link
          href="/catalog"
          className="absolute top-4 right-4 z-[500] flex items-center gap-1.5 px-4 py-2 bg-white/90 backdrop-blur-sm rounded-full text-sm font-medium text-stone-700 shadow-md hover:shadow-lg hover:bg-white transition-all duration-200"
        >
          <span>☰</span>
          <span>Список</span>
        </Link>
        <CategoryFilter />
        <BottomSheetWrapper />
      </main>
    </MapProvider>
  );
}
