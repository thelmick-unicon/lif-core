// k6 Configuration File
// This file contains common configuration settings for all k6 tests

export const config = {
  // API Base URL - modify this to match your environment
  baseUrl: __ENV.API_BASE_URL || 'http://localhost:8081',

  // API Key for authentication - set this in your environment variables
  apiKey: __ENV.API_KEY || '',
  
  // Test duration settings
  durations: {
    smoke: __ENV.SMOKE_DURATION || '30s',
    load: __ENV.LOAD_DURATION || '5m',
    stress: __ENV.STRESS_DURATION || '10m',
    spike: __ENV.SPIKE_DURATION || '2m'
  },
  
  // Virtual User (VU) settings
  users: {
    smoke: parseInt(__ENV.SMOKE_USERS) || 1,
    load: parseInt(__ENV.LOAD_USERS) || 10,
    stress: parseInt(__ENV.STRESS_USERS) || 50,
    spike: parseInt(__ENV.SPIKE_USERS) || 100
  },
  
  // Performance thresholds
  thresholds: {
    // 95% of requests must complete within 5s
    http_req_duration: ['p(95)<5000', 'avg<500'],
    // 99% of requests must be successful
    http_req_failed: ['rate<0.01']
  },
  
  // Test data
  testData: {
    modelIds: [1, 17],
    entityIds: [1, 2, 3, 4, 5],
    attributeIds: [1, 2, 3, 4, 5],
    valueSetIds: [1, 2, 3, 4, 5],
    valueIds: [1, 2, 3, 4, 5, 10, 15, 20], // Individual value records
    transformationGroupIds: [3, 12, 15, 16],
    entityAssociationIds: [1, 2, 3, 4, 5],
    entityAttributeAssociationIds: [1, 2, 3, 4, 5],
    inclusionIds: [1, 2, 3, 4, 5],
    transformationIds: [1, 2, 3, 5, 8, 12], // Individual transformations within groups
    valueMappingIds: [1, 2, 3, 4, 5],
    valueSetValueIds: [1, 2, 3, 4, 5, 10, 15], // Values within value sets
    dataModelConstraintIds: [1, 2, 3, 4, 5],
    
    // Search terms for testing
    searchTerms: ['name', 'description', 'entity', 'attribute', 'value'],
    
    // Valid enum values for API parameters
    accessTypes: ['Private', 'Public', 'Internal', 'Restricted'],
    stateTypes: ['Published', 'Draft', 'Work_In_Progress', 'Active', 'Inactive'],
    
    // Pagination settings
    pagination: {
      pages: [1, 2, 3],
      sizes: [10, 25, 50]
    },

    // Output settings
    output: {
      // Enable JSON output by default
      enableJson: __ENV.ENABLE_JSON_OUTPUT !== 'false',
      // Output directory for results
      outputDir: __ENV.OUTPUT_DIR || './results',
      // Include timestamp in filename
      includeTimestamp: __ENV.INCLUDE_TIMESTAMP !== 'false'
    }
  }
};

// Utility function to generate JSON output filename
export function generateJsonOutputFilename(testType) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').replace('T', '_').split('.')[0];
  return `${config.testData.output?.outputDir || './results'}/${testType}_test_${timestamp}.json`;
}

export default config;