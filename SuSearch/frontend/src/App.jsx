import React, { useState } from 'react';
import Test from './BackendTest';
import TextSearch from './components/search/TextSearch';
import DocumentSearch from './components/search/DocumentSearch';
import './app.css'

export default function App() {
    const [showTest, setShowTest] = useState(false);
    const [query, setQuery] = useState('');
    const [selectedDocument, setSelectedDocument] = useState(null);

    return (
      <div id='wrapepr'>
        <main>
          <TextSearch
          value={query}
          onChange={setQuery}
          onSearch={(event) => event.preventDefault()} 
          />
          <DocumentSearch 
          onFileChange={setSelectedDocument} 
          />
        </main>

        {/* Testing the backend connection please dont change this or the child component //GHL */}
        <button id='test-btn'
          onClick={() => setShowTest((prev) => !prev)}>
          {showTest ? 'Close Backend' : 'Test Backend'}
        </button>
        {showTest && (
          <div id='test-box'>
            <Test />
          </div>
        )}
      </div>
    );
}