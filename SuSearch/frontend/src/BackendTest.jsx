import React, { useState } from 'react';

export default function Test() {
    const [query, setQuery] = useState('');
    const [result, setResult] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim() || !window.pywebview?.api) return;

        if (!window.pywebview?.api) {
            setError("Unable to reach backend.");
            return;
        }

        try {
            const data = await window.pywebview.api.search_text(query);
            console.log("Result:", data);
            setResult(data);
        }
        catch (err) {
            console.error("Backend error:", err);
            setResult(null);
        }

    };

    return (
        <div style={{ padding: '20px', width: '100%' }}>
            <form
                onSubmit={handleSearch}>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    style={{ padding: '10px', width: '80%', margin: 'auto' }}
                    placeholder="Search"
                />
                <button type="submit">Search</button>
            </form>

            {result && (
                <pre style={{ marginTop: '16px', background: '#eee', padding: '10px' }}>
                    {JSON.stringify(result, null, 2)}
                </pre>
            )}
        </div>
    );
}