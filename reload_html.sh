#!/bin/bash
docker exec nginx rm -r /usr/share/nginx/html
docker cp ./web_public nginx:/usr/share/nginx/html