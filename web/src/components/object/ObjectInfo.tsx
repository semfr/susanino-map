'use client';

import type { MapObject } from '@/types';

interface ObjectInfoProps {
  object: MapObject;
}

export default function ObjectInfo({ object }: ObjectInfoProps) {
  const { contacts, schedule, pricing, address, externalLinks } = object;

  return (
    <div className="space-y-3 text-sm text-gray-700">
      {/* Address */}
      {address && (
        <div className="flex gap-2">
          <span className="shrink-0 text-gray-400">📍</span>
          <span>{address}</span>
        </div>
      )}

      {/* Phone */}
      {contacts.phone && (
        <div className="flex gap-2">
          <span className="shrink-0 text-gray-400">📞</span>
          <a
            href={`tel:${contacts.phone.replace(/\s/g, '')}`}
            className="text-blue-600 underline-offset-2 hover:underline"
          >
            {contacts.phone}
          </a>
        </div>
      )}

      {/* Website */}
      {contacts.website && (
        <div className="flex gap-2">
          <span className="shrink-0 text-gray-400">🌐</span>
          <a
            href={contacts.website}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 underline-offset-2 hover:underline break-all"
          >
            {contacts.website.replace(/^https?:\/\//, '')}
          </a>
        </div>
      )}

      {/* Schedule */}
      {(schedule.regular || schedule.days) && (
        <div className="flex gap-2">
          <span className="shrink-0 text-gray-400">🕐</span>
          <div>
            {schedule.regular && <div>{schedule.regular}</div>}
            {schedule.days && <div className="text-gray-500">{schedule.days}</div>}
            {schedule.exceptions && <div className="text-gray-500">{schedule.exceptions}</div>}
          </div>
        </div>
      )}

      {/* Pricing */}
      {(pricing.adult > 0 || pricing.child > 0 || pricing.notes) && (
        <div className="flex gap-2">
          <span className="shrink-0 text-gray-400">🎟</span>
          <div>
            {pricing.adult > 0 && (
              <div>Взрослый: {pricing.adult} {pricing.currency === 'RUB' ? '₽' : pricing.currency}</div>
            )}
            {pricing.child > 0 && (
              <div>Детский: {pricing.child} {pricing.currency === 'RUB' ? '₽' : pricing.currency}</div>
            )}
            {pricing.adult === 0 && pricing.child === 0 && !pricing.notes && (
              <div>Бесплатно</div>
            )}
            {pricing.notes && <div className="text-gray-500 text-xs mt-0.5">{pricing.notes}</div>}
          </div>
        </div>
      )}

      {/* Yandex Maps link */}
      {externalLinks.yandexMaps && (
        <div className="pt-1">
          <a
            href={externalLinks.yandexMaps}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 text-xs underline-offset-2 hover:underline"
          >
            Отзывы на Яндекс.Картах →
          </a>
        </div>
      )}
    </div>
  );
}
