import api from "./api";
import {
  ApiResponse,
  CountResponse,
  InclusionDTO,
} from "../types";

const apiBaseUrl = import.meta.env.VITE_API_URL;

export const getInclusion = async (id: number) => {
  try {
    const result = await api.get<ApiResponse>(
      `${apiBaseUrl}/inclusions/${id}`
    );
    return result.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export const listInclusionByModel = async (id: number) => {
  try {
    const result = await api.get<ApiResponse>(
      `${apiBaseUrl}/inclusions/by_data_model_id/${id}?pagination=false`
    );
    return result?.data?.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export interface CreateInclusionParams {
  ExtDataModelId: number;
  IncludedElementId: number;
  ElementType: 'Attribute' | 'Entity' | 'Constraint' | 'Transformation';
  LevelOfAccess: 'Private' | 'Public' | 'Internal' | 'Restricted';
  Deleted: boolean;
  CreationDate?: string | null;
  ActivationDate?: string | null;
  DeprecationDate?: string | null;
  Contributor?: string | null;
  ContributorOrganization?: string | null;
}
const Types: string[] = ['Attribute', 'Entity', 'Constraint', 'Transformation'];
const LevelOfAccess: string[] = ['Private', 'Public', 'Internal', 'Restricted'];
// Generate a template
export const tmplCreateInclusion = (modelId: number, eleId: number, dtoType: string, access?: string): CreateInclusionParams => {
  if (!Types.includes(dtoType)) { console.warn(`Unknown Inclusion ElementType: "${dtoType}"`); }
  if (!access || !LevelOfAccess.includes(access)) { access = LevelOfAccess[0]; }
  return {
    ExtDataModelId: modelId,
    IncludedElementId: eleId,
    ElementType: dtoType as CreateInclusionParams["ElementType"],
    LevelOfAccess: access as CreateInclusionParams["LevelOfAccess"],
    Deleted: false,
    CreationDate: new Date().toISOString().slice(0, 16),
    ActivationDate: new Date().toISOString().slice(0, 16),
    DeprecationDate: null,
    Contributor: null,
    ContributorOrganization: null,
  };
};

export const createInclusion = async (params: CreateInclusionParams) => {
  try {
    const response = await api.post(`${apiBaseUrl}/inclusions/`, params);
    return response.data;
  } catch (error) {
    console.error("Error creating inclusion:", error);
    throw error;
  }
};

export const updateInclusion = async (id: number, params: Partial<CreateInclusionParams>) => {
  try {
    const response = await api.put(`${apiBaseUrl}/inclusions/${id}`, params);
    return response.data;
  } catch (error) {
    console.error("Error updating inclusion:", error);
    throw error;
  }
};

export const deleteInclusion = async (id: number) => {
  try {
    const response = await api.delete(`${apiBaseUrl}/inclusions/${id}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting inclusion:", error);
    throw error;
  }
};
