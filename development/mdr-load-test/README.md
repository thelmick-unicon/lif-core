# Load Testing with k6

This directory contains a comprehensive k6 test suite for performance testing the metadata-repo-api. The test suite includes smoke tests, functional tests, load tests, stress tests, and spike tests to ensure the API performs well under various conditions.

## Test Suite Overview

The test suite consists of the following components:

- **smoke-test.js** - Basic functionality verification with minimal load
- **functional-test.js** - Comprehensive functional testing of all API endpoints
- **load-test.js** - Performance testing under normal expected load
- **stress-test.js** - High-load testing to find breaking points
- **spike-test.js** - Sudden traffic spike testing
- **k6.config.js** - Centralized configuration for all tests
- **utils.js** - Utility functions and helpers
- **run-tests.sh** - Convenient test runner script
- **results/** - Directory for automatic JSON output files (auto-created)

## Prerequisites

1. Install [k6](https://grafana.com/docs/k6/latest/set-up/install-k6/)
2. Setup Database and API (see repo [README.md](../README.md))
3. Ensure the metadata-repo-api is running at `http://localhost:8081` (or set `API_BASE_URL` environment variable)

## Quick Start

### Using the Test Runner Script (Recommended)

```bash
# Make the script executable (if not already done)
chmod +x run-tests.sh

# Run smoke test
./run-tests.sh smoke

# Run all tests (each creates timestamped JSON output)
./run-tests.sh all

# Run load test against a different API URL (with automatic JSON output)
./run-tests.sh -u http://your-api-host:8081 load

# Run stress test with custom output filename
./run-tests.sh -o custom_results.json stress
```

### Running Tests Directly with k6

```bash
# Set the API base URL (optional, defaults to http://localhost:8081)
export API_BASE_URL=http://localhost:8081

# Run individual tests
k6 run smoke-test.js
k6 run functional-test.js
k6 run load-test.js
k6 run stress-test.js
k6 run spike-test.js
```

## Test Types Explained

### 1. Smoke Test (`smoke-test.js`)
- **Purpose**: Quick verification that the API is working
- **Duration**: ~30 seconds
- **Load**: 1 virtual user
- **Use Case**: Run after deployments or code changes

### 2. Functional Test (`functional-test.js`)
- **Purpose**: Comprehensive testing of all API endpoints
- **Duration**: ~1 minute
- **Load**: 1 virtual user
- **Use Case**: Validate API functionality and endpoint coverage

### 3. Load Test (`load-test.js`)
- **Purpose**: Test performance under normal expected load
- **Duration**: ~5 minutes
- **Load**: 10 virtual users
- **Use Case**: Validate performance under typical usage patterns

### 4. Stress Test (`stress-test.js`)
- **Purpose**: Find system breaking points under high load
- **Duration**: ~10 minutes
- **Load**: Up to 50 virtual users
- **Use Case**: Determine maximum system capacity

### 5. Spike Test (`spike-test.js`)
- **Purpose**: Test behavior during sudden traffic spikes
- **Duration**: ~2 minutes
- **Load**: Sudden spike to 100 virtual users
- **Use Case**: Validate system resilience during traffic bursts

## Configuration

### Environment Variables (.env file)

The test suite supports environment variables via a `.env` file for easy configuration. Copy `.env.example` to `.env` and modify as needed:

```bash
# Copy the example file
cp .env.example .env

# Edit the configuration
nano .env
```

Example `.env` file:
```bash
# API Configuration
API_BASE_URL=https://mdr-api.lif.unicon.net

# Test Configuration (optional overrides)
SMOKE_DURATION=30s
LOAD_DURATION=5m
STRESS_DURATION=10m
SPIKE_DURATION=2m

SMOKE_USERS=1
LOAD_USERS=10
STRESS_USERS=50
SPIKE_USERS=100

# Output Configuration
ENABLE_JSON_OUTPUT=true
OUTPUT_DIR=./results
INCLUDE_TIMESTAMP=true
```

**Note**: The `run-tests.sh` script automatically loads environment variables from the `.env` file if it exists.

### Manual Environment Variables

Alternatively, you can set environment variables manually:

- `API_BASE_URL`: Base URL of the API (default: `http://localhost:8081`)
- `SMOKE_DURATION`, `LOAD_DURATION`, etc.: Override test durations
- `SMOKE_USERS`, `LOAD_USERS`, etc.: Override virtual user counts

### Test Configuration (`k6.config.js`)

Key configuration options:

```javascript
export const config = {
  baseUrl: 'http://localhost:8081',  // API base URL
  durations: {
    smoke: '30s',
    load: '5m',
    stress: '10m',
    spike: '2m'
  },
  users: {
    smoke: 1,
    load: 10,
    stress: 50,
    spike: 100
  },
  thresholds: {
    http_req_duration: ['p(95)<2000'],     // 95% requests under 2s
    http_req_failed: ['rate<0.01'],        // 99% success rate
    http_req_duration_avg: ['avg<500']     // Average under 500ms
  }
};
```

### Test Data Configuration

Update the `testData` section in `k6.config.js` to match your database:

```javascript
testData: {
  dataModelIds: [1, 2, 3, 4, 5],  // Valid data model IDs in your DB
  entityIds: [1, 2, 3, 4, 5],     // Valid entity IDs in your DB
  valueSetIds: [1, 2, 3, 4, 5],   // Valid value set IDs in your DB
  searchTerms: ['name', 'description', 'entity', 'attribute', 'value']
}
```

## API Endpoints Tested

The test suite covers all major API endpoints:

### Data Models
- `GET /datamodels/` - List data models with pagination and filters
- `GET /datamodels/{id}` - Get specific data model
- `GET /datamodels/with_details/{id}` - Get data model with details
- `GET /datamodels/open_api_schema/{id}` - Generate OpenAPI schema

### Entities
- `GET /entities/` - List entities with pagination
- `GET /entities/{id}` - Get specific entity

### Value Sets
- `GET /valuesets/` - List value sets with pagination
- `GET /valuesets/{id}` - Get specific value set

### Search
- `GET /search/` - Search across data models with various parameters

### Other Endpoints
- `GET /health-check` - Health check endpoint
- `GET /transformation_groups/` - Transformation groups
- `GET /value_mappings/` - Value mappings

## Test Results and Metrics

k6 provides comprehensive metrics including:

- **Response Time Metrics**: Average, min, max, percentiles (p95, p99)
- **Throughput Metrics**: Requests per second
- **Error Metrics**: Error rate, error types
- **Virtual User Metrics**: Active users, user lifecycle

### Understanding Thresholds

The tests include performance thresholds that define acceptable performance:

- `http_req_duration: ['p(95)<2000']` - 95% of requests must complete within 2 seconds
- `http_req_failed: ['rate<0.01']` - Less than 1% of requests should fail
- `http_req_duration_avg: ['avg<500']` - Average response time should be under 500ms

### Automatic JSON Output

**All tests now automatically generate JSON output with timestamps!**

When using the `run-tests.sh` script, JSON results are automatically saved to the `results/` directory with timestamped filenames:

```bash
# Automatic JSON output example
./run-tests.sh smoke
# Creates: results/smoke_test_20241013_143022.json

./run-tests.sh load  
# Creates: results/load_test_20241013_143545.json
```

### Custom Output Options

```bash
# Use custom output filename
./run-tests.sh -o custom_results.json stress

# Direct k6 command with JSON output
k6 run --out json=results.json load-test.js

# Save results to InfluxDB (if configured)
k6 run --out influxdb=http://localhost:8086/k6 load-test.js
```

### JSON Output Structure

The JSON output contains detailed metrics and can be used for:
- Performance analysis and trending
- Integration with monitoring systems
- Custom reporting and visualization
- CI/CD pipeline integration

## Troubleshooting

### Common Issues

1. **API Not Running**
   ```
   Error: Connection refused
   ```
   - Ensure metadata-repo-api is running on the expected port
   - Check if database is running and accessible

2. **High Error Rates**
   - Check API logs for errors
   - Verify database connectivity
   - Consider reducing load or increasing API resources

3. **Slow Response Times**
   - Check database performance
   - Look for resource bottlenecks (CPU, memory, network)
   - Consider database query optimization

### Debugging Tests

Enable verbose logging:
```bash
k6 run --verbose load-test.js
```

Add custom logging in tests:
```javascript
console.log(`Request to ${url} took ${response.timings.duration}ms`);
```

## Advanced Usage

### Custom Test Scenarios

Create custom test scenarios by modifying the existing files or creating new ones:

```javascript
import { config } from './k6.config.js';

export let options = {
  scenarios: {
    custom_scenario: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '1m', target: 20 },
        { duration: '5m', target: 20 },
        { duration: '1m', target: 0 },
      ],
    },
  },
};
```

## Best Practices

1. **Start Small**: Always run smoke tests before load tests
2. **Monitor Resources**: Watch CPU, memory, and database metrics during tests
3. **Gradual Scaling**: Increase load gradually to find breaking points
4. **Regular Testing**: Include performance tests in your CI/CD pipeline
5. **Realistic Data**: Use realistic test data that matches production patterns
6. **Environment Isolation**: Test against dedicated test environments when possible

## Contributing

When adding new tests:

1. Follow the existing patterns in the test files
2. Use the utility functions in `utils.js`
3. Add appropriate validations and error handling
4. Update this README with new test descriptions
5. Test your changes against a running API instance
