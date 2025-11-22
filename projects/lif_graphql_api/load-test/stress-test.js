// Stress Test Suite
// Tests GraphQL API performance under high load to find breaking points
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

  // Test GraphQL API under stress
  testGraphQLPersonQueryStress(baseUrl);

  // Shorter sleep times to increase load
  randomSleep(0.1, 1);
}

function testGraphQLPersonQueryStress(baseUrl) {
  // Get random person from config test data
  const { personId, expectedOrgTypes } = getRandomTestPerson();
  
  const graphqlQuery = createPersonGraphQLQuery(personId, expectedOrgTypes);
  
  const response = makeGraphQLRequest(
    http.post,
    `${baseUrl}/graphql`,
    graphqlQuery,
    {
      'GraphQL survives under stress': (r) => r.status >= 200 && r.status < 500, // Allow some 4xx errors under stress
      'response time under stress': (r) => r.timings.duration < 10000 // More lenient timing
    }
  );
  
  if (Math.random() < 0.05) { // Log 5% of requests to reduce noise
    logTestResult(`GraphQL Stress Test - Person ${personId}`, response);
  }
}

export function teardown() {
  console.log('Stress test completed - GraphQL API stress limits identified');
}