// API Functional Test Suite
// Comprehensive functional testing of GraphQL API endpoint
import http from 'k6/http';
import { sleep } from 'k6';
import { config } from './k6.config.js';
import { 
  makeGraphQLRequest, 
  createPersonGraphQLQuery,
  getTestDataset,
  logTestResult
} from './utils.js';

export let options = {
  stages: [
    { duration: '1m', target: 1 }, // Single user functional testing
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000', 'avg<1000'],
    http_req_failed: ['rate<0.01']
  }
};

export default function () {
  const baseUrl = config.baseUrl;

  // Test the GraphQL API endpoint with various person queries
  testGraphQLPersonQueries(baseUrl);
  sleep(1);
}

function testGraphQLPersonQueries(baseUrl) {
  // Use test data from config
  const r1_demo_data = getTestDataset();
  
  // Test each person in the dataset
  Object.entries(r1_demo_data).forEach(([personId, expectedOrgTypes]) => {
    const graphqlQuery = createPersonGraphQLQuery(personId, expectedOrgTypes);
    
    const response = makeGraphQLRequest(
      http.post,
      `${baseUrl}/graphql`,
      graphqlQuery,
      {
        'GraphQL query returns success': (r) => r.status >= 200 && r.status < 300,
        'response has person data': (r) => {
          try {
            const body = JSON.parse(r.body);
            console.log(body);
            return body.data && body.data.person && body.data.person.length > 0;
          } catch (e) {
            return false;
          }
        }
      }
    );
    
    logTestResult(`GraphQL Functional Test - Person ${personId}`, response);
    sleep(0.5); // Short pause between individual tests
  });
}

export function teardown() {
  console.log('GraphQL API functional test completed');
}