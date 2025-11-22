// Load Test Suite
// Tests GraphQL API performance under normal expected load
import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from './k6.config.js';
import { 
  makeGraphQLRequest, 
  createPersonGraphQLQuery,
  getRandomTestPerson,
  randomSleep, 
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
  
  // Test GraphQL API under load with random person data
  testGraphQLPersonQueryLoad(baseUrl);
  randomSleep(1, 3);
}

function testGraphQLPersonQueryLoad(baseUrl) {
  // Get random person from config test data
  const { personId, expectedOrgTypes } = getRandomTestPerson();
  
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
      'response time under load acceptable': (r) => r.timings.duration < 3000
    }
  );
  
  if (Math.random() < 0.1) { // Log 10% of requests to avoid spam
    logTestResult(`GraphQL Person Query Load Test - Person ${personId}`, response);
  }
}

export function teardown() {
  console.log('Load test completed - GraphQL API performance under normal load verified');
}