# New Django REST framework -based Webmark

[![codecov](https://codecov.io/gh/quantum-ohtu/WebMark2/branch/main/graph/badge.svg?token=CJBQEREUOW)](https://codecov.io/gh/quantum-ohtu/WebMark2)

Read [creation notes](documentation/CreationNotes.md) to see which files were modified or created to get this far from the previous version [WebMark](https://github.com/quantum-ohtu/WebMark).

Note that you need to set up your .env before running the server.

## Environment

First of all, the environment variables has to be set. Make sure you have a file [.env](https://github.com/quantum-ohtu/WebMark2/blob/main/.env) in the root of the project. The .env is also in the .gitignore. Currently, there is some values and it is highly recommended to replace those (espacially the secrets, in production those have to be secret!)

Here is the current values:
```
SECRET_KEY="secret"
DATABASE_NAME=quantdb
DATABASE_USER=quantuser
DATABASE_PASSWORD="greatsecret"
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
```

__Tip how to generate a secret key with python:__

```
python -c "import secrets; print(secrets.token_urlsafe())"
```

## Starting the server

If you have made changes to the model then you need to update the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

`Ctrl-C` to terminate.

## Testing the server

A request should initially return an empty JSON list []:

```bash
curl -L http://127.0.0.1:8000/api/
```

To POST some data:

```bash
curl -L --header "Content-Type: application/json" \
  --data '{"result":"Kukkuuu"}' \
  http://localhost:8000/api/
```

To use a browser to see the list we need an api.html template.


## Setting up the development environment using Docker (recommended)

Install Docker [Engine](https://docs.docker.com/engine/install/) and Docker [Compose](https://docs.docker.com/compose/install/) according to the instructions.

Navigate to the project root and run the development environment with command:
```
sudo docker-compose up
```
In case new dependencies have been added to any of the environments (that is requirements.txt or environment.yml have been changed), start the development environment with
```
sudo docker-compose up --build
```
If the database needs to be flushed, the easiest way to do that is with command
```
sudo docker-compose down
```

## Other commands

---
**NOTE**: all the next commands can be used from Docker with
```
sudo docker-compose run qleader-web <command_name_with_possible_parameters>
```
For example:
```
sudo docker-compose run qleader-web python manage.py makemigration
```
---
Lint your code with
```
flake8
```

Lint HTML templates with
```
curlylint templates/
```

Run tests
```
python manage.py test
```

Run code coverage
```
coverage erase
coverage run manage.py test
coverage report
```

Update database after change in models
```
python manage.py makemigrations
python manage.py migrate

```
