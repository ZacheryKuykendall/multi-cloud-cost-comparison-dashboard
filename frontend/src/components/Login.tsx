import React from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  Paper,
  Stack,
} from '@mui/material';

const Login: React.FC = () => {
  const handleLogin = (provider: string) => {
    window.location.href = `/api/v1/auth/login/${provider}`;
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Paper sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Cloud Marketplace Cost Comparator
          </Typography>
          <Typography variant="body1" gutterBottom align="center" sx={{ mb: 4 }}>
            Sign in with your cloud provider account to compare prices
          </Typography>
          <Stack spacing={2}>
            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={() => handleLogin('aws')}
              sx={{ bgcolor: '#FF9900', '&:hover': { bgcolor: '#FF9900' } }}
            >
              Sign in with AWS
            </Button>
            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={() => handleLogin('azure')}
              sx={{ bgcolor: '#0078D4', '&:hover': { bgcolor: '#0078D4' } }}
            >
              Sign in with Azure
            </Button>
            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={() => handleLogin('google')}
              sx={{ bgcolor: '#4285F4', '&:hover': { bgcolor: '#4285F4' } }}
            >
              Sign in with Google Cloud
            </Button>
          </Stack>
        </Paper>
      </Box>
    </Container>
  );
};

export default Login; 