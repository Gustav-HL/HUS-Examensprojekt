
import { useState } from 'react';

import FolderSelector from './components/settings/FolderSelector';
import Test from './BackendTest';

import SearchPage from './pages/SearchPage';
import ProjectPage from './pages/ProjectPage';

import './App.css';

/**
 * Main application component.
 * Handles page navigation, search results,
 * folder selection and backend testing.
 */
export default function App() {
  const [showTest, setShowTest] = useState(false);
  const [selectedFolder, setSelectedFolder] = useState('');
  const [selectedProject, setSelectedProject] = useState(null);
  const [results, setResults] = useState([]);

  /**
   * Handles search requests.
   * Search results will be connected to the backend later.
   */
  const handleSearch = (searchData) => {
    console.log('Sökning: ', searchData);
    setResults([]);
  };

  /**
   * Opens the selected project.
   */
  const handleSelectProject = (project) => {
    setSelectedProject(project);
  };

  /**
   * Returns to the search results.
   */
  const handleBack = () => {
    setSelectedProject(null);
  };

  /**
   * Opens the folder selector through pywebview.
   */
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
    <div id="wrapper">

      {/* Preserve search state when navigating between pages. */}
      <div hidden={selectedProject !== null}>
        <SearchPage
          results={results}
          onSearch={handleSearch}
          onSelectProject={handleSelectProject}
        />

        <FolderSelector
          selectedFolder={selectedFolder}
          onSelectFolder={handleSelectFolder}
        />
      </div>

      {/* Display the selected project. */}
      {selectedProject && (
        <ProjectPage
          project={selectedProject}
          onBack={handleBack}
        />
      )}

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
