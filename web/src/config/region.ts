import configData from '../data/config.json';
import categoriesData from '../data/categories.json';
import objectsData from '../data/objects.json';
import type { RegionConfig, Category, MapObject } from '../types';

export const config = configData as RegionConfig;
export const categories = categoriesData as Category[];
export const objects = objectsData as MapObject[];
