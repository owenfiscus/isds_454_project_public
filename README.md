# Description
Git repository for the ISDS 454 project at CSUF, Team A. Built using Python Flask, HTML, CSS, JavaScript, and jQuery. Hosted on a Vultr VPS running Ubuntu Server. Data is stored in a PostgreSQL database. Served using a Caddy reverse proxy, static files are served using an NGINX webserver. The Flask app, NGINX webserver, Postgres database, and Caddy reverse proxy are all containerized with Docker and deployed using docker-compose from a Git repository.

# Navigation

This GitHub repository is organized in such a way that it can be deployed almost immediately after cloning the repository. If you wish to take a look at some of the most important portions of the code, we recommend that you look at our Python backend application and the JavaScript files used in the front end. Additionally you may look at the HTML and CSS files. Here are the paths for each of those.

Python: /back/src/api/app/__init.py__
JavaScript: /back/src/api/app/static/scripts/
HTML: /back/src/api/app/templates/
CSS: JavaScript: /back/src/api/app/static/scripts/styles.css

Of course, you should feel free to take a look at any portions of the source code that you wish.

# Website Link

[Nutwood Auto Group](https://nutwoodauto.group/)

# Deploying

Clone this project, edit both `.env` files with the correct credentials. The Caddyfile will need to be altered depending on your hosting confguration.

Enter the local Git repository and use `docker-compose` to deploy using the following commands.

``` bash
cd back &&
docker-compose --env-file ./.env up -d --build

cd ../front &&
docker-compose up -d
```