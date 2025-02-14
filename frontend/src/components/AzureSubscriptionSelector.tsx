import React, { useEffect, useState } from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import { api } from '../services/api';

interface Subscription {
  subscriptionId: string;
  displayName: string;
  state: string;
}

interface AzureSubscriptionSelectorProps {
  onSubscriptionChange: (subscriptionId: string) => void;
}

const AzureSubscriptionSelector: React.FC<AzureSubscriptionSelectorProps> = ({
  onSubscriptionChange,
}) => {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [selectedSubscription, setSelectedSubscription] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        setLoading(true);
        const response = await api.get('/azure/subscriptions');
        setSubscriptions(response.data.subscriptions);
        
        // If there's only one subscription, select it automatically
        if (response.data.subscriptions.length === 1) {
          setSelectedSubscription(response.data.subscriptions[0].subscriptionId);
          onSubscriptionChange(response.data.subscriptions[0].subscriptionId);
        }
      } catch (err) {
        setError('Failed to load Azure subscriptions');
        console.error('Error fetching subscriptions:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSubscriptions();
  }, [onSubscriptionChange]);

  const handleSubscriptionChange = (event: any) => {
    const subscriptionId = event.target.value;
    setSelectedSubscription(subscriptionId);
    onSubscriptionChange(subscriptionId);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={2}>
        <CircularProgress size={24} />
        <Typography variant="body2" sx={{ ml: 1 }}>
          Loading subscriptions...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  if (subscriptions.length === 0) {
    return (
      <Alert severity="warning" sx={{ mb: 2 }}>
        No Azure subscriptions found. Please make sure you have access to at least one subscription.
      </Alert>
    );
  }

  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="subtitle1" gutterBottom>
        Azure Subscription
      </Typography>
      <FormControl fullWidth>
        <InputLabel>Select Subscription</InputLabel>
        <Select
          value={selectedSubscription}
          label="Select Subscription"
          onChange={handleSubscriptionChange}
        >
          {subscriptions.map((sub) => (
            <MenuItem key={sub.subscriptionId} value={sub.subscriptionId}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                <Typography variant="body1">{sub.displayName}</Typography>
                <Chip
                  label={sub.state}
                  size="small"
                  color={sub.state === 'Enabled' ? 'success' : 'error'}
                  sx={{ ml: 1 }}
                />
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
};

export default AzureSubscriptionSelector; 