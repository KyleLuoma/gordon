#!/bin/bash

# Build Backend
cd ./app
docker kill backend
docker rm backend
docker build --rm --no-cache -t backend .
cd ..

# Start the web server backend 
docker run -dit --name backend -p 8000:8000 --network web-app-net --hostname backend backend