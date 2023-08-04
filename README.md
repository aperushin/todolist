# The TODO List (working title)
This project is a task manager

## Technologies
Project is created with:
* Python version: 3.10
* Django version: 4.2.4
* Postgres version: 15
* Docker Compose version: v2.19.1

## Setup
* Install requirements: `pip install -r requirements.txt`


* Create `.env` file in the project root directory according to the example in `.env.dist`


* Run `docker-compose -f .\todolist-postgres\docker-compose.yaml up -d` to create a docker container with a database


* Apply migrations: `python .\todolist\manage.py migrate`


* Run server: `python .\todolist\manage.py runserver`
