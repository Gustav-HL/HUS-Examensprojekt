import React, { useState } from 'react';
import FolderSelector from './components/settings/FolderSelector';
import Test from './BackendTest';
import './App.css'

export default function App() {
  const [showTest, setShowTest] = useState(false);
  const [selectedFolder, setSelectedFolder] = useState('');

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