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
  const [results, setSearchResults] = useState([]);
  const [isLoading] = useState(false);

 
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

   /**
   * Sends a document or text query to the backend. 
   * Stores the returned search results in state.
   */
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

      setSearchResults(results ?? []);
    
  }

  return (
    <div id="wrapper">

      {/* Preserve search state when navigating between pages. */}
      <div hidden={selectedProject !== null}>
       
      {/* SearchPage receives the search results and loading status.
          When the user searches or selects a project,
          it calls the corresponding function in App. */}
       <SearchPage
          results={results}
          loading={isLoading}
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