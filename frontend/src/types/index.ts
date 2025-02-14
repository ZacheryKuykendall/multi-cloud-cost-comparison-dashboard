export interface ComputePricing {
    instance_type: string;
    region: string;
    on_demand_price: number;
    spot_price?: number;
    reserved_price_1y?: number;
    reserved_price_3y?: number;
    provider: 'aws' | 'azure' | 'gcp';
}

export interface PriceComparison {
    instance_type: string;
    region: string;
    prices: ComputePricing[];
    savings: Record<string, number>;
}

export interface Region {
    id: string;
    name: string;
    provider: string;
}

export interface InstanceType {
    id: string;
    name: string;
    provider: string;
    vcpus?: number;
    memory_gb?: number;
}

export interface ErrorResponse {
    detail: string;
} 