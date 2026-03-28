'use client';

interface MapControlsProps {
  mode: 'map' | 'illustration';
  onToggle: () => void;
}

export default function MapControls({ mode, onToggle }: MapControlsProps) {
  return (
    <div
      className="absolute top-4 right-4 z-[1000]"
      style={{ zIndex: 1000 }}
    >
      <button
        onClick={onToggle}
        className="flex items-center gap-2 px-3 py-2 bg-white rounded-lg shadow-md border border-gray-200 text-sm font-medium text-gray-700 hover:bg-gray-50 active:bg-gray-100 transition-colors"
        title={mode === 'map' ? 'Показать лубок' : 'Показать навигацию'}
      >
        <span className="text-base">{mode === 'map' ? '🎨' : '🗺'}</span>
        <span>{mode === 'map' ? 'Лубок' : 'Навигация'}</span>
      </button>
    </div>
  );
}
