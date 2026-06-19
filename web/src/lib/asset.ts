// Префикс basePath для «сырых» абсолютных путей к ассетам из /public.
// На GitHub Pages (project page) сайт отдаётся по подпути /susanino-map,
// поэтому пути вида /images/... нужно префиксовать значением NEXT_PUBLIC_BASE_PATH.
// На localhost / при своём домене basePath пустой — пути остаются как есть.
export const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || '';

export function asset(p: string): string {
  if (!p) return p;
  if (/^https?:\/\//i.test(p) || p.startsWith('data:')) return p; // внешние URL не трогаем
  return BASE_PATH + (p.startsWith('/') ? p : '/' + p);
}
