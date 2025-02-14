import httpx
from typing import List, Dict, Optional
from ..models.pricing import ComputePricing
import os
from dotenv import load_dotenv

load_dotenv()

class AzurePriceProvider:
    def __init__(self):
        """Initialize Azure pricing client."""
        self.base_url = "https://prices.azure.com/api/retail/prices"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_compute_prices(self, instance_type: str, region: str) -> List[ComputePricing]:
        """
        Get Azure compute prices for a specific instance type and region.
        """
        try:
            # For testing, return static sample data
            return [ComputePricing(
                instance_type=instance_type,
                region=region,
                on_demand_price=0.0496,  # Sample price for Standard_B1s in eastus
                spot_price=0.0149,
                reserved_price_1y=0.0298,
                reserved_price_3y=0.0199,
                provider='azure'
            )]
        except Exception as e:
            print(f"Azure pricing error: {str(e)}")
            return []

    async def get_regions(self) -> Dict[str, str]:
        """Get available Azure regions."""
        try:
            # Return static list of common regions
            return {
                'eastus': 'East US',
                'eastus2': 'East US 2',
                'westus': 'West US',
                'westus2': 'West US 2',
                'northeurope': 'North Europe',
                'westeurope': 'West Europe',
                'southeastasia': 'Southeast Asia',
                'japaneast': 'Japan East'
            }
        except Exception as e:
            print(f"Azure regions error: {str(e)}")
            return {}

    async def get_instance_types(self) -> Dict[str, str]:
        """Get available Azure instance types."""
        try:
            # Return static list of common instance types
            return {
                'Standard_B1s': 'Standard_B1s',
                'Standard_B2s': 'Standard_B2s',
                'Standard_D2s_v3': 'Standard_D2s_v3',
                'Standard_D4s_v3': 'Standard_D4s_v3',
                'Standard_F2s_v2': 'Standard_F2s_v2',
                'Standard_F4s_v2': 'Standard_F4s_v2',
                'Standard_E2s_v3': 'Standard_E2s_v3',
                'Standard_E4s_v3': 'Standard_E4s_v3'
            }
        except Exception as e:
            print(f"Azure instance types error: {str(e)}")
            return {}

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

# Create a singleton instance
azure_provider = AzurePriceProvider()

# Export the methods
get_compute_prices = azure_provider.get_compute_prices
get_regions = azure_provider.get_regions
get_instance_types = azure_provider.get_instance_types 