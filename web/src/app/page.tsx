'use client';

import dynamic from 'next/dynamic';
import { MapProvider } from '@/hooks/useMapObjects';

const MapContainer = dynamic(
  () => import('@/components/map/MapContainer'),
  { ssr: false, loading: () => <div className="h-screen w-screen bg-stone-100" /> }
);

export default function Home() {
  return (
    <MapProvider>
      <main className="h-screen w-screen">
        <MapContainer />
      </main>
    </MapProvider>
  );
}
