from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class ComputePricing(BaseModel):
    """Model for compute instance pricing."""
    instance_type: str = Field(..., description="Instance type/size")
    region: str = Field(..., description="Cloud region")
    on_demand_price: float = Field(..., description="On-demand price per hour")
    spot_price: Optional[float] = Field(None, description="Spot/preemptible price per hour")
    reserved_price_1y: Optional[float] = Field(None, description="1-year reserved/committed price per hour")
    reserved_price_3y: Optional[float] = Field(None, description="3-year reserved/committed price per hour")
    provider: str = Field(..., description="Cloud provider (aws, azure, gcp)")

class PriceComparison(BaseModel):
    """Model for price comparison results."""
    instance_type: str
    region: str
    prices: List[ComputePricing]
    savings: Dict[str, float] = Field(
        default_factory=dict,
        description="Potential savings percentages for different pricing models"
    )

class Region(BaseModel):
    """Model for cloud region."""
    id: str = Field(..., description="Region identifier")
    name: str = Field(..., description="Region display name")
    provider: str = Field(..., description="Cloud provider")

class InstanceType(BaseModel):
    """Model for instance type."""
    id: str = Field(..., description="Instance type identifier")
    name: str = Field(..., description="Instance type display name")
    provider: str = Field(..., description="Cloud provider")
    vcpus: Optional[int] = Field(None, description="Number of vCPUs")
    memory_gb: Optional[float] = Field(None, description="Memory in GB")

class ErrorResponse(BaseModel):
    """Model for error responses."""
    detail: str = Field(..., description="Error message") 