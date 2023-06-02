# Tinder for Food 12:30

Link for demo: https://www.loom.com/share/392bc8bf72fa45a5bdfb9776304016d0

## Project Structure


`/.github/workflows` contains CI/CD code.

`/app` contains the application.

`/app/static` contains css/img/js files.

`/app/templates` contains html files.

`/app/__init__.py` is the project initializer file.

`/app/auth` contains the routes related to authentication.

`/app/models` contains the DB models using SQLAlchemy.

`/app/extensions.py` contains build-in extensions that are initialized in `__init__.py`.

`/app/jwt.py` contains the code for JWT authentication.

`/app/populate.py` contains functions to populate initially the databse.

`/app/tests` contains the unit tests files.

`/.env.example` contains the variables you need for your .env.

`/config.py` contains the environment variables used in this code

## Before you start

The `.env.example` contains all the environment variables you need to run this program. Simply copy all the content from it and paste in a new file called `.env` in the root of the app (same level as the app folder and the `.env.example` file).

## Docker and run the app
Create the Docker network:

    $ docker network create -d bridge tinder-for-food-bridge-network

Build the swarm:

    $ docker swarm init

Then, create the Docker image for the flask app:

    $ docker build -t tinder-for-food:latest .

Add the container to Docker from docker-compose.yml:

    $ docker stack deploy -c docker-compose.yml tinder-for-food

To see the app, visit http://localhost:5001
To see the database, visit http://localhost:8080. Credentials:
- Username: tinder_for_food_user
- Password: tinder_for_food_password
- Database: tinder_for_food
- System: PostgreSQL

When you are done, remove the containers from Docker:

    $ docker stack rm tinder-for-food

## To run the unit tests, create the virtual environment and activate it:

Create the virtualenv:

    $ virtualenv -p python3 venv

Sometimes, the above doesn't work. You can try then:

    $ python3 -m venv venv

Then, activate the activate the virtualenv. For Mac

    $ source venv/bin/activate

For **Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ venv\Scripts\activate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt

Run the unit tests:

	$ python3 -m unittest discover app/tests

When you are done. Close the virtual env.

    $ deactivate