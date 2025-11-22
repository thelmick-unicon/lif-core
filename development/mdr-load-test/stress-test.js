// Stress Test Suite
// Tests API performance under high load to find breaking points
import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from './k6.config.js';
import { 
  makeRequest, 
  headers, 
  randomSleep, 
  testDataGenerator,
  logTestResult
} from './utils.js';

export let options = {
  stages: [
    { duration: '2m', target: config.users.load }, // Normal load
    { duration: '5m', target: config.users.stress }, // Stress load
    { duration: '2m', target: config.users.load }, // Scale back to normal
    { duration: '1m', target: 0 }, // Ramp down
  ],
  thresholds: {
    // More relaxed thresholds for stress testing
    http_req_duration: ['p(95)<5000', 'avg<2000'], // 95% under 5s, average under 2s
    http_req_failed: ['rate<0.05'] // 95% success rate
  }
};

export default function () {
  const baseUrl = config.baseUrl;

  // Mix of different API calls to simulate real usage patterns
  const scenarios = [
    () => testDataModelsStress(baseUrl),
    () => testEntitiesStress(baseUrl),
    () => testSearchStress(baseUrl),
    () => testValueSetsStress(baseUrl),
    () => testComplexQueries(baseUrl),
    () => testDataModelRelatedStress(baseUrl),
    () => testIntegrationStress(baseUrl),
    () => testAttributesStress(baseUrl),
    () => testTransformationsStress(baseUrl),
    () => testValueMappingsStress(baseUrl)
  ];

  // Randomly select and execute scenarios
  const scenario = testDataGenerator.randomArrayElement(scenarios);
  scenario();

  // Shorter sleep times to increase load
  randomSleep(0.5, 2);
}

function testDataModelsStress(baseUrl) {
  // Test various data model endpoints with valid enum values
  const accessType = testDataGenerator.randomArrayElement(config.testData.accessTypes);
  const stateType = testDataGenerator.randomArrayElement(config.testData.stateTypes);
  
  const endpoints = [
    '/datamodels/?pagination=false',
    '/datamodels/?page=1&size=50&pagination=true',
    `/datamodels/?level_of_access=${accessType}&pagination=false`,
    `/datamodels/?state=${stateType}&pagination=false`,
    '/datamodels/?include_extension=true&pagination=false',
    `/datamodels/?level_of_access=${accessType}&state=${stateType}&pagination=false`,
    '/datamodels/orglif/',
    '/transformation_groups/data_models/'
  ];

  const endpoint = testDataGenerator.randomArrayElement(endpoints);
  
  const response = makeRequest(
    http.get,
    `${baseUrl}${endpoint}`,
    { headers },
    {
      'stress - data models responds': (r) => r.status < 500,
      'stress - reasonable response time': (r) => r.timings.duration < 10000
    }
  );
  
  logTestResult(`Stress - Data Models: ${endpoint}`, response);
}

function testEntitiesStress(baseUrl) {
  // Test entity endpoints with different parameters
  const page = Math.floor(Math.random() * 5) + 1;
  const size = [10, 25, 50, 100][Math.floor(Math.random() * 4)];
  
  const response = makeRequest(
    http.get,
    `${baseUrl}/entities/?page=${page}&size=${size}&pagination=true`,
    { headers },
    {
      'stress - entities responds': (r) => r.status < 500,
      'stress - reasonable response time': (r) => r.timings.duration < 8000
    }
  );
  
  logTestResult(`Stress - Entities (page=${page}, size=${size})`, response);
}

function testSearchStress(baseUrl) {
  // Test search with various terms and parameters
  const searchTerms = ['name', 'description', 'entity', 'attribute', 'value', 'model', 'data'];
  const searchTerm = testDataGenerator.randomArrayElement(searchTerms);
  
  // Add random parameters with proper data model ID selection
  const params = [];
  const useOnlyExtension = Math.random() > 0.7;
  
  if (Math.random() > 0.5) {
    // Use context-aware data model ID generation
    const dataModelId = testDataGenerator.randomDataModelId(useOnlyExtension);
    params.push(`data_model_id=${dataModelId}`);
  }
  
  if (useOnlyExtension) {
    params.push('only_extension=true');
  }
  
  const queryString = params.length > 0 ? `&${params.join('&')}` : '';
  
  const response = makeRequest(
    http.get,
    `${baseUrl}/search/?search_key=${searchTerm}${queryString}`,
    { headers },
    {
      'stress - search responds': (r) => r.status < 500,
      'stress - search reasonable time': (r) => r.timings.duration < 15000
    }
  );
  
  logTestResult(`Stress - Search: ${searchTerm}${queryString}`, response);
}

function testValueSetsStress(baseUrl) {
  const page = Math.floor(Math.random() * 3) + 1;
  const size = [10, 25, 50][Math.floor(Math.random() * 3)];
  
  const response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/?page=${page}&size=${size}&pagination=true`,
    { headers },
    {
      'stress - value sets responds': (r) => r.status < 500,
      'stress - reasonable response time': (r) => r.timings.duration < 6000
    }
  );
  
  logTestResult(`Stress - Value Sets (page=${page}, size=${size})`, response);
}

function testComplexQueries(baseUrl) {
  // Test more complex endpoints that might be resource intensive
  const endpoints = [
    () => {
      const id = testDataGenerator.randomDataModelId(false);
      return `/datamodels/with_details/${id}`;
    },
    () => {
      const id = testDataGenerator.randomDataModelId(false);
      return `/datamodels/open_api_schema/${id}?include_attr_md=true`;
    },
    () => '/transformation_groups/transformations_for_data_models/?source_data_model_id=26&target_data_model_id=17&size=100'
  ];

  const endpointFunc = testDataGenerator.randomArrayElement(endpoints);
  const endpoint = endpointFunc();
  
  const response = makeRequest(
    http.get,
    `${baseUrl}${endpoint}`,
    { headers },
    {
      'stress - complex query responds': (r) => r.status < 500,
      'stress - complex query time acceptable': (r) => r.timings.duration < 20000
    }
  );
  
  logTestResult(`Stress - Complex Query: ${endpoint}`, response);
}

function testDataModelRelatedStress(baseUrl) {
  const dataModelId = testDataGenerator.randomDataModelId(false);
  
  const endpoints = [
    `/entities/by_data_model_id/${dataModelId}?pagination=false`,
    `/attributes/by_data_model_id/${dataModelId}?pagination=false`,
    `/entity_associations/by_data_model_id/${dataModelId}?pagination=false&allow_empty=true`,
    `/entity_attribute_associations/by_data_model_id/${dataModelId}?pagination=false`
  ];
  
  const endpoint = testDataGenerator.randomArrayElement(endpoints);
  
  const response = makeRequest(
    http.get,
    `${baseUrl}${endpoint}`,
    { headers },
    {
      'stress - data model related responds': (r) => r.status < 500,
      'stress - data model related time acceptable': (r) => r.timings.duration < 15000
    }
  );
  
  logTestResult(`Stress - Data Model Related: ${endpoint}`, response);
}

function testIntegrationStress(baseUrl) {
  const endpoints = [
    '/transformation_groups/data_models/',
    '/datamodels/orglif/',
    () => {
      const transformationGroupId = testDataGenerator.randomArrayElement(config.testData.transformationGroupIds || [1, 2, 3, 4, 5]);
      return `/transformation_groups/${transformationGroupId}?pagination=false`;
    }
  ];
  
  const endpointOrFunc = testDataGenerator.randomArrayElement(endpoints);
  const endpoint = typeof endpointOrFunc === 'function' ? endpointOrFunc() : endpointOrFunc;
  
  const response = makeRequest(
    http.get,
    `${baseUrl}${endpoint}`,
    { headers },
    {
      'stress - integration responds': (r) => r.status < 500,
      'stress - integration time acceptable': (r) => r.timings.duration < 10000
    }
  );
  
  logTestResult(`Stress - Integration: ${endpoint}`, response);
}

function testAttributesStress(baseUrl) {
  const endpoints = [
    '/attributes?pagination=false',
    () => {
      const entityId = testDataGenerator.randomArrayElement(config.testData.entityIds);
      return `/attributes/by_entity_id/${entityId}`;
    },
    () => {
      const attributeId = testDataGenerator.randomArrayElement(config.testData.attributeIds);
      return `/attributes/${attributeId}`;
    },
    () => {
      const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
      return `/attributes/by_data_model_id/${dataModelId}?pagination=false`;
    }
  ];
  
  const endpointOrFunc = testDataGenerator.randomArrayElement(endpoints);
  const endpoint = typeof endpointOrFunc === 'function' ? endpointOrFunc() : endpointOrFunc;
  
  const response = makeRequest(
    http.get,
    `${baseUrl}${endpoint}`,
    { headers },
    {
      'stress - attributes responds': (r) => r.status < 500,
      'stress - attributes time acceptable': (r) => r.timings.duration < 8000
    }
  );
  
  logTestResult(`Stress - Attributes: ${endpoint}`, response);
}

function testTransformationsStress(baseUrl) {
  const endpoints = [
    '/transformation_groups?pagination=false',
    '/transformations_for_data_models?source_data_model_id=1&target_data_model_id=17',
    () => {
      const transformationGroupId = testDataGenerator.randomArrayElement(config.testData.transformationGroupIds);
      return `/transformation_groups/${transformationGroupId}`;
    },
    () => {
      const transformationId = testDataGenerator.randomArrayElement(config.testData.transformationIds);
      return `/transformation_groups/transformations/${transformationId}`;
    }
  ];
  
  const endpointOrFunc = testDataGenerator.randomArrayElement(endpoints);
  const endpoint = typeof endpointOrFunc === 'function' ? endpointOrFunc() : endpointOrFunc;
  
  const response = makeRequest(
    http.get,
    `${baseUrl}${endpoint}`,
    { headers },
    {
      'stress - transformations responds': (r) => r.status < 500,
      'stress - transformations time acceptable': (r) => r.timings.duration < 12000
    }
  );
  
  logTestResult(`Stress - Transformations: ${endpoint}`, response);
}

function testValueMappingsStress(baseUrl) {
  const endpoints = [
    '/value_mappings?page=1&size=50',
    '/value_set_values?pagination=false',
    () => {
      const valueMappingId = testDataGenerator.randomArrayElement(config.testData.valueMappingIds);
      return `/value_mappings/${valueMappingId}`;
    },
    () => {
      const transformationGroupId = testDataGenerator.randomArrayElement(config.testData.transformationGroupIds);
      return `/value_mappings/by_transformation_group/${transformationGroupId}`;
    },
    () => {
      const valueSetId = testDataGenerator.randomArrayElement(config.testData.valueSetIds);
      return `/value_set_values/by_valueset_id/${valueSetId}`;
    },
    () => {
      const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
      return `/value_sets/by_data_model_id/${dataModelId}`;
    }
  ];
  
  const endpointOrFunc = testDataGenerator.randomArrayElement(endpoints);
  const endpoint = typeof endpointOrFunc === 'function' ? endpointOrFunc() : endpointOrFunc;
  
  const response = makeRequest(
    http.get,
    `${baseUrl}${endpoint}`,
    { headers },
    {
      'stress - value mappings responds': (r) => r.status < 500,
      'stress - value mappings time acceptable': (r) => r.timings.duration < 10000
    }
  );
  
  logTestResult(`Stress - Value Mappings: ${endpoint}`, response);
}

export function teardown() {
  console.log('Stress test completed');
}