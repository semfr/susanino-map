'use client';

import { useMapObjects } from '@/hooks/useMapObjects';
import BottomSheet from '@/components/ui/BottomSheet';
import ObjectCard from '@/components/object/ObjectCard';

export default function BottomSheetWrapper() {
  const { selectedObject, setSelectedObject } = useMapObjects();

  return (
    <BottomSheet
      open={selectedObject !== null}
      onClose={() => setSelectedObject(null)}
    >
      {selectedObject && <ObjectCard object={selectedObject} />}
    </BottomSheet>
  );
}
