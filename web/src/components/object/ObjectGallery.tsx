import type { Photo, Category } from '@/types';
import { asset } from '@/lib/asset';

interface ObjectGalleryProps {
  photos: Photo[];
  category?: Category;
  objectName: string;
}

export default function ObjectGallery({ photos, category, objectName }: ObjectGalleryProps) {
  const mainPhoto = photos.find((p) => p.isMain) ?? photos[0];
  const otherPhotos = photos.filter((p) => p !== mainPhoto);

  if (!mainPhoto) {
    return (
      <div className="flex items-center justify-center w-full h-48 bg-gray-100 rounded-xl text-5xl">
        {category?.emoji ?? '📍'}
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {/* Main photo */}
      <div className="relative w-full aspect-[4/3] rounded-xl overflow-hidden bg-gray-100">
        <img
          src={asset(mainPhoto.src)}
          alt={mainPhoto.alt || objectName}
          className="w-full h-full object-cover"
        />
      </div>

      {mainPhoto.attribution && (
        <p className="text-[11px] leading-tight text-gray-400">{mainPhoto.attribution}</p>
      )}

      {/* Thumbnails */}
      {otherPhotos.length > 0 && (
        <div className="flex gap-2 overflow-x-auto pb-1">
          {otherPhotos.map((photo, idx) => (
            <div
              key={idx}
              className="relative shrink-0 w-20 h-20 rounded-lg overflow-hidden bg-gray-100"
            >
              <img
                src={asset(photo.src)}
                alt={photo.alt || `${objectName} — фото ${idx + 2}`}
                className="w-full h-full object-cover"
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
