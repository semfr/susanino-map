import configData from '../data/config.json';
import categoriesData from '../data/categories.json';
import objectsData from '../data/objects.json';
import illustrationGuide from '../data/illustrations/guide-susanino.json';
import type { RegionConfig, Category, MapObject, Illustration } from '../types';

export const config = configData as RegionConfig;
export const categories = categoriesData as Category[];
export const objects = objectsData as MapObject[];

// Статический import иллюстраций (static export требует import, не fetch).
export const illustrations: Illustration[] = [illustrationGuide as unknown as Illustration];

export function getIllustration(id: string): Illustration | undefined {
  return illustrations.find((i) => i.id === id);
}

export function getDefaultIllustration(): Illustration {
  return illustrations.find((i) => i.isDefault) ?? illustrations[0];
}
