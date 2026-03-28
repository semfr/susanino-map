import Link from 'next/link';
import type { MapObject, Category } from '@/types';

interface CatalogItemProps {
  object: MapObject;
  category: Category | undefined;
}

export default function CatalogItem({ object, category }: CatalogItemProps) {
  return (
    <Link
      href={`/object/${object.slug}`}
      className="flex items-start gap-3 p-4 bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200 hover:-translate-y-0.5"
    >
      <div
        className="w-10 h-10 rounded-lg flex items-center justify-center text-xl flex-shrink-0"
        style={{ backgroundColor: category ? `${category.color}20` : '#f5f5f4' }}
      >
        {category?.emoji ?? '📍'}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <h3 className="font-semibold text-stone-900 truncate">{object.name}</h3>
          {category && (
            <span
              className="text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0"
              style={{
                backgroundColor: `${category.color}20`,
                color: category.color,
              }}
            >
              {category.name}
            </span>
          )}
        </div>
        {object.description && (
          <p className="text-sm text-stone-500 line-clamp-2">{object.description}</p>
        )}
      </div>
      <span className="text-stone-300 flex-shrink-0 mt-1">›</span>
    </Link>
  );
}
