# Description
Git repository for the ISDS 454 project at CSUF, Team A. Built using Python Flask, HTML, CSS, JavaScript, and jQuery. Hosted on a Vultr VPS running Ubuntu Server. Data is stored in a PostgreSQL database. Served using a Caddy reverse proxy, static files are served using an NGINX webserver. The Flask app, NGINX webserver, Postgres database, and Caddy reverse proxy are all containerized with Docker and deployed using docker-compose from a Git repository.

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