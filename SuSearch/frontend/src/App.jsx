import React, { useState } from 'react';
import Test from './BackendTest';
import './app.css'

export default function App() {
  const [showTest, setShowTest] = useState(false);

  return (
    <div id='wrapepr'>
      <main>

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