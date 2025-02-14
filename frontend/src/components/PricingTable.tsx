import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
} from '@mui/material';
import { ComputePricing } from '../types';

interface PricingTableProps {
  prices: ComputePricing[];
}

const PricingTable: React.FC<PricingTableProps> = ({ prices }) => {
  const formatPrice = (price: number | undefined) => {
    if (price === undefined) return 'N/A';
    return `$${price.toFixed(4)}/hr`;
  };

  const calculateSavings = (price: ComputePricing) => {
    const savings: { [key: string]: string } = {};
    const onDemandPrice = price.on_demand_price;

    if (price.spot_price) {
      const spotSavings = ((onDemandPrice - price.spot_price) / onDemandPrice) * 100;
      savings['Spot'] = `${spotSavings.toFixed(1)}%`;
    }

    if (price.reserved_price_1y) {
      const reserved1ySavings = ((onDemandPrice - price.reserved_price_1y) / onDemandPrice) * 100;
      savings['1-Year Reserved'] = `${reserved1ySavings.toFixed(1)}%`;
    }

    if (price.reserved_price_3y) {
      const reserved3ySavings = ((onDemandPrice - price.reserved_price_3y) / onDemandPrice) * 100;
      savings['3-Year Reserved'] = `${reserved3ySavings.toFixed(1)}%`;
    }

    return savings;
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Provider</TableCell>
            <TableCell align="right">On-Demand</TableCell>
            <TableCell align="right">Spot (Savings)</TableCell>
            <TableCell align="right">1-Year Reserved (Savings)</TableCell>
            <TableCell align="right">3-Year Reserved (Savings)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {prices.map((price) => {
            const savings = calculateSavings(price);
            return (
              <TableRow key={price.provider}>
                <TableCell component="th" scope="row">
                  <Typography variant="body1" sx={{ textTransform: 'uppercase' }}>
                    {price.provider}
                  </Typography>
                </TableCell>
                <TableCell align="right">
                  {formatPrice(price.on_demand_price)}
                </TableCell>
                <TableCell align="right">
                  <Box>
                    {formatPrice(price.spot_price)}
                    {savings['Spot'] && (
                      <Typography variant="caption" color="success.main" display="block">
                        Save {savings['Spot']}
                      </Typography>
                    )}
                  </Box>
                </TableCell>
                <TableCell align="right">
                  <Box>
                    {formatPrice(price.reserved_price_1y)}
                    {savings['1-Year Reserved'] && (
                      <Typography variant="caption" color="success.main" display="block">
                        Save {savings['1-Year Reserved']}
                      </Typography>
                    )}
                  </Box>
                </TableCell>
                <TableCell align="right">
                  <Box>
                    {formatPrice(price.reserved_price_3y)}
                    {savings['3-Year Reserved'] && (
                      <Typography variant="caption" color="success.main" display="block">
                        Save {savings['3-Year Reserved']}
                      </Typography>
                    )}
                  </Box>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PricingTable; 