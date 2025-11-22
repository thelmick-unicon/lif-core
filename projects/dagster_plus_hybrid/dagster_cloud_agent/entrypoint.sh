#!/bin/bash

# For operating in AWS, pass config via ssm
if [ ! -z "${DAGSTER_YAML_SSM}" ]; then
  mkdir -p /opt/dagster/app
  echo "${DAGSTER_YAML_SSM}" > /opt/dagster/app/dagster.yaml
  DAGSTER_YAML=/opt/dagster/app/dagster.yaml
fi

# If not in AWS, a local env should supply a dagster.yaml
if [ "foo" = "${DAGSTER_YAML:=foo}" ]; then
  echo "Missing env variable: DAGSTER_YAML"
  echo "Where is the dagster.yaml file?"
  exit 1    
fi

while [ ! -f "$DAGSTER_YAML" ]; do
  echo "waiting for $DAGSTER_YAML to exist"
  sleep 15
done

dagster_dir=$(dirname $DAGSTER_YAML)

dagster-cloud agent run $dagster_dir
