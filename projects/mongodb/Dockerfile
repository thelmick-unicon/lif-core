FROM mongodb/mongodb-community-server:8.0.10-ubuntu2204

# Switch to root user before installing
USER root


# Install jq
RUN apt-get update && \
    apt-get install -y jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add the seed data
COPY sample_data /seed_data

# Add the entrypoint script
COPY entrypoint.sh /docker-entrypoint-initdb.d/entrypoint.sh
RUN chmod +x /docker-entrypoint-initdb.d/entrypoint.sh
