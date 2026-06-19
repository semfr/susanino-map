'use client';

import { useRef, useState, type ReactNode, type PointerEvent } from 'react';
import { clampSheetOffset, shouldDismissSheet } from '@/lib/sheetGesture';

interface BottomSheetProps {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}

export default function BottomSheet({ open, onClose, children }: BottomSheetProps) {
  const [offset, setOffset] = useState(0);
  const [dragging, setDragging] = useState(false);
  const drag = useRef<{ startY: number; lastY: number; lastT: number; v: number } | null>(null);

  if (!open) return null;

  const onPointerDown = (e: PointerEvent) => {
    (e.currentTarget as Element).setPointerCapture?.(e.pointerId);
    drag.current = { startY: e.clientY, lastY: e.clientY, lastT: e.timeStamp, v: 0 };
    setDragging(true);
  };

  const onPointerMove = (e: PointerEvent) => {
    const d = drag.current;
    if (!d) return;
    const dt = e.timeStamp - d.lastT;
    if (dt > 0) d.v = (e.clientY - d.lastY) / dt;
    d.lastY = e.clientY;
    d.lastT = e.timeStamp;
    setOffset(clampSheetOffset(e.clientY - d.startY));
  };

  const endDrag = (e: PointerEvent) => {
    const d = drag.current;
    if (!d) return;
    const deltaY = e.clientY - d.startY;
    const velocity = d.v;
    drag.current = null;
    setDragging(false);
    setOffset(0);
    if (shouldDismissSheet({ deltaY, velocity })) onClose();
  };

  return (
    <>
      {/* Overlay */}
      <div className="fixed inset-0 bg-black/40 z-[600]" onClick={onClose} />
      {/* Sheet */}
      <div
        className="fixed bottom-0 left-0 right-0 z-[700] bg-white rounded-t-2xl shadow-2xl max-h-[85vh] overflow-y-auto"
        style={{
          transform: `translateY(${offset}px)`,
          transition: dragging ? 'none' : 'transform 0.3s ease',
        }}
      >
        {/* Handle — зона свайпа вниз для закрытия */}
        <div
          className="sticky top-0 bg-white rounded-t-2xl pt-3 pb-2 flex justify-center z-10 cursor-grab active:cursor-grabbing"
          style={{ touchAction: 'none' }}
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={endDrag}
          onPointerCancel={endDrag}
        >
          <div className="w-10 h-1.5 rounded-full bg-gray-300" />
        </div>
        {/* Content */}
        <div className="px-4 pb-8">{children}</div>
      </div>
    </>
  );
}
