#!/bin/bash
set -x

echo "Starting entrypoint script..."

# For operating in AWS, pass config via ssm
if [ ! -z "${LIF_QUERY_PLANNER_INFORMATION_SOURCES_CONFIG_YAML_SSM}" ]; then
  mkdir -p /opt/app
  echo "${LIF_QUERY_PLANNER_INFORMATION_SOURCES_CONFIG_YAML_SSM}" > /opt/app/information_sources_config.yml
  export LIF_QUERY_PLANNER_INFORMATION_SOURCES_CONFIG_PATH=/opt/app/information_sources_config.yml
fi

# If not in AWS, a local env should supply an information sources config file
if [ "foo" = "${LIF_QUERY_PLANNER_INFORMATION_SOURCES_CONFIG_PATH:=foo}" ]; then
  echo "Missing env variable: LIF_QUERY_PLANNER_INFORMATION_SOURCES_CONFIG_PATH"
  echo "Where is the information sources config file?"
  exit 1    
fi

# Wait until config path exists
while [ ! -f "$LIF_QUERY_PLANNER_INFORMATION_SOURCES_CONFIG_PATH" ]; do
  echo "waiting for $LIF_QUERY_PLANNER_INFORMATION_SOURCES_CONFIG_PATH to exist"
  sleep 15
done

# Log config file contents (for debugging)
echo "Information Sources Config file contents: "
cat "$LIF_QUERY_PLANNER_INFORMATION_SOURCES_CONFIG_PATH"

# Start Uvicorn
exec uvicorn lif.query_planner_restapi.core:app --host 0.0.0.0 --port 8002 "$@"
