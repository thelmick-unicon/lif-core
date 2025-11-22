# Authentication

## Overview

This project implements a JWT-based authentication system similar to the LIF Advisor app. The system includes:

- Login/logout functionality via JWT tokens
- Automatic frontend token refresh
- Protected API endpoints by LIF service

## Backend Authentication

### Authentication Endpoints

- `POST /login` - Login with username/password
- `POST /logout` - Logout (requires authentication)
- `POST /refresh-token` - Refresh access token
- `GET /health-check` - Health check endpoint

### Demo Users

The system includes three demo users, hard coded into the Github repo. Currently there is only authN, not authZ, so all users have the same abilities in MDR. 

```json
{
  "username": "atsatrian_lifdemo@stateu.edu",
  "password": "liffy4life!",
  "firstname": "Alan",
  "lastname": "Tsatrian"
}
```

```json
{
  "username": "jdiaz_lifdemo@stateu.edu",
  "password": "liffy4life!",
  "firstname": "Jenna",
  "lastname": "Diaz"
}
```

```json
{
  "username": "smarin_lifdemo@stateu.edu",
  "password": "liffy4life!",
  "firstname": "Sarah",
  "lastname": "Marin"
}
```

### Securing API Endpoints

All endpoints are secured by default, requiring either an API service token or a JWT access token.

Exceptions can be configured by adjusting one of the following configurations. Note the option of allowing an exact context path versus allowing a context path that starts with a given string.

```dotenv
MDR__AUTH__PUBLIC_ALLOWLIST_EXACT="/login,/refresh-token,/health-check"
MDR__AUTH__PUBLIC_ALLOWLIST_STARTS_WITH="/docs,/openapi.json"
```

## Frontend Authentication

Ensure you configure `MDR__AUTH__JWT_SECRET_KEY` to be a hard to guess value. This is used to build the JWT access and refresh tokens.

### Login Component

The frontend provides a login page at `/login` with:
- Username/password fields
- Error handling
- Automatic redirection after login

### Protected Routes

By default, all routes except `/login`, `/refresh-token`, `/health-check`, `/docs*`, and `/openapi.json*` are protected and require authentication.

### Automatic Token Refresh

The frontend automatically refreshes tokens when they expire, providing a seamless user experience.

### User Context

Access current user information anywhere in the React app:

```tsx
import { useAuth } from "../context/AuthContext";

function MyComponent() {
  const { user, isAuthenticated, logout } = useAuth();
  
  return (
    <div>
      {isAuthenticated && (
        <p>Welcome, {user?.firstname} {user?.lastname}!</p>
      )}
    </div>
  );
}
```

## Development

### Testing Authentication in the Browser

1. Start the backend server
2. Start the frontend development server
3. Navigate to the application
4. You'll be redirected to `/login`
5. Use any of the demo credentials to log in
6. You'll be redirected to the main application

## Testing Authentication with cURL

Use the test endpoint to verify your authentication:

```bash
# Test with JWT token
curl -X GET "http://localhost:8000/test/auth-info" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Test with API key
curl -X GET "http://localhost:8000/test/auth-info" \
  -H "X-API-Key: translator_key_67890"
```

## Security Notes

- JWT tokens (access and refresh) are stored in localStorage
- Refresh tokens allow seamless token renewal
- All protected endpoints return 401 for invalid/expired tokens
- The frontend automatically handles token refresh and logout on auth failure
