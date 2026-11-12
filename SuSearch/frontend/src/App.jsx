import React, { useState } from 'react';
import Test from './BackendTest';
import TextSearch from './components/search/TextSearch';
import DocumentSearch from './components/search/DocumentSearch';
import DisplaySelectedDocument from './components/search/DisplaySelectedDocument';
import './App.css'

export default function App() {
    const [showTest, setShowTest] = useState(false);
    const [query, setQuery] = useState('');
    const [selectedDocument, setSelectedDocument] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [searchResults, setSearchResults] = useState(null);

    const handleDocumentSearch = async () => {
        if (!selectedDocument) return;

        setIsLoading(true);
        try {
            // selectedDocument is the file path string returned by Python file dialog
            const results = await window.pywebview.api.search_by_document(selectedDocument);
            setSearchResults(results);
        } catch (error) {
            console.error('Failed to search document:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
      <div id='wrapepr'>
        <main>
          <TextSearch
          value={query}
          onChange={setQuery}
          onSearch={(event) => console.log('Söktext: ', query)}
          />
          <DocumentSearch 
          file={selectedDocument}
          onFileChange={setSelectedDocument} 
          />
          <DisplaySelectedDocument
          file={selectedDocument}
          onRemove={() => setSelectedDocument(null)}
          />
          {selectedDocument && (
            <button 
              onClick={handleDocumentSearch} 
              disabled={isLoading}
              style={{ marginTop: '10px' }}
            >
              {isLoading ? 'Söker...' : 'Sök med dokument'}
            </button>
          )}
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