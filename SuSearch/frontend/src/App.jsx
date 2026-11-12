import React, { useState } from 'react';
import FolderSelector from './components/settings/FolderSelector';
import Test from './BackendTest';
import TextSearch from './components/search/TextSearch';
import DocumentSearch from './components/search/DocumentSearch';
import DisplaySelectedDocumentTitle from './components/search/DisplaySelectedDocumentTitle';
import SearchPage from './pages/SearchPage';
import './App.css'

export default function App() {
  const [showTest, setShowTest] = useState(false);
  const [selectedFolder, setSelectedFolder] = useState('');
  const mockProjects = [
      { id: 'doc_1', 
        title: 'Hållbara transporter.pdf',
        description: 'Ett projekt om hållbara resor'
      },
      { id: 'doc_2', 
        title: 'Återbruk i Malmö.docx',
        //description: 'Ett projekt om hållbara resor.'
      }
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

  return (
    <div id='wrapper'>
      <main>
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