import type { Metadata } from 'next';
import Link from 'next/link';
import { objects, categories } from '@/config/region';

const PAPER = '#f5f4f0';
const FOREST = '#2d5a3d';
const TERRA = '#8b3a2a';
const INK = '#1a1916';
const MUTED = '#6b675c';
const LINE = '#d8d5cc';

const TELEGRAM_URL = 'https://t.me/susanino_map_bot';
const DISPLAY = 'var(--font-display), Georgia, serif';

export const metadata: Metadata = {
  title: 'О проекте — Карта Сусанино',
  description:
    'Туристическая карта-лубок Сусанинского района: концепция, что внутри и планы развития.',
};

/** Заголовок секции с орнаментом. */
function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <h2
      className="mb-4 text-[26px] leading-tight"
      style={{ fontFamily: DISPLAY, fontWeight: 700, color: INK }}
    >
      {children}
    </h2>
  );
}

export default function AboutPage() {
  const count = objects.length;

  return (
    <main className="min-h-screen" style={{ background: PAPER, color: INK }}>
      <div className="mx-auto max-w-2xl px-6 py-10">
        {/* Назад */}
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-sm font-semibold"
          style={{ color: MUTED }}
        >
          ← На карту
        </Link>

        {/* Шапка */}
        <header className="mt-8 mb-10 text-center">
          <p
            className="mb-3 text-[11px] font-extrabold uppercase"
            style={{ color: TERRA, letterSpacing: '0.32em' }}
          >
            О проекте
          </p>
          <h1
            className="leading-[1.05]"
            style={{ fontFamily: DISPLAY, fontWeight: 700, fontSize: '40px', color: INK }}
          >
            Карта Сусанино
          </h1>
          <div className="my-4 flex items-center justify-center gap-2" aria-hidden>
            <span style={{ width: 40, height: 1, background: TERRA, opacity: 0.6 }} />
            <span style={{ color: TERRA, fontSize: 14 }}>❧</span>
            <span style={{ width: 40, height: 1, background: TERRA, opacity: 0.6 }} />
          </div>
          <p className="text-[16px] font-semibold" style={{ color: FOREST }}>
            Туристическая карта-лубок Сусанинского района
          </p>
        </header>

        {/* Концепция */}
        <section className="mb-10">
          <SectionTitle>Концепция</SectionTitle>
          <div className="space-y-4 text-[16px] leading-relaxed" style={{ color: '#33312c' }}>
            <p>
              Карта Сусанино — это не сухой навигатор, а живая картина края. Район нарисован
              в стиле русского <b style={{ color: TERRA }}>лубка</b> — народной картинки — и
              превращён в кликабельную карту достопримечательностей: касаешься места на рисунке
              и читаешь о нём.
            </p>
            <p>
              Сусанино — родина <b>Ивана Сусанина</b>, костромская глубинка с большой историей
              и тихой северной природой. Хочется показать её так, чтобы захотелось приехать —
              тепло, по-домашнему, а не списком точек на сером фоне.
            </p>
            <p>
              Карта сделана прежде всего для телефона и работает прямо в дороге, без всяких
              ухищрений с доступом, — чтобы быть полезной на месте, а не только дома за столом.
            </p>
          </div>
        </section>

        {/* Что внутри */}
        <section className="mb-10">
          <SectionTitle>Что внутри</SectionTitle>
          <ul className="space-y-3 text-[16px] leading-relaxed" style={{ color: '#33312c' }}>
            <li>
              <b style={{ color: FOREST }}>Карта-лубок</b> — рисунок района с отмеченными местами;
              клик по месту открывает его карточку.
            </li>
            <li>
              <b style={{ color: FOREST }}>Карточки мест</b> — рассказ, фотографии, адрес, часы
              работы, цены и кнопка построения маршрута.
            </li>
            <li>
              <b style={{ color: FOREST }}>Режим навигатора</b> — обычная карта с геолокацией:
              «где я» и «что рядом».
            </li>
            <li>
              <b style={{ color: FOREST }}>Telegram-бот</b> — та же карта в кармане: место по
              ссылке, поиск ближайшего и удобно делиться с друзьями.
            </li>
          </ul>

          <p className="mt-6 mb-3 text-[13px] font-bold uppercase" style={{ color: MUTED, letterSpacing: '0.12em' }}>
            Сейчас на карте · {count} мест в категориях:
          </p>
          <div className="flex flex-wrap gap-2">
            {categories.map((c) => (
              <span
                key={c.id}
                className="inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-[13px] font-semibold"
                style={{ background: '#fff', border: `1px solid ${LINE}`, color: INK }}
              >
                <span>{c.emoji}</span>
                <span>{c.name}</span>
              </span>
            ))}
          </div>
        </section>

        {/* Планы */}
        <section className="mb-10">
          <SectionTitle>Планы</SectionTitle>
          <ul className="space-y-3 text-[16px] leading-relaxed" style={{ color: '#33312c' }}>
            <li>Больше мест и настоящие фотографии каждого уголка района.</li>
            <li>Карты от разных художников — сменные «виды» одного и того же края.</li>
            <li>Маршруты-прогулки и, возможно, короткий аудиогид по местам.</li>
            <li>Перенос идеи на другие районы и городки русской глубинки.</li>
          </ul>
        </section>

        {/* Призыв к действию */}
        <section className="mt-12 mb-6 flex flex-col gap-3">
          <Link
            href="/"
            className="flex w-full items-center justify-center gap-2.5 rounded-2xl px-5 py-4 text-[17px] font-extrabold"
            style={{
              background: FOREST,
              color: PAPER,
              boxShadow: '0 14px 30px -10px rgba(45,90,61,0.5)',
            }}
          >
            Открыть карту
            <span style={{ fontSize: 18 }}>→</span>
          </Link>
          <a
            href={TELEGRAM_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="flex w-full items-center justify-center gap-2 rounded-2xl px-5 py-3.5 text-[15px] font-bold"
            style={{ background: '#fff', border: `1px solid ${LINE}`, color: TERRA }}
          >
            ✈️ Открыть в Telegram-боте
          </a>
        </section>

        <p className="mt-8 text-center text-[13px]" style={{ color: MUTED }}>
          Личный некоммерческий проект · Сусанинский район, Костромская область
        </p>
      </div>
    </main>
  );
}
