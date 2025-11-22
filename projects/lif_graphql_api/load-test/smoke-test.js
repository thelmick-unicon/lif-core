// Smoke Test Suite
// Basic functionality test to ensure the GraphQL API is working
import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from './k6.config.js';
import { makeGraphQLRequest, createPersonGraphQLQuery, getTestDataset, logTestResult } from './utils.js';

export let options = {
  stages: [
    { duration: '1m', target: config.users.smoke }
  ],
  thresholds: config.thresholds
};

export default function () {
  const baseUrl = config.baseUrl;

  // Test: GraphQL API with sample person query
  testGraphQLPersonQuery(baseUrl);
}

function testGraphQLPersonQuery(baseUrl) {
  // Use test data from config - select first person for smoke test
  const r1_demo_data = getTestDataset();
  const personId = Object.keys(r1_demo_data)[0]; // Use first person for consistency
  const expectedOrgTypes = r1_demo_data[personId];
  
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
          return body.data && body.data.person && body.data.person.length > 0;
        } catch (e) {
          return false;
        }
      },
      'response time acceptable': (r) => r.timings.duration < 5000
    }
  );
  
  logTestResult('GraphQL Person Query Smoke Test', response);
  sleep(1);
}

export function teardown() {
  console.log('Smoke test completed - GraphQL API endpoint verified');
}