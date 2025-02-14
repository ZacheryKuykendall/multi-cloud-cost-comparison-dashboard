import boto3
from typing import List, Dict, Optional
from ..models.pricing import ComputePricing
import os
from dotenv import load_dotenv

load_dotenv()

class AWSPriceProvider:
    def __init__(self):
        """Initialize AWS pricing client."""
        self._pricing_client = None
        self._ec2_client = None

    @property
    def pricing_client(self):
        """Lazy initialization of pricing client."""
        if self._pricing_client is None and os.getenv('AWS_ACCESS_KEY_ID'):
            self._pricing_client = boto3.client(
                'pricing',
                region_name='us-east-1',  # Pricing API is only available in us-east-1
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
        return self._pricing_client

    @property
    def ec2_client(self):
        """Lazy initialization of EC2 client."""
        if self._ec2_client is None and os.getenv('AWS_ACCESS_KEY_ID'):
            self._ec2_client = boto3.client(
                'ec2',
                region_name='us-east-1',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
        return self._ec2_client

    async def get_compute_prices(self, instance_type: str, region: str) -> List[ComputePricing]:
        """
        Get AWS compute prices for a specific instance type and region.
        """
        try:
            # For testing, return static sample data
            return [ComputePricing(
                instance_type=instance_type,
                region=region,
                on_demand_price=0.0464,  # Sample price for t2.micro in us-east-1
                spot_price=0.0139,
                reserved_price_1y=0.0299,
                reserved_price_3y=0.0199,
                provider='aws'
            )]
        except Exception as e:
            print(f"AWS pricing error: {str(e)}")
            return []

    async def get_regions(self) -> Dict[str, str]:
        """Get available AWS regions."""
        try:
            # Return static list of common regions
            return {
                'us-east-1': 'US East (N. Virginia)',
                'us-east-2': 'US East (Ohio)',
                'us-west-1': 'US West (N. California)',
                'us-west-2': 'US West (Oregon)',
                'eu-west-1': 'Europe (Ireland)',
                'eu-central-1': 'Europe (Frankfurt)',
                'ap-northeast-1': 'Asia Pacific (Tokyo)',
                'ap-southeast-1': 'Asia Pacific (Singapore)'
            }
        except Exception as e:
            print(f"AWS regions error: {str(e)}")
            return {}

    async def get_instance_types(self) -> Dict[str, str]:
        """Get available AWS instance types."""
        try:
            # Return static list of common instance types
            return {
                't2.micro': 't2.micro',
                't2.small': 't2.small',
                't2.medium': 't2.medium',
                't3.micro': 't3.micro',
                't3.small': 't3.small',
                't3.medium': 't3.medium',
                'm5.large': 'm5.large',
                'm5.xlarge': 'm5.xlarge'
            }
        except Exception as e:
            print(f"AWS instance types error: {str(e)}")
            return {}

# Create a singleton instance
aws_provider = AWSPriceProvider()

# Export the methods
get_compute_prices = aws_provider.get_compute_prices
get_regions = aws_provider.get_regions
get_instance_types = aws_provider.get_instance_types 