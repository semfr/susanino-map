'use client';

import type { ReactNode } from 'react';

interface BottomSheetProps {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}

export default function BottomSheet({ open, onClose, children }: BottomSheetProps) {
  if (!open) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/40 z-[600]"
        onClick={onClose}
      />
      {/* Sheet */}
      <div className="fixed bottom-0 left-0 right-0 z-[700] bg-white rounded-t-2xl shadow-2xl max-h-[85vh] overflow-y-auto transition-transform duration-300">
        {/* Handle */}
        <div className="sticky top-0 bg-white rounded-t-2xl pt-3 pb-2 flex justify-center z-10">
          <div className="w-10 h-1.5 rounded-full bg-gray-300" />
        </div>
        {/* Content */}
        <div className="px-4 pb-8">
          {children}
        </div>
      </div>
    </>
  );
}
