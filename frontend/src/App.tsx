import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import AccountingEntryPage from './pages/AccountingEntryPage';
import { Box, Button } from '@chakra-ui/react';
import ErrorBoundary from './utils/error_boundary';
import LoginPage from './auth/login_page';
import ProtectedRoute from './auth/protected_route';

function App() {
  return (
    <Box p={4}>
      <nav>
        <Button as={Link} to="/" colorScheme="teal" variant="link">
          Home
        </Button>
        <Button as={Link} to="/record-entry" ml={4} colorScheme="teal" variant="link">
          Record Entry
        </Button>
        <Button as={Link} to="/login" ml={4} colorScheme="teal" variant="link">
          Login
        </Button>
      </nav>
      <ErrorBoundary>
        <Routes>
          <Route path="/" element={<div><h1>Welcome to the Accounting App</h1></div>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/record-entry" element={
            <ProtectedRoute>
              <AccountingEntryPage />
            </ProtectedRoute>
          } />
        </Routes>
      </ErrorBoundary>
    </Box>
  );
}

export default App;