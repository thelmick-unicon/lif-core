// Spike Test Suite  
// Tests API behavior during sudden traffic spikes
import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from './k6.config.js';
import { 
  makeRequest, 
  headers, 
  testDataGenerator,
  logTestResult
} from './utils.js';

export let options = {
  stages: [
    { duration: '10s', target: config.users.load }, // Normal load
    { duration: '1m', target: config.users.spike }, // Sudden spike
    { duration: '10s', target: config.users.load }, // Back to normal
    { duration: '10s', target: 0 }, // Ramp down
  ],
  thresholds: {
    // More lenient thresholds for spike testing
    http_req_duration: ['p(95)<10000'], // 95% under 10s
    http_req_failed: ['rate<0.1'], // 90% success rate
  }
};

export default function () {
  const baseUrl = config.baseUrl;

  // During spike test, focus on core endpoints that users would hit most
  const scenarios = [
    () => testCoreEndpoints(baseUrl),
    () => testCriticalPaths(baseUrl),
    () => testResourceIntensiveOperations(baseUrl)
  ];

  const scenario = testDataGenerator.randomArrayElement(scenarios);
  scenario();

  // Very short sleep to maximize request rate
  sleep(Math.random() * 0.5);
}

function testCoreEndpoints(baseUrl) {
  // Core endpoints that must remain responsive
  const endpoints = [
    '/health-check',
    '/datamodels/?pagination=false',
    '/entities/?pagination=false',
    '/value_sets/?pagination=false',
    '/datamodels/orglif/',
    '/transformation_groups/data_models/',
    '/attributes?pagination=false',
    '/transformation_groups?pagination=false',
    '/value_mappings?page=1&size=10',
    `/entity_associations/by_data_model_id/${testDataGenerator.randomArrayElement(config.testData.modelIds)}?pagination=false&allow_empty=true`,
    '/value_set_values?pagination=false'
  ];

  const endpoint = testDataGenerator.randomArrayElement(endpoints);
  
  const response = makeRequest(
    http.get,
    `${baseUrl}${endpoint}`,
    { headers },
    {
      'spike - core endpoint available': (r) => r.status < 500,
      'spike - core endpoint responsive': (r) => r.timings.duration < 15000
    }
  );
  
  logTestResult(`Spike - Core: ${endpoint}`, response);
}

function testCriticalPaths(baseUrl) {
  // Critical user paths that should work during spikes
  const paths = [
    () => {
      // Search - critical for user discovery
      const term = testDataGenerator.randomArrayElement(['name', 'entity', 'model']);
      return makeRequest(
        http.get,
        `${baseUrl}/search/?search_key=${term}`,
        { headers },
        {
          'spike - search available': (r) => r.status < 500,
          'spike - search time reasonable': (r) => r.timings.duration < 20000
        }
      );
    },
    () => {
      // Data model details - critical for data exploration
      const id = testDataGenerator.randomArrayElement(config.testData.modelIds);
      return makeRequest(
        http.get,
        `${baseUrl}/datamodels/${id}`,
        { headers },
        {
          'spike - model details available': (r) => r.status < 500 || r.status === 404,
          'spike - model details time reasonable': (r) => r.timings.duration < 10000
        }
      );
    },
    () => {
      // Entities by data model - important for data exploration
      const id = testDataGenerator.randomArrayElement(config.testData.modelIds);
      return makeRequest(
        http.get,
        `${baseUrl}/entities/by_data_model_id/${id}?pagination=false`,
        { headers },
        {
          'spike - entities by model available': (r) => r.status < 500,
          'spike - entities by model time reasonable': (r) => r.timings.duration < 15000
        }
      );
    },
    () => {
      // Paginated listing - common user interaction
      const page = Math.floor(Math.random() * 3) + 1;
      return makeRequest(
        http.get,
        `${baseUrl}/datamodels/?page=${page}&size=10&pagination=true`,
        { headers },
        {
          'spike - pagination available': (r) => r.status < 500,
          'spike - pagination time reasonable': (r) => r.timings.duration < 12000
        }
      );
    }
  ];

  const pathFunc = testDataGenerator.randomArrayElement(paths);
  const response = pathFunc();
  
  logTestResult('Spike - Critical Path', response);
}

function testResourceIntensiveOperations(baseUrl) {
  // Test resource-heavy operations under spike conditions
  const operations = [
    () => {
      // Complex search with parameters
      const term = testDataGenerator.randomString(5);
      return makeRequest(
        http.get,
        `${baseUrl}/search/?search_key=${term}&only_extension=true`,
        { headers },
        {
          'spike - complex search handles load': (r) => r.status < 500,
          'spike - complex search eventually responds': (r) => r.timings.duration < 25000
        }
      );
    },
    () => {
      // Data model with details
      const id = testDataGenerator.randomArrayElement(config.testData.modelIds);
      return makeRequest(
        http.get,
        `${baseUrl}/datamodels/with_details/${id}?public_only=false`,
        { headers },
        {
          'spike - detailed model handles load': (r) => r.status < 500 || r.status === 404,
          'spike - detailed model eventually responds': (r) => r.timings.duration < 20000
        }
      );
    },
    () => {
      // OpenAPI schema generation - resource intensive
      const id = testDataGenerator.randomArrayElement(config.testData.modelIds);
      return makeRequest(
        http.get,
        `${baseUrl}/datamodels/open_api_schema/${id}?include_attr_md=true`,
        { headers },
        {
          'spike - openapi schema handles load': (r) => r.status < 500 || r.status === 404,
          'spike - openapi schema eventually responds': (r) => r.timings.duration < 30000
        }
      );
    },
    () => {
      // Transformation queries - complex operations
      return makeRequest(
        http.get,
        `${baseUrl}/transformation_groups/transformations_for_data_models/?source_data_model_id=26&target_data_model_id=17&size=100`,
        { headers },
        {
          'spike - transformations handle load': (r) => r.status < 500,
          'spike - transformations eventually respond': (r) => r.timings.duration < 25000
        }
      );
    }
  ];

  const operationFunc = testDataGenerator.randomArrayElement(operations);
  const response = operationFunc();
  
  logTestResult('Spike - Resource Intensive', response);
}

export function teardown() {
  console.log('Spike test completed');
}