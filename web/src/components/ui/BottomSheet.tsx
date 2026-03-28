'use client';

import { useState } from 'react';
import { Drawer } from 'vaul';
import type { ReactNode } from 'react';

interface BottomSheetProps {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}

const SNAP_POINTS = [0.4, 0.85];

export default function BottomSheet({ open, onClose, children }: BottomSheetProps) {
  const [snap, setSnap] = useState<number | string | null>(SNAP_POINTS[0]);

  return (
    <Drawer.Root
      open={open}
      onOpenChange={(isOpen) => {
        if (!isOpen) {
          setSnap(SNAP_POINTS[0]);
          onClose();
        }
      }}
      snapPoints={SNAP_POINTS}
      activeSnapPoint={snap}
      setActiveSnapPoint={setSnap}
    >
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 bg-black/40 z-40" />
        <Drawer.Content
          className="fixed bottom-0 left-0 right-0 z-50 flex flex-col bg-white rounded-t-2xl outline-none"
          style={{ height: `${Number(snap) * 100}dvh` }}
        >
          {/* Handle bar */}
          <div className="flex justify-center pt-3 pb-2 shrink-0">
            <div className="w-10 h-1.5 rounded-full bg-gray-300" />
          </div>

          {/* Scrollable content */}
          <div
            className="flex-1 overflow-y-auto overscroll-contain px-4 pb-8"
          >
            {children}
          </div>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}
