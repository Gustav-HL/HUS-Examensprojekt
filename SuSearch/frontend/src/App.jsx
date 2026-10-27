import { useState } from 'react';

export default function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    if (window.pywebview && window.pywebview.api) {
      setLoading(true);
      
      try {
        const data = await window.pywebview.api.execute_search(query);
        setResults(data);
        console.log(data)
      } 
      
      catch (err) {
        console.error('Fel vid anrop till Python:', err);
      } 
      
      finally {
        setLoading(false);
      }
    } 
    
    else {
      console.warn('Använd inte webläsaren kör main.py');
    }
  };

  return (
    <div>
      <h1>Testo</h1>

      <div style={{ display: 'flex' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ flex: 1, padding: '8px' }}
        />
        <button onClick={handleSearch} disabled={loading} style={{ padding: '8px 16px' }}>
          {loading ? 'Söker' : 'Sök'}
        </button>
      </div>

      <div>
        {results.map((item, index) => (
          <div
            key={index}>
            <p>{item.text}</p>
            <p>{item.score}</p>
          </div>
        ))}
      </div>
    </div>
  );
}