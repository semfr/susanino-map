import { botDeepLink } from '@/lib/botLink';

interface TelegramBotButtonProps {
  objectId: string;
  className?: string;
}

// Кнопка-ссылка «Открыть в Telegram-боте» (deep-link на карточку объекта в боте).
// Цвет — терракота (--kal-terra) фирменной палитры, чтобы отличаться от синей «Построить маршрут».
export default function TelegramBotButton({ objectId, className = '' }: TelegramBotButtonProps) {
  const url = botDeepLink(objectId);

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className={`flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-medium text-sm text-white transition-colors ${className}`}
      style={{ backgroundColor: 'var(--kal-terra)' }}
    >
      <span>✈️</span>
      <span>Открыть в Telegram-боте</span>
    </a>
  );
}
