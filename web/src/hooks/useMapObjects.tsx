'use client';

import { createContext, useContext, useState, useMemo, type ReactNode } from 'react';
import { objects, categories } from '@/config/region';
import type { MapObject, Category } from '@/types';

interface MapContextValue {
  allObjects: MapObject[];
  visibleObjects: MapObject[];
  categories: Category[];
  activeCategory: string | null;
  setActiveCategory: (id: string | null) => void;
  currentZoom: number;
  setCurrentZoom: (zoom: number) => void;
  selectedObject: MapObject | null;
  setSelectedObject: (obj: MapObject | null) => void;
}

const MapContext = createContext<MapContextValue | null>(null);

export function MapProvider({ children }: { children: ReactNode }) {
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [currentZoom, setCurrentZoom] = useState(11);
  const [selectedObject, setSelectedObject] = useState<MapObject | null>(null);

  const visibleObjects = useMemo(() => {
    return objects.filter((obj) => {
      if (obj.display.minZoom > currentZoom) return false;
      if (activeCategory && obj.categoryId !== activeCategory) return false;
      return true;
    });
  }, [activeCategory, currentZoom]);

  return (
    <MapContext.Provider value={{
      allObjects: objects, visibleObjects, categories,
      activeCategory, setActiveCategory,
      currentZoom, setCurrentZoom,
      selectedObject, setSelectedObject,
    }}>
      {children}
    </MapContext.Provider>
  );
}

export function useMapObjects() {
  const ctx = useContext(MapContext);
  if (!ctx) throw new Error('useMapObjects must be used within MapProvider');
  return ctx;
}
