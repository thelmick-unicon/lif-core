# Dagster OSS for AWS

This project defines the *Dagster OSS*-focused deployment artifacts, used in the reference deployment on AWS. This flow is similar to the 'Dagster OSS Docker Compose' project. Please refer to that readme ( `projects/dagster_docker_compose/README.md` ) for general details. This readme will focus on any differences.

The deployment of Dagster OSS for AWS and the related Orchestrator and Adapters are handled in two parts:
- ECR / ECS for hosting and running the services. The build and deployment scripts are located in: `.github/workflows/`
- CloudFormation scripts for deploying the stacks are located in: `cloudformation/`

## ECR definitions

**Web Server**:
`projects/dagster_oss_ecs/Dockerfile.dagster`

**Daemon**:
`projects/dagster_oss_ecs/Dockerfile.dagster`

**Code Location**:
`projects/dagster_oss_ecs/Dockerfile.code_location`

## Database definitions

**PostgreSQL**:
`sam/dagster-database`
