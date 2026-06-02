#!/bin/bash

# Build Frontend / Proxy container
docker kill nginx
docker rm nginx
docker build --rm --no-cache -t nginx .

# Start the web server frontend / proxy
docker run -it --name nginx -p 0.0.0.0:8080:80 --network web-app-net --hostname nginx nginx