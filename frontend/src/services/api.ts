import axios from 'axios';
import { ComputePricing, Region, InstanceType } from '../types';

export const api = axios.create({
    baseURL: '/api/v1',
});

export interface AzureSubscription {
    subscriptionId: string;
    displayName: string;
    state: string;
}

export const getComputePrices = async (
    instanceType: string, 
    region: string, 
    subscriptionId?: string
): Promise<ComputePricing[]> => {
    const response = await api.get<ComputePricing[]>('/compute/prices', {
        params: { 
            instance_type: instanceType, 
            region,
            subscription_id: subscriptionId 
        },
    });
    return response.data;
};

export const getRegions = async (subscriptionId?: string): Promise<Record<string, string>> => {
    const response = await api.get<Record<string, string>>('/regions', {
        params: { subscription_id: subscriptionId }
    });
    return response.data;
};

export const getInstanceTypes = async (subscriptionId?: string): Promise<Record<string, string>> => {
    const response = await api.get<Record<string, string>>('/instance-types', {
        params: { subscription_id: subscriptionId }
    });
    return response.data;
};

export const getAzureSubscriptions = async (): Promise<AzureSubscription[]> => {
    const response = await api.get<{ subscriptions: AzureSubscription[] }>('/azure/subscriptions');
    return response.data.subscriptions;
}; 