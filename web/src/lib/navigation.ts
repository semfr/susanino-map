export function getYandexMapsRouteUrl(lat: number, lng: number, name: string): string {
  return `https://yandex.ru/maps/?rtext=~${lat},${lng}&rtt=auto&text=${encodeURIComponent(name)}`;
}

export function getYandexMapsOrgUrl(orgUrl: string): string {
  return orgUrl;
}
