import React, { useState } from 'react';
import Test from './BackendTest';
import SearchPage from './pages/SearchPage';
import './app.css'

export default function App() {
    const [showTest, setShowTest] = useState(false);

    return (
      <div id='wrapepr'>
      
      {/* When the user submits a search, 
        searchData receives the search text, filters and selected document. 
        The data is then logged to the console. */}
      <SearchPage
        onSearch={(searchData) => console.log('Sökning: ', searchData)}
      />  

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