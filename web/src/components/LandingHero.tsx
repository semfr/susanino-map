'use client';

import { asset } from '@/lib/asset';
import { getDefaultIllustration, objects } from '@/config/region';

interface LandingHeroProps {
  /** Переход к интерактивной карте. */
  onOpen: () => void;
}

const PAPER = '#f5f4f0';
const FOREST = '#2d5a3d';
const TERRA = '#8b3a2a';
const INK = '#1a1916';
const MUTED = '#6b675c';

const TELEGRAM_URL = 'https://t.me/susanino_map_bot';

/**
 * Стартовый лендинг (стиль «Календарь русской природы»):
 * лубок-обложка сверху плавно перетекает (фейд) в бумажную панель снизу
 * с заголовком, краткой справкой и кнопками. Картинка статична и на весь экран
 * (не Leaflet) — поэтому она заполняет экран телефона и не «гуляет».
 * Кнопка «Открыть карту» открывает интерактивную карту.
 */
export default function LandingHero({ onOpen }: LandingHeroProps) {
  const illustration = getDefaultIllustration();
  const lubokSrc = asset(`/images/map/${illustration.file}`);
  const count = objects.length;

  return (
    <div
      className="relative h-full w-full overflow-hidden select-none"
      style={{ background: PAPER }}
    >
      {/* Лубок-обложка на весь экран */}
      <img
        src={lubokSrc}
        alt="Иллюстрированная карта Сусанинского района"
        className="absolute inset-0 h-full w-full object-cover"
        style={{ objectPosition: 'center 30%' }}
        draggable={false}
      />

      {/* Фейд: чёткий лубок сверху → сплошная бумага снизу */}
      <div
        className="absolute inset-0"
        style={{
          background:
            'linear-gradient(180deg, rgba(245,244,240,0) 0%, rgba(245,244,240,0) 38%, rgba(245,244,240,0.72) 52%, #f5f4f0 64%, #f5f4f0 100%)',
        }}
      />

      {/* Декоративные пины поверх чёткой части лубка */}
      <Pin n={1} color={TERRA} top="20%" left="24%" />
      <Pin n={2} color={INK} top="30%" left="62%" />
      <Pin n={3} color={FOREST} top="40%" left="40%" />

      {/* Контент на бумажной части */}
      <div className="absolute inset-0 flex flex-col items-center justify-end px-7 pb-9 text-center">
        <p
          className="mb-2 text-[11px] font-extrabold uppercase"
          style={{ color: TERRA, letterSpacing: '0.32em' }}
        >
          Туристическая карта
        </p>

        <h1
          className="leading-[1.02]"
          style={{
            fontFamily: 'var(--font-display), Georgia, serif',
            fontWeight: 700,
            fontSize: '44px',
            color: INK,
            letterSpacing: '0.5px',
          }}
        >
          Карта Сусанино
        </h1>

        {/* Орнаментальная линейка */}
        <div className="my-3.5 flex items-center gap-2" aria-hidden>
          <span style={{ width: 34, height: 1, background: TERRA, opacity: 0.6 }} />
          <span style={{ color: TERRA, fontSize: 14 }}>❧</span>
          <span style={{ width: 34, height: 1, background: TERRA, opacity: 0.6 }} />
        </div>

        <p className="text-[15px] font-bold" style={{ color: FOREST }}>
          Сусанинский район · Костромская область
        </p>
        <p className="mt-1.5 text-[12.5px] font-semibold" style={{ color: MUTED }}>
          край Ивана Сусанина ·{' '}
          <b style={{ color: TERRA, fontWeight: 800 }}>{count} объектов</b>
        </p>

        <button
          type="button"
          onClick={onOpen}
          className="mt-6 flex w-full items-center justify-center gap-2.5 rounded-2xl px-5 py-4 text-[17px] font-extrabold active:scale-[0.99]"
          style={{
            background: FOREST,
            color: PAPER,
            boxShadow: '0 14px 30px -10px rgba(45,90,61,0.5)',
            transition: 'transform 0.1s ease',
          }}
        >
          Открыть карту
          <span style={{ fontSize: 18 }}>→</span>
        </button>

        <a
          href={TELEGRAM_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 text-[13.5px] font-bold underline-offset-4 hover:underline"
          style={{ color: TERRA }}
        >
          Открыть в Telegram
        </a>
      </div>
    </div>
  );
}

function Pin({
  n,
  color,
  top,
  left,
}: {
  n: number;
  color: string;
  top: string;
  left: string;
}) {
  return (
    <div
      className="absolute flex h-7 w-7 items-center justify-center"
      style={{
        top,
        left,
        background: color,
        color: PAPER,
        borderRadius: '50% 50% 50% 2px',
        transform: 'rotate(45deg)',
        border: `2px solid ${PAPER}`,
        boxShadow: '0 4px 10px rgba(26,25,22,0.4)',
      }}
      aria-hidden
    >
      <span style={{ transform: 'rotate(-45deg)', fontSize: 12, fontWeight: 800 }}>
        {n}
      </span>
    </div>
  );
}
