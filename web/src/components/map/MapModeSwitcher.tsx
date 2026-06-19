'use client';

export type MapMode = 'geo' | 'illustration';

interface MapModeSwitcherProps {
  mode: MapMode;
  onChange: (mode: MapMode) => void;
}

/**
 * Переключатель режимов карты: Навигатор (geo) / Лубок (illustration).
 * Заменяет MapControls.
 */
export default function MapModeSwitcher({ mode, onChange }: MapModeSwitcherProps) {
  const baseBtn =
    'flex items-center gap-1.5 px-3 py-2 text-sm font-medium transition-colors';
  const activeBtn = 'bg-stone-800 text-white';
  const inactiveBtn = 'bg-white text-stone-700 hover:bg-stone-50 active:bg-stone-100';

  return (
    <div
      className="absolute bottom-4 left-1/2 -translate-x-1/2 z-[1000] flex overflow-hidden rounded-full border border-stone-200 shadow-md"
      style={{ zIndex: 1000 }}
    >
      <button
        type="button"
        onClick={() => onChange('geo')}
        className={`${baseBtn} ${mode === 'geo' ? activeBtn : inactiveBtn}`}
        aria-pressed={mode === 'geo'}
        title="Режим навигатора (GPS)"
      >
        <span className="text-base">🗺</span>
        <span>Навигатор</span>
      </button>
      <button
        type="button"
        onClick={() => onChange('illustration')}
        className={`${baseBtn} ${mode === 'illustration' ? activeBtn : inactiveBtn}`}
        aria-pressed={mode === 'illustration'}
        title="Режим лубка (иллюстрация)"
      >
        <span className="text-base">🎨</span>
        <span>Лубок</span>
      </button>
    </div>
  );
}
