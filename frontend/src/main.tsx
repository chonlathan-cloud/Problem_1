import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { ChakraProvider } from '@chakra-ui/react'
import { BrowserRouter as Router } from 'react-router-dom'
import { AuthProvider } from './auth/auth_context'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ChakraProvider>
      <Router>
        <AuthProvider>
          <App />
        </AuthProvider>
      </Router>
    </ChakraProvider>
  </StrictMode>,
)