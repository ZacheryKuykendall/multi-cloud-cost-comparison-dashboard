from google.cloud import compute_v1
from typing import List, Dict, Optional
from ..models.pricing import ComputePricing
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

class GCPPriceProvider:
    def __init__(self):
        """Initialize GCP pricing client."""
        self.catalog_url = "https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus"
        self.client = httpx.AsyncClient(timeout=30.0)
        self.project_id = os.getenv('GCP_PROJECT_ID')
        self._compute_client = None

    @property
    def compute_client(self):
        """Lazy initialization of compute client."""
        if self._compute_client is None:
            self._compute_client = compute_v1.InstancesClient()
        return self._compute_client

    async def get_compute_prices(self, instance_type: str, region: str) -> List[ComputePricing]:
        """
        Get GCP compute prices for a specific instance type and region.
        """
        try:
            # Get all compute SKUs for the instance type and region
            params = {
                'key': os.getenv('GCP_API_KEY'),
                'filter': f'resource.machineType="{instance_type}" AND resource.region="{region}"'
            }
            response = await self.client.get(self.catalog_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Parse different price types
            on_demand_price = None
            spot_price = None
            reserved_1y_price = None
            reserved_3y_price = None

            for sku in data.get('skus', []):
                pricing_info = sku.get('pricingInfo', [{}])[0]
                price_type = sku.get('category', {}).get('resourceGroup', '')

                if 'OnDemand' in price_type:
                    on_demand_price = self._parse_price(pricing_info)
                elif 'Spot' in price_type:
                    spot_price = self._parse_price(pricing_info)
                elif 'Commitment' in price_type:
                    term = sku.get('description', '')
                    if '1 Year' in term:
                        reserved_1y_price = self._parse_price(pricing_info)
                    elif '3 Year' in term:
                        reserved_3y_price = self._parse_price(pricing_info)

            return [ComputePricing(
                instance_type=instance_type,
                region=region,
                on_demand_price=on_demand_price or 0.0,
                spot_price=spot_price,
                reserved_price_1y=reserved_1y_price,
                reserved_price_3y=reserved_3y_price,
                provider='gcp'
            )]

        except Exception as e:
            print(f"GCP pricing error: {str(e)}")
            return []

    def _parse_price(self, pricing_info: Dict) -> Optional[float]:
        """Parse price from GCP API response."""
        try:
            price_details = pricing_info.get('pricingExpression', {})
            unit_price = float(price_details.get('tieredRates', [{}])[0].get('unitPrice', {}).get('nanos', 0)) / 1e9
            unit_price += float(price_details.get('tieredRates', [{}])[0].get('unitPrice', {}).get('units', 0))
            return unit_price
        except Exception:
            return None

    async def get_regions(self) -> Dict[str, str]:
        """Get available GCP regions."""
        try:
            # For now, return a static list of regions to avoid GCP client initialization
            return {
                'us-central1': 'US Central (Iowa)',
                'us-east1': 'US East (South Carolina)',
                'us-east4': 'US East (Northern Virginia)',
                'us-west1': 'US West (Oregon)',
                'europe-west1': 'Europe West (Belgium)',
                'asia-east1': 'Asia East (Taiwan)'
            }
        except Exception as e:
            print(f"GCP regions error: {str(e)}")
            return {}

    async def get_instance_types(self) -> Dict[str, str]:
        """Get available GCP instance types."""
        try:
            # For now, return a static list of common instance types
            return {
                'n1-standard-1': 'n1-standard-1',
                'n1-standard-2': 'n1-standard-2',
                'n1-standard-4': 'n1-standard-4',
                'n1-standard-8': 'n1-standard-8',
                'n2-standard-2': 'n2-standard-2',
                'n2-standard-4': 'n2-standard-4',
                'e2-standard-2': 'e2-standard-2',
                'e2-standard-4': 'e2-standard-4'
            }
        except Exception as e:
            print(f"GCP instance types error: {str(e)}")
            return {}

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

# Create a singleton instance
gcp_provider = GCPPriceProvider()

# Export the methods
get_compute_prices = gcp_provider.get_compute_prices
get_regions = gcp_provider.get_regions
get_instance_types = gcp_provider.get_instance_types 