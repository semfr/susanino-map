'use client';

import { asset } from '@/lib/asset';
import { useMapObjects } from '@/hooks/useMapObjects';
import ObjectInfo from './ObjectInfo';
import NavigateButton from './NavigateButton';
import type { MapObject } from '@/types';

interface ObjectCardProps {
  object: MapObject;
}

export default function ObjectCard({ object }: ObjectCardProps) {
  const { categories } = useMapObjects();
  const category = categories.find((c) => c.id === object.categoryId);

  const mainPhoto = object.photos.find((p) => p.isMain) ?? object.photos[0];

  return (
    <div className="flex flex-col gap-4">
      {/* Photo */}
      <div className="relative w-full h-48 rounded-xl overflow-hidden bg-gray-100 shrink-0">
        {mainPhoto ? (
          <img
            src={asset(mainPhoto.src)}
            alt={mainPhoto.alt}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="flex items-center justify-center h-full text-4xl text-gray-300">
            {category?.emoji ?? '📍'}
          </div>
        )}
      </div>

      {mainPhoto?.attribution && (
        <p className="-mt-2 text-[11px] leading-tight text-gray-400">{mainPhoto.attribution}</p>
      )}

      {/* Header */}
      <div className="flex flex-col gap-1.5">
        {/* Category badge */}
        {category && (
          <span
            className="inline-flex self-start items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white"
            style={{ backgroundColor: category.color }}
          >
            {category.emoji} {category.name}
          </span>
        )}

        {/* Name */}
        <h2 className="text-xl font-bold text-gray-900 leading-tight">{object.name}</h2>

        {/* Short description */}
        {object.description && (
          <p className="text-sm text-gray-600 leading-relaxed">{object.description}</p>
        )}
      </div>

      {/* Info block */}
      <ObjectInfo object={object} />

      {/* Navigate button */}
      <NavigateButton object={object} />
    </div>
  );
}
