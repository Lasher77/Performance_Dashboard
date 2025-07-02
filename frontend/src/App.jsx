import { useEffect, useState } from 'react';

function App() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    fetch('/api/metrics')
      .then((res) => res.json())
      .then(setMetrics)
      .catch((err) => console.error('Failed to load metrics', err));
  }, []);

  return (
    <div>
      <h1>Membership Metrics</h1>
      {metrics ? (
        <pre>{JSON.stringify(metrics, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
