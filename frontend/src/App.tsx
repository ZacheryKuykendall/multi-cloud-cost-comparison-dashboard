import React, { useState, useEffect } from 'react';
import { ThemeProvider, CssBaseline, Box } from '@mui/material';
import { lightTheme, darkTheme } from './theme';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import Login from './components/Login';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is authenticated (e.g., by checking URL params or session storage)
    const params = new URLSearchParams(window.location.search);
    const provider = params.get('provider');
    if (provider) {
      setIsAuthenticated(true);
      // Remove the query parameter
      window.history.replaceState({}, '', window.location.pathname);
    }
  }, []);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Header isDarkMode={isDarkMode} onThemeToggle={toggleTheme} />
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          {isAuthenticated ? <Dashboard /> : <Login />}
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App; 