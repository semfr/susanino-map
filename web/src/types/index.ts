export interface Coordinates {
  lat: number;
  lng: number;
}

export interface MapConfig {
  illustrationFile: string;
  illustrationBounds: [[number, number], [number, number]];
  defaultZoom: number;
  minZoom: number;
  maxZoom: number;
}

export interface SeoConfig {
  title: string;
  description: string;
  ogImage: string;
}

export interface RegionConfig {
  id: string;
  name: string;
  fullName: string;
  description: string;
  center: Coordinates;
  bounds: [[number, number], [number, number]];
  map: MapConfig;
  seo: SeoConfig;
  analytics: {
    yandexMetrikaId: string;
  };
  contacts: {
    telegram: string;
    email: string;
  };
}

export interface Category {
  id: string;
  name: string;
  icon: string;
  color: string;
  emoji: string;
  sortOrder: number;
}

export interface Schedule {
  regular: string;
  days: string;
  exceptions: string;
}

export interface Pricing {
  adult: number;
  child: number;
  currency: string;
  notes: string;
}

export interface Photo {
  src: string;
  alt: string;
  isMain: boolean;
}

export interface ObjectContacts {
  phone?: string;
  website?: string;
  email?: string;
  vk?: string;
  telegram?: string;
}

export interface ObjectDisplay {
  minZoom: number;
  priority: number;
  showLabel: boolean;
  illustrationAsset: string;
}

export interface BusinessInfo {
  isPaid: boolean;
  tier: 'free' | 'basic' | 'premium';
  validUntil: string;
}

export interface MapObject {
  id: string;
  slug: string;
  categoryId: string;
  name: string;
  shortName: string;
  description: string;
  fullDescription: string;
  coordinates: {
    real: Coordinates;
  };
  address: string;
  contacts: ObjectContacts;
  schedule: Schedule;
  pricing: Pricing;
  photos: Photo[];
  externalLinks: {
    yandexMaps: string;
    googleMaps: string;
  };
  display: ObjectDisplay;
  tags: string[];
  business: BusinessInfo;
  meta: {
    createdAt: string;
    updatedAt: string;
  };
}
