// Load Test Suite
// Tests API performance under normal expected load
import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from './k6.config.js';
import { 
  makeRequest, 
  headers, 
  randomSleep, 
  validatePaginationResponse,
  validateEntityResponse,
  testDataGenerator,
  logTestResult
} from './utils.js';

export let options = {
  stages: [
    { duration: '2m', target: config.users.load }, // Ramp up
    { duration: config.durations.load, target: config.users.load }, // Stay at load
    { duration: '2m', target: 0 }, // Ramp down
  ],
  thresholds: config.thresholds
};

export default function () {
  const baseUrl = config.baseUrl;

  // Scenario 1: Browse data models with pagination
  testDataModelsPagination(baseUrl);
  randomSleep(1, 3);

  // Scenario 2: Get specific data model details
  testDataModelDetails(baseUrl);
  randomSleep(1, 3);

  // Scenario 3: Browse entities
  testEntitiesPagination(baseUrl);
  randomSleep(1, 3);

  // Scenario 4: Search functionality
  testSearchFunctionality(baseUrl);
  randomSleep(1, 3);

  // Scenario 5: Get value sets
  testValueSets(baseUrl);
  randomSleep(2, 4);

  // Scenario 6: Test integration endpoints
  testIntegrationEndpoints(baseUrl);
  randomSleep(1, 3);

  // Scenario 7: Test data model related endpoints
  testDataModelRelatedEndpoints(baseUrl);
  randomSleep(1, 3);

  // Scenario 8: Test attribute endpoints
  testAttributeEndpoints(baseUrl);
  randomSleep(1, 2);

  // Scenario 9: Test transformation endpoints
  testTransformationEndpoints(baseUrl);
  randomSleep(2, 4);

  // Scenario 10: Test value mapping endpoints
  testValueMappingEndpoints(baseUrl);
  randomSleep(1, 2);
}

function testDataModelsPagination(baseUrl) {
  const page = testDataGenerator.randomArrayElement(config.testData.pagination.pages);
  const size = testDataGenerator.randomArrayElement(config.testData.pagination.sizes);
  
  const response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/?page=${page}&size=${size}&pagination=true`,
    { headers },
    {
      'data models pagination works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  
  validatePaginationResponse(response);
  logTestResult(`Data Models Pagination (page=${page}, size=${size})`, response);
}

function testDataModelDetails(baseUrl) {
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  
  const response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/${dataModelId}`,
    { headers },
    {
      'data model details retrieved': (r) => r.status === 200 || r.status === 404,
      'response time acceptable': (r) => r.timings.duration < 1000
    }
  );
  
  if (response.status === 200) {
    validateEntityResponse(response, ['Name', 'DataModelVersion', 'Type']);
  }
  
  logTestResult(`Data Model Details (ID: ${dataModelId})`, response);
}

function testEntitiesPagination(baseUrl) {
  const page = testDataGenerator.randomArrayElement(config.testData.pagination.pages);
  const size = testDataGenerator.randomArrayElement(config.testData.pagination.sizes);
  
  const response = makeRequest(
    http.get,
    `${baseUrl}/entities/?page=${page}&size=${size}&pagination=true`,
    { headers },
    {
      'entities pagination works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  
  validatePaginationResponse(response);
  logTestResult(`Entities Pagination (page=${page}, size=${size})`, response);
}

function testSearchFunctionality(baseUrl) {
  const searchTerm = testDataGenerator.randomArrayElement(config.testData.searchTerms);
  
  const response = makeRequest(
    http.get,
    `${baseUrl}/search/?search_key=${searchTerm}`,
    { headers },
    {
      'search works': (r) => r.status === 200,
      'search response time acceptable': (r) => r.timings.duration < 2000,
      'search returns object': (r) => {
        try {
          const body = JSON.parse(r.body);
          return typeof body === 'object';
        } catch (e) {
          return false;
        }
      }
    }
  );
  
  logTestResult(`Search (term: ${searchTerm})`, response);
}

function testValueSets(baseUrl) {
  const page = testDataGenerator.randomArrayElement(config.testData.pagination.pages);
  const size = testDataGenerator.randomArrayElement(config.testData.pagination.sizes);
  
  const response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/?page=${page}&size=${size}&pagination=true`,
    { headers },
    {
      'value sets works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  
  validatePaginationResponse(response);
  logTestResult(`Value Sets (page=${page}, size=${size})`, response);
}

function testIntegrationEndpoints(baseUrl) {
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  
  // Test OpenAPI schema endpoint
  let response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/open_api_schema/${dataModelId}?include_attr_md=true`,
    { headers },
    {
      'open api schema works': (r) => r.status === 200 || r.status === 404,
      'response time acceptable': (r) => r.timings.duration < 2000
    }
  );
  logTestResult(`OpenAPI Schema (ID: ${dataModelId})`, response);
  
  // Test transformations for data models
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/transformations_for_data_models/?source_data_model_id=26&target_data_model_id=17&size=100`,
    { headers },
    {
      'transformations for data models works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 3000
    }
  );
  logTestResult('Transformations for Data Models', response);
}

function testDataModelRelatedEndpoints(baseUrl) {
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  
  // Test entities by data model
  let response = makeRequest(
    http.get,
    `${baseUrl}/entities/by_data_model_id/${dataModelId}?pagination=false`,
    { headers },
    {
      'entities by data model works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  logTestResult(`Entities by Data Model (ID: ${dataModelId})`, response);
  
  // Test attributes by data model
  response = makeRequest(
    http.get,
    `${baseUrl}/attributes/by_data_model_id/${dataModelId}?pagination=false`,
    { headers },
    {
      'attributes by data model works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  logTestResult(`Attributes by Data Model (ID: ${dataModelId})`, response);
  
  // Test entity associations by data model
  response = makeRequest(
    http.get,
    `${baseUrl}/entity_associations/by_data_model_id/${dataModelId}?pagination=false&allow_empty=true`,
    { headers },
    {
      'entity associations by data model works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  logTestResult(`Entity Associations by Data Model (ID: ${dataModelId})`, response);
  
  // Test entity attribute associations by data model
  response = makeRequest(
    http.get,
    `${baseUrl}/entity_attribute_associations/by_data_model_id/${dataModelId}?pagination=false`,
    { headers },
    {
      'entity attribute associations by data model works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  logTestResult(`Entity Attribute Associations by Data Model (ID: ${dataModelId})`, response);
}

function testAttributeEndpoints(baseUrl) {
  // Test attributes listing
  let response = makeRequest(
    http.get,
    `${baseUrl}/attributes?pagination=false`,
    { headers },
    {
      'attributes listing works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1000
    }
  );
  logTestResult('Attributes Listing', response);
  
  // Test specific attribute by ID
  const attributeId = testDataGenerator.randomArrayElement(config.testData.attributeIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/attributes/${attributeId}`,
    { headers },
    {
      'specific attribute retrieval works': (r) => r.status === 200 || r.status === 404,
      'response time acceptable': (r) => r.timings.duration < 800
    }
  );
  logTestResult(`Specific Attribute (ID: ${attributeId})`, response);
  
  // Test attributes by entity
  const entityId = testDataGenerator.randomArrayElement(config.testData.entityIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/attributes/by_entity_id/${entityId}`,
    { headers },
    {
      'attributes by entity works': (r) => r.status === 200 || r.status === 404,
      'response time acceptable': (r) => r.timings.duration < 1000
    }
  );
  logTestResult(`Attributes by Entity (ID: ${entityId})`, response);
}

function testTransformationEndpoints(baseUrl) {
  // Test transformation groups listing
  let response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups?pagination=false`,
    { headers },
    {
      'transformation groups listing works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  logTestResult('Transformation Groups Listing', response);
  
  // Get a random transformation group ID for detailed tests
  const transformationGroupId = testDataGenerator.randomArrayElement(config.testData.transformationGroupIds);
  
  // Test transformation groups source and target
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/${transformationGroupId}/source_and_target`,
    { headers },
    {
      'transformation groups source and target works': (r) => r.status === 200 || r.status === 404,
      'response time acceptable': (r) => r.timings.duration < 1200
    }
  );
  logTestResult(`Transformation Groups Source and Target (ID: ${transformationGroupId})`, response);
  
  // Test transformation groups transformations
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/${transformationGroupId}/transformations`,
    { headers },
    {
      'transformation groups transformations works': (r) => r.status === 200 || r.status === 404,
      'response time acceptable': (r) => r.timings.duration < 1500
    }
  );
  logTestResult(`Transformation Groups Transformations (ID: ${transformationGroupId})`, response);
  
  // Test transformations for data models
  response = makeRequest(
    http.get,
    `${baseUrl}/transformations_for_data_models?source_data_model_id=1&target_data_model_id=17`,
    { headers },
    {
      'transformations for data models works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 2000
    }
  );
  logTestResult('Transformations for Data Models', response);
}

function testValueMappingEndpoints(baseUrl) {
  // Test value mappings with pagination
  let response = makeRequest(
    http.get,
    `${baseUrl}/value_mappings?page=1&size=25`,
    { headers },
    {
      'value mappings listing works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1200
    }
  );
  logTestResult('Value Mappings Listing', response);
  
  // Test value mappings by transformation group
  const transformationGroupId = testDataGenerator.randomArrayElement(config.testData.transformationGroupIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/value_mappings/by_transformation_group/${transformationGroupId}`,
    { headers },
    {
      'value mappings by transformation group works': (r) => r.status === 200 || r.status === 404,
      'response time acceptable': (r) => r.timings.duration < 1000
    }
  );
  logTestResult(`Value Mappings by Transformation Group (ID: ${transformationGroupId})`, response);
  
  // Test value set values
  response = makeRequest(
    http.get,
    `${baseUrl}/value_set_values?pagination=false`,
    { headers },
    {
      'value set values listing works': (r) => r.status === 200,
      'response time acceptable': (r) => r.timings.duration < 1000
    }
  );
  logTestResult('Value Set Values Listing', response);
}

export function teardown() {
  console.log('Load test completed');
}