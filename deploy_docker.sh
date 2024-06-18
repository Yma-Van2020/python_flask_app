#!/bin/bash

# Define variables
IMAGE_NAME="flask-app"
CONTAINER_NAME="flask-app-container"
HOST_PORT=5000
CONTAINER_PORT=5000

# Navigate to the project directory
cd ~/flask-app

# Build the Docker image
docker build -t $IMAGE_NAME .

# Stop and remove any existing containers with the same name
docker rm -f $CONTAINER_NAME

# Run the Docker container
docker run -d --name $CONTAINER_NAME -p $HOST_PORT:$CONTAINER_PORT $IMAGE_NAME
