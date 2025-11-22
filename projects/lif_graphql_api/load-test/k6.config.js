// k6 Configuration File
// This file contains common configuration settings for all k6 tests

export const config = {
  // API Base URL - modify this to match your environment
  baseUrl: __ENV.API_BASE_URL || 'http://localhost:8000',
  
  // Authentication
  authToken: __ENV.AUTH_TOKEN || 'your-token-here',
  
  // Target Group for load balancer routing
  targetGroup: __ENV.TARGET_GROUP || 'dev-graphql-org1',
  
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
    // Demo person data for GraphQL testing
    r1_demo_data: {
      "100001": ["Public Sector", "Private Sector"],
      "100002": ["Non-Profit"],
      "100003": ["Private Sector"],
      "100004": ["Public Sector"],
      "100005": ["Non-Profit", "Private Sector"],
      "100006": ["Non-Profit", "Public Sector"]
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