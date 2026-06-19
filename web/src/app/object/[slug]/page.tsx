import type { Metadata } from 'next';
import Link from 'next/link';
import { objects, categories, config } from '@/config/region';
import type { MapObject, Category } from '@/types';
import ObjectGallery from '@/components/object/ObjectGallery';
import ObjectInfo from '@/components/object/ObjectInfo';
import NavigateButton from '@/components/object/NavigateButton';
import ShareButton from '@/components/object/ShareButton';
import TelegramBotButton from '@/components/object/TelegramBotButton';

interface PageProps {
  params: Promise<{ slug: string }>;
}

function findObject(slug: string): MapObject | undefined {
  return objects.find((o) => o.slug === slug);
}

function findCategory(categoryId: string): Category | undefined {
  return categories.find((c) => c.id === categoryId);
}

export async function generateStaticParams() {
  return objects.map((obj) => ({ slug: obj.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const obj = findObject(slug);

  if (!obj) {
    return { title: 'Объект не найден' };
  }

  const category = findCategory(obj.categoryId);
  const mainPhoto = obj.photos.find((p) => p.isMain) ?? obj.photos[0];
  const ogImage = mainPhoto?.src ?? config.seo.ogImage;

  return {
    title: `${obj.name} — ${config.name}`,
    description: obj.description,
    openGraph: {
      title: obj.name,
      description: obj.description,
      images: [{ url: ogImage, alt: obj.name }],
      locale: 'ru_RU',
      type: 'article',
    },
    other: {
      'og:site_name': config.name,
    },
  };
}

export default async function ObjectPage({ params }: PageProps) {
  const { slug } = await params;
  const obj = findObject(slug);

  if (!obj) {
    return (
      <main className="min-h-screen flex items-center justify-center p-4">
        <div className="text-center">
          <p className="text-xl text-gray-500">Объект не найден</p>
          <Link href="/" className="mt-4 inline-block text-blue-600 underline">
            На карту
          </Link>
        </div>
      </main>
    );
  }

  const category = findCategory(obj.categoryId);

  return (
    <main className="min-h-screen bg-white">
      <div className="max-w-2xl mx-auto px-4 py-6 space-y-6">

        {/* Back link */}
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800"
        >
          ← На карту
        </Link>

        {/* Header */}
        <div className="space-y-2">
          {category && (
            <span
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium text-white"
              style={{ backgroundColor: category.color }}
            >
              <span>{category.emoji}</span>
              <span>{category.name}</span>
            </span>
          )}
          <h1 className="text-2xl font-bold text-gray-900 leading-tight">
            {obj.name}
          </h1>
          <p className="text-gray-600">{obj.description}</p>
        </div>

        {/* Gallery */}
        <ObjectGallery
          photos={obj.photos}
          category={category}
          objectName={obj.name}
        />

        {/* Full description */}
        {obj.fullDescription && (
          <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed">
            <p>{obj.fullDescription}</p>
          </div>
        )}

        {/* Info block */}
        <ObjectInfo object={obj} />

        {/* Actions */}
        <div className="space-y-3 pt-2">
          <NavigateButton object={obj} />

          <TelegramBotButton objectId={obj.id} className="w-full" />

          <div className="flex gap-3">
            <Link
              href={`/?focus=${obj.slug}`}
              className="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl border border-gray-200 text-gray-700 font-medium text-sm hover:bg-gray-50 transition-colors"
            >
              <span>🗺</span>
              <span>На карте</span>
            </Link>

            <ShareButton className="flex-1" />
          </div>
        </div>

      </div>
    </main>
  );
}
