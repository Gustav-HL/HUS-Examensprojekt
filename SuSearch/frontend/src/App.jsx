import { useState } from 'react'

import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [apiResponse, setApiResponse] = useState('')

  const handleClick = async () => {
    setCount((prev) => prev + 1)

    try {
      const res = await fetch('/api/health')
      const data = await res.json()
      setApiResponse(JSON.stringify(data))
    } catch (err) {
      setApiResponse('Failed to connect to backend')
    }
  }

  return (
    <>
      <section id="center">

        <div>
          <h1>Get started</h1>
          <p>
            Edit <code>src/App.jsx</code> and save to test <code>HMR</code>
          </p>
        </div>
      <div>
        <button type="button" className="counter" onClick={handleClick}>
          Count is {count}
        </button>

        {apiResponse && (
          <p style={{ marginTop: '1rem' }}>
            Backend response: <code>{apiResponse}</code>
          </p>
        )}
      </div>
      </section>

      <div className="ticks"></div>

      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

export default App
