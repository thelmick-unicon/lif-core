import api from "./api";

const apiBaseUrl = import.meta.env.VITE_API_URL;

export const getValueSetValues = async (
  valueSetId: string,
  page = 1,
  size = 10
) => {
  try {
    const response = await api.get(
      `${apiBaseUrl}/value_set_values/by_valueset_id/${valueSetId}?page=${page}&size=${size}&pagination=false`
    );
    return response.data.data;
  } catch (error) {
    console.error("Error fetching value set values:", error);
    throw error;
  }
};

export const getValueSetAttributes = async (
  valueSetId: string,
  page = 1,
  size = 10
) => {
  try {
    const response = await api.get(
      `${apiBaseUrl}/value_sets/usage/${valueSetId}?page=${page}&size=${size}&pagination=false`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching value set attributes:", error);
    throw error;
  }
};

export const getValueSetData = async (valueSetId: string) => {
  try {
    const [valuesResponse, attributesResponse] = await Promise.all([
      getValueSetValues(valueSetId),
      getValueSetAttributes(valueSetId),
    ]);

    return {
      values: valuesResponse.values,
      valuesCount: valuesResponse.total,
      attributes: attributesResponse.attributes,
      attributesCount: attributesResponse.total,
    };
  } catch (error) {
    console.error("Error fetching value set data:", error);
    throw error;
  }
};
