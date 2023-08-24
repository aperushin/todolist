# The TODO List (working title)
This project is a backend API for a todo list app.

## Technologies
Project is created with:
* Python version: 3.10
* Django version: 4.2.4
* Postgres version: 15
* Docker Compose version: v2.19.1

## Setup
First, clone the repository:

```sh
$ git clone https://github.com/aperushin/todolist
$ cd todolist
```

Create and activate virtual environment:
```sh
$ python -m venv venv
$ source venv/bin/activate
```

Install Poetry and project requirements:
```sh
(venv)$ pip install poetry
(venv)$ poetry install
```

Finally, create `.env` file in the project root directory according to the example in `.env.dist`

### How to run

Locally with Docker Compose:
```sh
(venv)$ docker-compose up -d
```
