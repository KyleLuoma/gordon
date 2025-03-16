#!/bin/bash

# If you're having issues with the image recalling errors from some
# cache, then remove the image in 
# /var/lib/docker/image/overlay2/imagedb/content/sha256#
# that corresponds to the message 'writing image sha256:...'

# Create network
docker network create web-app-net

bash launch_backend.sh
bash launch_frontend.sh




