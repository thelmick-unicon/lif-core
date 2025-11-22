// Smoke Test Suite
// Basic functionality test to ensure the API is working
import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from './k6.config.js';
import { makeRequest, headers, logTestResult, testDataGenerator } from './utils.js';

export let options = {
  stages: [
    { duration: '1m', target: config.users.smoke }
  ],
  thresholds: config.thresholds
};

export default function () {
  const baseUrl = config.baseUrl;

  // Test 1: Health Check
  let response = makeRequest(
    http.get,
    `${baseUrl}/health-check`,
    { headers },
    {
      'health check status is 200': (r) => r.status === 200,
      'health check has message': (r) => {
        const body = JSON.parse(r.body);
        return body.hasOwnProperty('message');
      }
    }
  );
  logTestResult('Health Check', response);

  sleep(1);

  // Test 2: Get Data Models (basic endpoint)
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/?pagination=false`,
    { headers },
    {
      'datamodels endpoint works': (r) => r.status === 200,
      'response has data': (r) => {
        const body = JSON.parse(r.body);
        return body.hasOwnProperty('data');
      }
    }
  );
  logTestResult('Get Data Models', response);

  sleep(1);

  // Test 3: Get Entities
  response = makeRequest(
    http.get,
    `${baseUrl}/entities/?pagination=false`,
    { headers },
    {
      'entities endpoint works': (r) => r.status === 200
    }
  );
  logTestResult('Get Entities', response);

  sleep(1);

  // Test 4: Get Value Sets
  response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/?pagination=false`,
    { headers },
    {
      'value sets endpoint works': (r) => r.status === 200
    }
  );
  logTestResult('Get Value Sets', response);

  sleep(1);

  // Test 5: Search functionality
  const searchTerm = 'name';
  response = makeRequest(
    http.get,
    `${baseUrl}/search/?search_key=${searchTerm}`,
    { headers },
    {
      'search endpoint works': (r) => r.status === 200,
      'search returns results': (r) => {
        const body = JSON.parse(r.body);
        return typeof body === 'object';
      }
    }
  );
  logTestResult('Search', response);

  sleep(1);

  // Test 6: Data model with details
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/with_details/${dataModelId}`,
    { headers },
    {
      'data model with details endpoint works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult('Get Data Model with Details', response);

  sleep(1);

  // Test 7: Entities by data model
  response = makeRequest(
    http.get,
    `${baseUrl}/entities/by_data_model_id/${dataModelId}?pagination=false`,
    { headers },
    {
      'entities by data model endpoint works': (r) => r.status === 200
    }
  );
  logTestResult('Get Entities by Data Model', response);

  sleep(1);

  // Test 8: Transformation groups data models
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/data_models/`,
    { headers },
    {
      'transformation groups data models endpoint works': (r) => r.status === 200
    }
  );
  logTestResult('Get Transformation Groups Data Models', response);

  sleep(1);

  // Test 9: OrgLIF data models
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/orglif/`,
    { headers },
    {
      'orglif data models endpoint works': (r) => r.status === 200
    }
  );
  logTestResult('Get OrgLIF Data Models', response);

  sleep(2);

  // Test 10: Additional endpoint checks  
  response = makeRequest(
    http.get,
    `${baseUrl}/attributes?pagination=false`,
    { headers },
    {
      'attributes endpoint works': (r) => r.status === 200
    }
  );
  logTestResult('Get Attributes', response);

  sleep(1);

  // Test 11: Value set values
  response = makeRequest(
    http.get,
    `${baseUrl}/value_set_values?pagination=false`,
    { headers },
    {
      'value set values endpoint works': (r) => r.status === 200
    }
  );
  logTestResult('Get Value Set Values', response);

  sleep(1);

  // Test 12: Entity associations
  
  // Test specific entity association by ID
  const entityAssociationId = testDataGenerator.randomArrayElement(config.testData.entityAssociationIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/entity_associations/${entityAssociationId}`,
    { headers },
    {
      'entity associations by id endpoint works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult('Get Entity Association by ID', response);
}

export function teardown() {
  console.log('Smoke test completed - all critical endpoints verified');
}