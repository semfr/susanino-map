import Link from 'next/link';
import { categories, objects, config } from '@/config/region';
import CatalogList from '@/components/catalog/CatalogList';

export const metadata = {
  title: `Все места — ${config.name}`,
  description: `Полный список достопримечательностей и мест интереса в ${config.fullName}.`,
};

export default function CatalogPage() {
  return (
    <div className="min-h-screen bg-stone-50">
      {/* Header */}
      <header className="sticky top-0 z-10 bg-white/90 backdrop-blur-sm border-b border-stone-100 shadow-sm">
        <div className="max-w-2xl mx-auto px-4 py-3 flex items-center gap-3">
          <Link
            href="/"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium text-stone-600 bg-stone-100 hover:bg-stone-200 transition-colors"
          >
            <span>🗺</span>
            <span>Карта</span>
          </Link>
          <h1 className="text-lg font-bold text-stone-900 flex-1">{config.name}</h1>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-2xl mx-auto px-4 py-5">
        <CatalogList objects={objects} categories={categories} />
      </main>
    </div>
  );
}
