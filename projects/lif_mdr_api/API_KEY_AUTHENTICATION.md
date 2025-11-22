# API Key Authentication for Microservices

This document explains how to set up and use API key authentication for microservices that need to access your LIF Metadata Repository API endpoints.

## Overview

The system supports two types of authentication:
- **JWT Tokens**: For user authentication (React frontend)
- **API Keys**: For microservice authentication

## Setting an API Key

Currently, there are 3 service API keys available, and should be configured with hard to guess values. 

For now, there is only authN, not authZ, so all services have the same abilities in MDR.

```dotenv
MDR__AUTH__SERVICE_API_KEY__GRAPHQL=
MDR__AUTH__SERVICE_API_KEY__SEMANTIC_SEARCH=
MDR__AUTH__SERVICE_API_KEY__TRANSLATOR=
```

## Using API Keys in Microservices

### Python Example

```python
import requests

API_KEY = "translator_key_67890"
BASE_URL = "http://your-api-server:8000"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Make a request to any protected endpoint
response = requests.get(f"{BASE_URL}/datamodels", headers=headers)
print(response.json())
```

### Node.js Example

```javascript
const axios = require('axios');

const API_KEY = 'graphql_key_67890';
const BASE_URL = 'http://your-api-server:8000';

const headers = {
  'X-API-Key': API_KEY,
  'Content-Type': 'application/json'
};

// Make a request to any protected endpoint
axios.get(`${BASE_URL}/datamodels`, { headers })
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

### cURL Example

```bash
curl -X GET "http://localhost:8000/datamodels" \
  -H "X-API-Key: semantic_search_key_67890" \
  -H "Content-Type: application/json"
```

## Security Best Practices

1. **Store API keys securely**: Use environment variables or secure key management
2. **Rotate keys regularly**: Generate new keys periodically
3. **Use HTTPS**: Always use HTTPS in production
4. **Monitor usage**: Log API key usage for security monitoring
5. **Limit scope**: Consider implementing role-based access for different services

## Troubleshooting

1. **401 Unauthorized**: Check that your API key is correct
2. **Missing X-API-Key header**: Ensure your microservice is sending the header
