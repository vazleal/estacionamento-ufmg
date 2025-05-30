import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import PainelEstacionamento from './App'
import LoginPage from './pages/LoginPage/LoginPage'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <PainelEstacionamento />
  </StrictMode>,
)
