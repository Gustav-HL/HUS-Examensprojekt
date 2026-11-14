import React, { useState } from 'react';
import FolderSelector from './components/settings/FolderSelector';
import Test from './BackendTest';
import TextSearch from './components/search/TextSearch';
import DocumentSearch from './components/search/DocumentSearch';
<<<<<<< Updated upstream
import DisplaySelectedDocument from './components/search/DisplaySelectedDocumentTitle';
=======
import DisplaySelectedDocumentTitle from './components/search/DisplaySelectedDocumentTitle';
>>>>>>> Stashed changes
import SearchPage from './pages/SearchPage';
import './App.css'

export default function App() {
  const [showTest, setShowTest] = useState(false);
  const [selectedFolder, setSelectedFolder] = useState('');
  const [isLoading] = useState(false);
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

  async function handleSearch(searchData) {
    console.log('Sökning: ', searchData);
      let results = null;

      if (searchData.document) {
        const base64Data = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(reader.result);
          reader.onerror = reject;
          reader.readAsDataURL(searchData.document);
        });

        results = await window.pywebview.api.search_by_document({
          name: searchData.document.name,
          data: base64Data,
        });
      } 
      
      else if (searchData.query) {
        results = await window.pywebview.api.search_text(searchData.query);
      }

      setSearchResults(results);
    
  }

  return (
    <div id='wrapper'>
      <main>
         {/* When the user submits a search, 
        searchData receives the search text, filters and selected document. 
        The data is then logged to the console. */}
      <SearchPage
        results={mockProjects}
        loading={isLoading}
        onSearch={handleSearch}
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