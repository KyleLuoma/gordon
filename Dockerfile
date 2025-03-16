FROM nginx:latest
COPY ./web_public /usr/share/nginx/html
COPY ./proxy.conf /etc/nginx/conf.d/default.conf

