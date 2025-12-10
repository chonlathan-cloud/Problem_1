#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Build the backend Docker image
echo "Building backend Docker image..."
docker build -f Dockerfile.backend -t accounting-backend .

# Build the frontend Docker image
echo "Building frontend Docker image..."
docker build -f Dockerfile.frontend -t accounting-frontend .

# Run the Docker containers using docker compose
echo "Starting Docker containers..."
docker compose down
docker compose up --build -d

echo "Deployment complete. Backend at http://localhost:8000, Frontend at http://localhost:80."
