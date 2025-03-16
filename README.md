## Simple web stack setup
This is a base setup for a simple web stack that includes a Python + Flask-based backend serving to an HTMX-based frontend hosted by NGINX.

### Deploying
You can launch the entire stack by running  ```bash launch_web_server.sh``` script, which will build and launch two containers:
  1. A Python image backend that will deploy your app from ```/app``` using Gunicorn
  2. A Nginx image frontend that will deploy your static page from ```/web_public``` using Nginx.

### Configuring and building
I am trying to keep this simple, so configure your containers in the launch scripts, configure the Nginx routes in ```/proxy.conf```, 
and build your Flask app inside the ```/app``` folder, being sure to keep requirements.txt updated.

## Disclaimers
1. The htmx script is stored locally in the /web_public/js folder. It will be up to the user to make sure this is the correct version for your use case.