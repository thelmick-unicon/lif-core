# `deployments/advisor-demo-docker` Directory

This directory contains the Docker Compose deployment for the AI Advisor demo for a local version of the demo.

## Pre-requisites

### Environment

An OpenAI key is needed to test the advisor chatbot.
```
export OPENAI_API_KEY=your_openai_key_here
```

### Tooling

The following tools are required to run this deployment:

- **Docker**: Version 20.10 or later
  - Install from [Docker Desktop](https://www.docker.com/products/docker-desktop/) or use your package manager
  - Ensure Docker daemon is running

- **Docker Compose**: Version 2.0 or later
  - Usually included with Docker Desktop
  - Can be installed separately if needed

- **uv**: Python package manager (used in Dockerfiles for building Python services)
  - Automatically installed during Docker build process
  - No manual installation required

### System Requirements

- **Available ports**: The deployment uses the following external ports:
  - `5174`: Frontend application (lif-advisor-app)
  - `8004`: Advisor API

- **Memory**: At least 4GB RAM recommended for running all services
- **Disk space**: At least 2GB free space for Docker images and volumes

## Usage

Note: the deployment reaches into other directories to build images.

To run the demo, starting at the root of the repo:
```
cd deployments/advisor-demo-docker
docker-compose up --build
```

To run it as a background task, add `-d`:
```
cd deployments/advisor-demo-docker
docker-compose up --build -d
```

To test, visit: http://localhost:5174/

Shutting the demo down is:
```
docker-compose down -v
```

## Notes
See docker-compose documentation for other usage scenarios.