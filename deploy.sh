#!/bin/bash
set -e

# Load environment variables if using a .env file
export $(grep -v '^#' .env | xargs)

echo "Logging into ECR..."
aws ecr get-login-password --region "$AWS_ECR_DEFAULT_REGION" \
  | docker login --username AWS --password-stdin "$ECR_URI"

echo "Pulling latest image..."
docker compose pull

echo "Restarting containers..."
docker compose up -d

echo "Deployment complete."
