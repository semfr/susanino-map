'use client';

import { useMapObjects } from '@/hooks/useMapObjects';

export default function CategoryFilter() {
  const { categories, activeCategory, setActiveCategory } = useMapObjects();

  const handleChipClick = (categoryId: string) => {
    if (activeCategory === categoryId) {
      setActiveCategory(null);
    } else {
      setActiveCategory(categoryId);
    }
  };

  return (
    <div className="absolute bottom-0 left-0 right-0 z-[400] pb-2 pt-2 px-3 bg-white/70 backdrop-blur-sm">
      <div className="flex gap-2 overflow-x-auto scrollbar-hide">
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
                    ? 'text-white shadow-md scale-105'
                    : 'bg-white text-stone-700 shadow-sm hover:shadow-md hover:scale-105'
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
    </div>
  );
}
