#!/bin/bash
IMAGE_NAME="typeclass"

echo "🛠️  Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" .

echo "🚪 Entering container..."
docker run -it --rm -v "$(pwd)":/app "$IMAGE_NAME"
