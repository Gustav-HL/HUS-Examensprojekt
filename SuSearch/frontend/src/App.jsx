
import { useState } from 'react';

import FolderSelector from './components/settings/FolderSelector';
import Test from './BackendTest';

import SearchPage from './pages/SearchPage';
import ProjectPage from './pages/ProjectPage';

import './App.css';

// Temporary mock data for testing page navigation.
const mockProjects = [
  {
    id: 'doc_1',
    name: 'Hållbara transporter.pdf',
    title: 'Hållbara transporter',
    area: 'Transport',
    description: 'Ett exempelprojekt om hållbara transportlösningar.',
    organization: 'Testorganisation',
    location: 'Skåne',
    status: 'Avslutat'
  },
  {
    id: 'doc_2',
    name: 'Återbruk i Malmö.docx',
    title: 'Återbruk i Malmö',
    area: 'Återbruk',
    description: 'Ett exempelprojekt om återbruk och hållbar konsumtion.',
    organization: 'Testorganisation',
    location: 'Malmö',
    status: 'Pågående'
  }
];

/**
 * Main application component.
 * Handles page navigation, folder selection and backend testing.
 */
export default function App() {
  const [showTest, setShowTest] = useState(false);
  const [selectedFolder, setSelectedFolder] = useState('');
  const [selectedProject, setSelectedProject] = useState(null);

  /**
   * Opens the selected project's detail page.
   */
  const handleSelectProject = (project) => {
    setSelectedProject(project);
  };

  /**
   * Returns to the search results page.
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

      {/* Keep SearchPage mounted to preserve its state. */}
      <div hidden={selectedProject !== null}>
        <SearchPage
          results={mockProjects}
          onSearch={(searchData) =>
            console.log('Sökning: ', searchData)
          }
          onSelectProject={handleSelectProject}
        />

        <FolderSelector
          selectedFolder={selectedFolder}
          onSelectFolder={handleSelectFolder}
        />
      </div>

      {/* Display the selected project's detail page. */}
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
