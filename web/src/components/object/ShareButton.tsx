'use client';

import { useState } from 'react';

interface ShareButtonProps {
  className?: string;
}

export default function ShareButton({ className = '' }: ShareButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback: try Web Share API
      if (navigator.share) {
        await navigator.share({ url: window.location.href });
      }
    }
  };

  return (
    <button
      onClick={handleShare}
      className={`flex items-center justify-center gap-2 py-3 px-4 rounded-xl border border-gray-200 text-gray-700 font-medium text-sm hover:bg-gray-50 transition-colors ${className}`}
    >
      <span>{copied ? '✅' : '🔗'}</span>
      <span>{copied ? 'Скопировано' : 'Поделиться'}</span>
    </button>
  );
}
