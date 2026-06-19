import type { Metadata } from "next";
import { Geist, Geist_Mono, Cormorant_Garamond, Nunito } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Фирменные шрифты «Календарь русской природы» (с кириллицей).
const cormorant = Cormorant_Garamond({
  variable: "--font-display",
  subsets: ["latin", "cyrillic"],
  weight: ["500", "600", "700"],
  display: "swap",
});

const nunito = Nunito({
  variable: "--font-body",
  subsets: ["latin", "cyrillic"],
  weight: ["400", "600", "700", "800"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Карта Сусанинского района",
  description: "Интерактивная карта достопримечательностей Сусанинского района",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';
  // На GitHub Pages (подпуть) SW отключаем для теста: пути в sw.js абсолютные,
  // под подпутём кэш некорректен. Офлайн вернём при деплое на свой домен.
  const swScript = basePath
    ? ''
    : `
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/sw.js').catch(function() {});
    });
  }
`;
  return (
    <html
      lang="ru"
      className={`${geistSans.variable} ${geistMono.variable} ${cormorant.variable} ${nunito.variable} h-full antialiased`}
    >
      <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <link rel="manifest" href={`${basePath}/manifest.json`} />
        <meta name="theme-color" content="#8B4513" />
      </head>
      <body className="min-h-full flex flex-col">
        {children}
        {swScript ? <script dangerouslySetInnerHTML={{ __html: swScript }} /> : null}
      </body>
    </html>
  );
}
