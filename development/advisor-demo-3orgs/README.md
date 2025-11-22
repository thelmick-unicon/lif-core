# `development/advisor-demo-3orgs` Directory

This directory contains the developer version of the Docker Compose deployment for the AI Advisor.
This version captures the two additional source organizations.

Note: the deployment reaches into other directories to build images.

## Usage

To run the demo, starting at the root of the repo:
```
cd development/advisor-demo-3orgs
docker-compose up --build
docker-compose up --build -d
```

To test, visit: http://localhost:5174/

Shutting the demo down is:
```
docker-compose down -v
```

## Developer Notes

Developers may want expose services to the host system for direct access and testing.
This can be done by adding a "ports:" section to the service in question.
This may also need adding a "driver: bridge" sub-attribute to the network.

If a component needs access to the host system, add the following the component:
```
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

## Notes
See docker-compose documentation for other usage scenarios.