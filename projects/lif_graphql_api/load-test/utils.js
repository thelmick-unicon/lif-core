// Utility functions for k6 tests
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';
import { config } from './k6.config.js';

// Custom metrics
export const errorRate = new Rate('errors');

/**
 * Make an HTTP request and validate the response
 * @param {Function} httpFunc - k6 HTTP function (http.get, http.post, etc.)
 * @param {string} url - Request URL
 * @param {Object} options - Request options (headers, body, etc.)
 * @param {Object} validations - Validation checks
 * @returns {Object} Response object
 */
export function makeRequest(httpFunc, url, options = {}, validations = {}) {
  const defaultValidations = {
    'status is 200': (r) => r.status === 200,
    'response time < 5s': (r) => r.timings.duration < 5000,
  };
  
  const allValidations = { ...defaultValidations, ...validations };
  
  const response = httpFunc(url, options);
  
  const result = check(response, allValidations);
  errorRate.add(!result);
  
  return response;
}

/**
 * Generate random test data
 */
export const testDataGenerator = {
  randomId: () => Math.floor(Math.random() * 100) + 1,
  randomString: (length = 10) => Math.random().toString(36).substring(2, length + 2),
  randomEmail: () => `test${Math.floor(Math.random() * 1000)}@example.com`,
  randomDate: () => new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
  randomBoolean: () => Math.random() > 0.5,
  randomArrayElement: (array) => array[Math.floor(Math.random() * array.length)],
  
  // Context-aware data model ID generation using config values
  randomDataModelId: (onlyExtension = false) => {
    // Use consolidated modelIds from config (1, 17)
    const modelIds = config.testData.modelIds;
    
    if (onlyExtension) {
      // Filter for extension data model IDs (17 is an extension type)
      const extensionIds = modelIds.filter(id => id === 17);
      return testDataGenerator.randomArrayElement(extensionIds.length > 0 ? extensionIds : modelIds);
    } else {
      return testDataGenerator.randomArrayElement(modelIds);
    }
  },
  
  // Generate test ID arrays for various endpoints
  randomEntityId: () => testDataGenerator.randomArrayElement(config.testData.entityIds),
  randomAttributeId: () => testDataGenerator.randomArrayElement(config.testData.attributeIds),
  randomValueSetId: () => testDataGenerator.randomArrayElement(config.testData.valueSetIds),
  randomValueId: () => testDataGenerator.randomArrayElement(config.testData.valueIds),
  randomTransformationGroupId: () => testDataGenerator.randomArrayElement(config.testData.transformationGroupIds),
  randomEntityAssociationId: () => testDataGenerator.randomArrayElement(config.testData.entityAssociationIds),
  randomEntityAttributeAssociationId: () => testDataGenerator.randomArrayElement(config.testData.entityAttributeAssociationIds),
  randomInclusionId: () => testDataGenerator.randomArrayElement(config.testData.inclusionIds),
  randomTransformationId: () => testDataGenerator.randomArrayElement(config.testData.transformationIds),
  randomValueMappingId: () => testDataGenerator.randomArrayElement(config.testData.valueMappingIds),
  randomValueSetValueId: () => testDataGenerator.randomArrayElement(config.testData.valueSetValueIds),
  randomDataModelConstraintId: () => testDataGenerator.randomArrayElement(config.testData.dataModelConstraintIds)
};

/**
 * GraphQL request headers
 */
export const graphqlHeaders = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'TargetGroup': config.targetGroup
};

/**
 * Create a GraphQL query for person data
 * @param {string} personId - Person identifier
 * @param {Array} orgTypes - Organization types for employment preferences 
 * @returns {Object} GraphQL query object
 */
export function createPersonGraphQLQuery(personId, orgTypes = []) {
  return {
    query: `
      query GetPerson($identifier: String!) {
        person(
          filter: {identifier: {identifier: $identifier, identifierType: "SCHOOL_ASSIGNED_NUMBER"}}
        ) {
          identifier {
            identifier
            identifierType
          }
          employmentPreferences {
            organizationTypes
          }
        }
      }
    `,
    variables: {
      identifier: personId
    }
  };
}

/**
 * Make a GraphQL request
 * @param {Function} httpFunc - k6 HTTP function (typically http.post)
 * @param {string} url - GraphQL endpoint URL  
 * @param {Object} query - GraphQL query object with query and variables
 * @param {Object} validations - Validation checks
 * @returns {Object} Response object
 */
export function makeGraphQLRequest(httpFunc, url, query, validations = {}) {
  const defaultValidations = {
    'status is 200': (r) => r.status === 200,
    'response time < 5s': (r) => r.timings.duration < 5000,
    'response is valid JSON': (r) => {
      try {
        JSON.parse(r.body);
        return true;
      } catch (e) {
        return false;
      }
    },
    'GraphQL response has no errors': (r) => {
      try {
        const body = JSON.parse(r.body);
        return !body.errors || body.errors.length === 0;
      } catch (e) {
        return false;
      }
    }
  };
  
  const allValidations = { ...defaultValidations, ...validations };
  const response = httpFunc(url, JSON.stringify(query), { headers: graphqlHeaders });
  
  const result = check(response, allValidations);
  errorRate.add(!result);
  
  return response;
}

/**
 * Get the test dataset from config
 * @returns {Object} The r1_demo_data object from config
 */
export function getTestDataset() {
  return config.testData.r1_demo_data;
}

/**
 * Get a random person from the test dataset
 * @returns {Object} Object with personId and expectedOrgTypes
 */
export function getRandomTestPerson() {
  const dataset = getTestDataset();
  const personIds = Object.keys(dataset);
  const randomPersonId = testDataGenerator.randomArrayElement(personIds);
  return {
    personId: randomPersonId,
    expectedOrgTypes: dataset[randomPersonId]
  };
}

/**
 * Sleep for a random duration between min and max seconds
 * @param {number} min - Minimum sleep time in seconds
 * @param {number} max - Maximum sleep time in seconds
 */
export function randomSleep(min = 1, max = 3) {
  const sleepTime = Math.random() * (max - min) + min;
  sleep(sleepTime);
}

/**
 * Validate pagination response structure
 * @param {Object} response - HTTP response
 * @returns {boolean} - Validation result
 */
export function validatePaginationResponse(response) {
  const body = JSON.parse(response.body);
  return check(response, {
    'has total field': () => body.hasOwnProperty('total'),
    'has data field': () => body.hasOwnProperty('data'),
    'data is array': () => Array.isArray(body.data),
    'total is number': () => typeof body.total === 'number'
  });
}

/**
 * Validate single entity response
 * @param {Object} response - HTTP response
 * @param {Array} requiredFields - Required fields in the response
 * @returns {boolean} - Validation result
 */
export function validateEntityResponse(response, requiredFields = []) {
  const body = JSON.parse(response.body);
  const validations = {
    'response has id': () => body.hasOwnProperty('Id') || body.hasOwnProperty('id')
  };
  
  requiredFields.forEach(field => {
    validations[`has ${field}`] = () => body.hasOwnProperty(field);
  });
  
  return check(response, validations);
}

/**
 * Log test results with enhanced error reporting
 * @param {string} testName - Name of the test
 * @param {Object} response - HTTP response
 */
export function logTestResult(testName, response) {
  const baseLog = `${testName}: Status ${response.status}, Duration: ${response.timings.duration}ms`;
  
  if (response.status >= 400) {
    // Log additional error details for failed requests
    try {
      const errorBody = JSON.parse(response.body);
      console.log(`${baseLog} - Error: ${JSON.stringify(errorBody)}`);
    } catch (e) {
      console.log(`${baseLog} - Error Body: ${response.body}`);
    }
  } else {
    console.log(baseLog);
  }
}

export default {
  makeRequest,
  makeGraphQLRequest,
  createPersonGraphQLQuery,
  getTestDataset,
  getRandomTestPerson,
  testDataGenerator,
  graphqlHeaders,
  randomSleep,
  validatePaginationResponse,
  validateEntityResponse,
  logTestResult,
  errorRate
};