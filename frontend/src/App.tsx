import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Chessboard from './components/Chessboard'
import MoveHistory from './components/MoveHistory'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <h1>Chess Game</h1>
      <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center' }}>
        <Chessboard />
        <MoveHistory />
      </div>
    </div>
  )
}

export default App
