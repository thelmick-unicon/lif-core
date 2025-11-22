# Deployment

The Dagster Cloud Agent requires a configuration file, dagster.yaml.  The file contains sensitive information that we don't want to commit to a GitHub repo.  We'll use SSM parameter store for the configuration file, and a startup script will place the parameter contents into /opt/dagster/app/dagster.yaml upon startup.  This approach is limited to a 4K config file size. Special/weird characters might cause problems.  The parameter should be named "/<env>/DagsterCloudAgentConfig", encrypted using the environment KMS key.
