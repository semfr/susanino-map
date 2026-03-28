'use client';

import { useEffect, useState } from 'react';

export default function TestPage() {
  const [msg, setMsg] = useState('loading...');

  useEffect(() => {
    setMsg('useEffect works!');
    import('leaflet').then((L) => {
      setMsg('Leaflet loaded: ' + typeof L.default.map);
    }).catch((err) => {
      setMsg('Leaflet error: ' + err.message);
    });
  }, []);

  return (
    <div style={{ padding: 40 }}>
      <h1>Test Page</h1>
      <p>{msg}</p>
    </div>
  );
}
