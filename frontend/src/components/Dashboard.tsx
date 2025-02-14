import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Box,
  Card,
  CardContent,
} from '@mui/material';
import { getComputePrices, getRegions, getInstanceTypes } from '../services/api';
import { ComputePricing } from '../types';
import PriceComparisonChart from './PriceComparisonChart';
import PricingTable from './PricingTable';

const Dashboard: React.FC = () => {
  const [selectedRegion, setSelectedRegion] = useState<string>('');
  const [selectedInstanceType, setSelectedInstanceType] = useState<string>('');
  const [regions, setRegions] = useState<Record<string, string>>({});
  const [instanceTypes, setInstanceTypes] = useState<Record<string, string>>({});
  const [prices, setPrices] = useState<ComputePricing[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [regionsData, instanceTypesData] = await Promise.all([
          getRegions(),
          getInstanceTypes(),
        ]);
        setRegions(regionsData);
        setInstanceTypes(instanceTypesData);
      } catch (err) {
        setError('Failed to load initial data');
      }
    };

    fetchInitialData();
  }, []);

  useEffect(() => {
    const fetchPrices = async () => {
      if (!selectedRegion || !selectedInstanceType) return;

      setLoading(true);
      setError(null);
      try {
        const pricesData = await getComputePrices(selectedInstanceType, selectedRegion);
        setPrices(pricesData);
      } catch (err) {
        setError('Failed to load pricing data');
      } finally {
        setLoading(false);
      }
    };

    fetchPrices();
  }, [selectedRegion, selectedInstanceType]);

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Cloud Cost Comparison Dashboard
      </Typography>

      {/* Controls */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Region</InputLabel>
              <Select
                value={selectedRegion}
                label="Region"
                onChange={(e) => setSelectedRegion(e.target.value)}
              >
                {Object.entries(regions).map(([id, name]) => (
                  <MenuItem key={id} value={id}>
                    {name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Instance Type</InputLabel>
              <Select
                value={selectedInstanceType}
                label="Instance Type"
                onChange={(e) => setSelectedInstanceType(e.target.value)}
              >
                {Object.entries(instanceTypes).map(([id, name]) => (
                  <MenuItem key={id} value={id}>
                    {name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Loading Indicator */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Price Comparison Chart */}
      {!loading && prices.length > 0 && (
        <>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Price Comparison Chart
            </Typography>
            <PriceComparisonChart prices={prices} />
          </Paper>

          {/* Pricing Table */}
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Detailed Pricing
            </Typography>
            <PricingTable prices={prices} />
          </Paper>
        </>
      )}
    </Container>
  );
};

export default Dashboard; 