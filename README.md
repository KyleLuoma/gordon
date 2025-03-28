## Cooking and Shopping Assistant
A web-based, AI-enabled, system for extracting ingredients from recipes and combining them into accurate and useful shopping lists.

### Project Goals

1. Extract ingredients from unstructured recipe data and store in a common format with common names and units of measurement
2. Given a selected set of recipes, build a shopping list organized by categories that align to sections in a grocery store
3. A web UI with:
  a. A recipe selector / checklist
  b. A generated shopping list that responds to selected recipes
  c. A recipe upload / ingest tool (can be local document or website url)
  d. Modes: recipe organization, shopping list building, shopping in a store


### Deploying
You can launch the entire stack by running  ```bash launch_web_server.sh``` script, which will build and launch two containers:
  1. A Python image backend that will deploy your app from ```/app``` using Gunicorn
  2. A Nginx image frontend that will deploy your static page from ```/web_public``` using Nginx.

### Configuring and building
I am trying to keep this simple, so configure your containers in the launch scripts, configure the Nginx routes in ```/proxy.conf```, 
and build your Flask app inside the ```/app``` folder, being sure to keep requirements.txt updated.

## Disclaimers
1. The htmx script is stored locally in the /web_public/js folder. It will be up to the user to make sure this is the correct version for your use case.