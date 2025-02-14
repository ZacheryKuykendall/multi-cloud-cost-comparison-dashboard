import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useTheme } from '@mui/material';
import { ComputePricing } from '../types';

interface PriceComparisonChartProps {
  prices: ComputePricing[];
}

const PriceComparisonChart: React.FC<PriceComparisonChartProps> = ({ prices }) => {
  const theme = useTheme();

  // Transform data for the chart
  const chartData = prices.map((price) => ({
    provider: price.provider.toUpperCase(),
    'On-Demand': price.on_demand_price,
    'Spot': price.spot_price || 0,
    '1-Year Reserved': price.reserved_price_1y || 0,
    '3-Year Reserved': price.reserved_price_3y || 0,
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={chartData}
        margin={{
          top: 20,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="provider"
          tick={{ fill: theme.palette.text.primary }}
        />
        <YAxis
          label={{
            value: 'Price per Hour ($)',
            angle: -90,
            position: 'insideLeft',
            fill: theme.palette.text.primary,
          }}
          tick={{ fill: theme.palette.text.primary }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: theme.palette.background.paper,
            border: `1px solid ${theme.palette.divider}`,
            borderRadius: 4,
          }}
        />
        <Legend />
        <Bar
          dataKey="On-Demand"
          fill={theme.palette.primary.main}
          name="On-Demand"
        />
        <Bar
          dataKey="Spot"
          fill={theme.palette.secondary.main}
          name="Spot"
        />
        <Bar
          dataKey="1-Year Reserved"
          fill={theme.palette.success.main}
          name="1-Year Reserved"
        />
        <Bar
          dataKey="3-Year Reserved"
          fill={theme.palette.warning.main}
          name="3-Year Reserved"
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default PriceComparisonChart; 