#!/bin/bash

# Build Backend
cd ./app
docker kill backend
docker rm backend
docker build --rm --no-cache -t backend .
cd ..

# Start the web server backend 
docker run -dit --name backend --network web-app-net --hostname backend backend