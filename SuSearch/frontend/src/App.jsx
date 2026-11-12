import React, { useState } from 'react';
import FolderSelector from './components/settings/FolderSelector';
import Test from './BackendTest';
import TextSearch from './components/search/TextSearch';
import DocumentSearch from './components/search/DocumentSearch';
import DisplaySelectedDocument from './components/search/DisplaySelectedDocumentTitle';
import './App.css'

export default function App() {
    const [showTest, setShowTest] = useState(false);
    const [query, setQuery] = useState('');
    const [selectedDocument, setSelectedDocument] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [searchResults, setSearchResults] = useState(null);

  const [selectedFolder, setSelectedFolder] = useState('');
  const mockProjects = [
      { id: 'doc_1', name: 'Hållbara transporter.pdf'},
      { id: 'doc_2', name: 'Återbruk i Malmö.docx'}
    ];

  async function handleSelectFolder() {
    if (!window.pywebview?.api?.select_folder) {
        console.warn('Folder selection requires pywebview');
        return;
    }

    try {
      const folder = await window.pywebview.api.select_folder();

      if (folder) {
        setSelectedFolder(folder);
      }
    } catch (error) {
      console.error('Failed to select folder', error);
    }
  }

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
                   {/* When the user submits a search, 
        searchData receives the search text, filters and selected document. 
        The data is then logged to the console. */}
      <SearchPage
        results={mockProjects}
        onSearch={(searchData) => console.log('Sökning: ', searchData)}
        />  
        <FolderSelector
          selectedFolder={selectedFolder}
          onSelectFolder={handleSelectFolder}
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