'use client';

import { useState } from 'react';
import type { MapObject, Category } from '@/types';
import CatalogItem from './CatalogItem';

interface CatalogListProps {
  objects: MapObject[];
  categories: Category[];
}

export default function CatalogList({ objects, categories }: CatalogListProps) {
  const [activeCategory, setActiveCategory] = useState<string | null>(null);

  const handleChipClick = (categoryId: string) => {
    setActiveCategory(activeCategory === categoryId ? null : categoryId);
  };

  const filteredObjects = activeCategory
    ? objects.filter((obj) => obj.categoryId === activeCategory)
    : objects;

  const sortedObjects = filteredObjects
    .slice()
    .sort((a, b) => b.display.priority - a.display.priority);

  const getCategoryById = (id: string) => categories.find((c) => c.id === id);

  return (
    <div>
      {/* Category filter chips */}
      <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-1 mb-4">
        {categories
          .slice()
          .sort((a, b) => a.sortOrder - b.sortOrder)
          .map((category) => {
            const isActive = activeCategory === category.id;
            return (
              <button
                key={category.id}
                onClick={() => handleChipClick(category.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-all duration-200 flex-shrink-0 ${
                  isActive
                    ? 'text-white shadow-md'
                    : 'bg-white text-stone-700 shadow-sm hover:shadow-md'
                }`}
                style={isActive ? { backgroundColor: category.color } : {}}
              >
                <span
                  className="w-2 h-2 rounded-full flex-shrink-0"
                  style={{ backgroundColor: category.color }}
                />
                <span>{category.name}</span>
              </button>
            );
          })}
      </div>

      {/* Objects count */}
      <p className="text-sm text-stone-400 mb-3">
        {sortedObjects.length}{' '}
        {sortedObjects.length === 1 ? 'место' : sortedObjects.length < 5 ? 'места' : 'мест'}
      </p>

      {/* Objects list */}
      <div className="flex flex-col gap-3">
        {sortedObjects.map((object) => (
          <CatalogItem
            key={object.id}
            object={object}
            category={getCategoryById(object.categoryId)}
          />
        ))}
      </div>
    </div>
  );
}
