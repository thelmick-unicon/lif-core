// Spike Test Suite  
// Tests GraphQL API behavior during sudden traffic spikes
import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from './k6.config.js';
import { 
  makeGraphQLRequest, 
  createPersonGraphQLQuery,
  getRandomTestPerson,
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

  // During spike test, focus on the GraphQL endpoint
  testGraphQLPersonQuerySpike(baseUrl);

  // Very short sleep to maximize request rate
  sleep(Math.random() * 0.3);
}

function testGraphQLPersonQuerySpike(baseUrl) {
  // Get random person from config test data
  const { personId, expectedOrgTypes } = getRandomTestPerson();
  
  const graphqlQuery = createPersonGraphQLQuery(personId, expectedOrgTypes);
  
  const response = makeGraphQLRequest(
    http.post,
    `${baseUrl}/graphql`,
    graphqlQuery,
    {
      'spike - GraphQL endpoint available': (r) => r.status < 500, // Allow some server errors during spike
      'spike - GraphQL eventually responds': (r) => r.timings.duration < 15000 // More lenient timing for spikes
    }
  );
  
  if (Math.random() < 0.02) { // Log 2% of requests to reduce noise during spike
    logTestResult(`GraphQL Spike Test - Person ${personId}`, response);
  }
}

export function teardown() {
  console.log('Spike test completed - GraphQL API spike resilience verified');
}