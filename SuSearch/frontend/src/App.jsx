
import { useState, useEffect } from 'react';
import FolderSelector from './components/settings/FolderSelector';
import Test from './BackendTest';
import TextSearch from './components/search/TextSearch';
import DocumentSearch from './components/search/DocumentSearch';
import DisplaySelectedDocumentTitle from './components/search/DisplaySelectedDocumentTitle';
import SearchPage from './pages/SearchPage';
import ProjectPage from './pages/ProjectPage';
import Header from './components/layout/Header';
import ThemeToggle from './components/layout/ThemeToggle';
import './App.css';


/**
 * Main application component.
 * Handles page navigation, search results,
 * folder selection and backend testing.
 */
export default function App() {

  // Store and restore the selected theme.
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') === 'dark' ? 'dark' : 'light';
  });

  // Apply the theme and save the selection.
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Switch between light and dark themes.
  const handleToggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const [showTest, setShowTest] = useState(false);

  const [selectedFolder, setSelectedFolder] = useState(() => {
    return window.localStorage.getItem('selectedFolder') || '';
  });

  const [selectedProject, setSelectedProject] = useState(null);
  const [results, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

 
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
      const folder = await window.pywebview.api.handle_documents();

      if (folder) {
        setSelectedFolder(folder);
        localStorage.setItem('selectedFolder', folder);
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
      setIsLoading(true);

      try {
        let results = null;

        if (searchData.document) {
          const base64data = await new Promise((resolve, reject) => {
            const reader = new Filereader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(searchData.document);
          });

          results = await window.pywebview.api.search_by_document({
            name: searchData.document.name,
            data: base64data,
          });
        }

        else if (searchData.query) {
          results = await window.pywebview.api.search_text(searchData.query);
        }

        setSearchResults(results ?? []);

      } catch (error) {
        console.error('Search failed', error);
        setSearchResults([]);

      } finally {
        setIsLoading(false);
      }
  }

  return (
    <div id="wrapper">

      {/* Shared header for SearchPage and ProjectPage. */}
      <Header
        variant={selectedProject ? 'project' : 'search'}
        projectTitle={selectedProject?.title}
        onNavigate={handleBack}
        themeToggle={
          <ThemeToggle
            theme={theme}
            onToggleTheme={handleToggleTheme}
          />
        }
      />

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
          onSelectProject={handleSelectProject}
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