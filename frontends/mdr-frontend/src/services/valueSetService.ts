import api from "./api";
import { ApiResponse } from "../types";

const apiBaseUrl = import.meta.env.VITE_API_URL;

export interface ValueSetParams {
  Name: string;
  Description?: string;
  UseConsiderations?: string;
  Notes?: string;
  CreationDate?: string;
  ActivationDate?: string;
  DeprecationDate?: string;
  Contributor?: string;
  ContributorOrganization?: string;
  DataModelId: number;
  Tags?: string;
}

export interface ValueSetValueParams {
  ValueSetId: number;
  DataModelId: number;
  Description?: string;
  UseConsiderations?: string;
  Value: string;
  ValueName: string;
  OriginalValueId?: number;
  Source?: string;
  Notes?: string;
  CreationDate?: string;
  ActivationDate?: string;
  DeprecationDate?: string;
  Contributor?: string;
  ContributorOrganization?: string;
  Extension?: boolean;
  ExtensionNotes?: string;
}

// List all value sets
export const listValueSets = async (
  pagination = false,
  page = 1,
  size = 10
) => {
  try {
    let url = `${apiBaseUrl}/value_sets/?pagination=${pagination}`;
    if (pagination) {
      url += `&page=${page}&size=${size}`;
    }
    const result = await api.get<ApiResponse>(url);
    return result.data.data;
  } catch (error) {
    console.error("Error fetching value sets:", error);
    throw error;
  }
};

// List all value sets for a specific data model
export const listValueSetsForDataModel = async (
  dataModelId: number,
  pagination = false,
  page = 1,
  size = 10
) => {
  try {
    let url = `${apiBaseUrl}/value_sets/by_data_model_id/${dataModelId}?pagination=${pagination}`;
    if (pagination) {
      url += `&page=${page}&size=${size}`;
    }
    const result = await api.get<ApiResponse>(url);
    return result.data.data;
  } catch (error) {
    console.error("Error fetching value sets:", error);
    throw error;
  }
};

// Get a single value set
export const getValueSet = async (id: number) => {
  try {
    const result = await api.get<ApiResponse>(`${apiBaseUrl}/value_sets/${id}`);
    return result.data;
  } catch (error) {
    console.error("Error fetching value set:", error);
    throw error;
  }
};

// Create a new value set
export const createValueSet = async (params: ValueSetParams) => {
  try {
    const response = await api.post<ApiResponse>(`${apiBaseUrl}/value_sets/`, params);
    return response.data;
  } catch (error) {
    console.error("Failed to create value set:", error);
    throw error;
  }
};

// Update an existing value set
export const updateValueSet = async (
  valueSetId: number,
  params: ValueSetParams
) => {
  try {
    const response = await api.put<ApiResponse>(
      `${apiBaseUrl}/value_sets/${valueSetId}`,
      params
    );
    return response.data;
  } catch (error) {
    console.error("Failed to update value set:", error);
    throw error;
  }
};

// Delete a value set
export const deleteValueSet = async (valueSetId: number) => {
  try {
    const response = await api.delete<ApiResponse>(
      `${apiBaseUrl}/value_sets/${valueSetId}`
    );
    return response.data;
  } catch (error) {
    console.error("Failed to delete value set:", error);
    throw error;
  }
};

// Create a new value set value
export const createValueSetValue = async (params: ValueSetValueParams) => {
  try {
    const response = await api.post<ApiResponse>(
      `${apiBaseUrl}/value_set_values/`,
      params
    );
    return response.data;
  } catch (error) {
    console.error("Failed to create value set value:", error);
    throw error;
  }
};

// Update an existing value set value
export const updateValueSetValue = async (
  valueId: number,
  params: ValueSetValueParams
) => {
  try {
    const response = await api.put<ApiResponse>(
      `${apiBaseUrl}/value_set_values/${valueId}`,
      params
    );
    return response.data;
  } catch (error) {
    console.error("Failed to update value set value:", error);
    throw error;
  }
};

// Delete a value set value
export const deleteValueSetValue = async (valueId: number) => {
  try {
    const response = await api.delete<ApiResponse>(
      `${apiBaseUrl}/value_set_values/${valueId}`
    );
    return response.data;
  } catch (error) {
    console.error("Failed to delete value set value:", error);
    throw error;
  }
};
