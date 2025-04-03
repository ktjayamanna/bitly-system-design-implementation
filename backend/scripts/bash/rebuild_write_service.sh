#!/bin/bash

# Navigate to docker-compose directory
cd "$(dirname "$0")/../../../deployment/docker_compose"

# Stop and remove only the write service container
echo "Stopping write service..."
docker-compose stop write_service
docker-compose rm -f write_service

# Rebuild and start only the write service
echo "Rebuilding and starting write service..."
docker-compose up -d --build write_service

# Follow the logs
echo "Following write service logs... (Ctrl+C to exit)"
docker-compose logs -f write_service