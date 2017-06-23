[![build status](https://gitlab.com/patkennedy79/flask_recipe_app/badges/master/build.svg)](https://gitlab.com/patkennedy79/flask_recipe_app/commits/master)
[![coverage report](https://gitlab.com/patkennedy79/flask_recipe_app/badges/master/coverage.svg)](https://gitlab.com/patkennedy79/flask_recipe_app/commits/master)
[![say thanks](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/patkennedy79)
## Synopsis

Family Recipe web application for keeping track of your favorite recipes.

## Website
http://www.kennedyfamilyrecipes.com

## What Does This Tool Do?
Keeps track of all your recipes.

## How to Run (Development)

1. Create the Dockerfile for the postgres service

- % cd ./flask_recipe_app/web/
- % python create_postgres_dockerfile.py
- % cd ..

2. Build and run the Docker containers

- % docker-compose build
- % docker-compose up -d

3. Create or re-initialize the database

- % docker-compose run --rm web python ./instance/db_create.py

Go to your favorite web browser and open:
    http://192.168.99.100:5000  $ Check the IP address using 'docker-machine ip'

## Key Python Modules Used

- Flask - web framework
- Jinga2 - templating engine
- SQLAlchemy - ORM (Object Relational Mapper)
- Flask-Bcrypt - password hashing
- Flask-Login - support for user management
- Flask-Migrate - database migrations
- Flask-WTF - simplifies forms
- itsdangerous - helps with user management, especially tokens

This application is written using Python 3.6.1.  The database used is PostgreSQL.

Docker is the recommended tool for running in development and production.

## Unit Testing

In the top-level folder:
    % nose2

For running a specific module:
    % nose2 -v project.tests.test_recipes_api