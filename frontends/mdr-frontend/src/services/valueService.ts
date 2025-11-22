import api from "./api";

const apiBaseUrl = import.meta.env.VITE_API_URL;

interface ApiResponse {
  data: any;
}

export interface ValueParams {
  ValueSetId: number;
  DataModelId: number;
  Value: string;
  ValueName?: string | null;
  Description?: string | null;
  UseConsiderations?: string | null;
  OriginalValueId?: number | null;
  Source?: string | null;
  Notes?: string | null;
  CreationDate?: string | null;
  ActivationDate?: string | null;
  DeprecationDate?: string | null;
  Contributor?: string | null;
  ContributorOrganization?: string | null;
  Extension?: boolean;
  ExtensionNotes?: string | null;
}

export const createValue = async (params: ValueParams) => {
  try {
    const result = await api.post<ApiResponse>(`${apiBaseUrl}/value_set_values/`, [params]); // Note: API expects an array
    return result.data;
  } catch (error) {
    console.error("Failed to create value:", error);
    throw error;
  }
};

export const updateValue = async (valueId: number, params: ValueParams) => {
  try {
    const result = await api.put<ApiResponse>(`${apiBaseUrl}/value_set_values/${valueId}`, params);
    return result.data;
  } catch (error) {
    console.error("Failed to update value:", error);
    throw error;
  }
};

export const deleteValue = async (valueId: number) => {
  try {
    const result = await api.delete<ApiResponse>(`${apiBaseUrl}/value_set_values/${valueId}`);
    return result.data;
  } catch (error) {
    console.error("Failed to delete value:", error);
    throw error;
  }
};
