# WebMark

[![codecov](https://codecov.io/gh/quantum-ohtu/WebMark/branch/main/graph/badge.svg?token=v5v9pp0sfJ)](https://codecov.io/gh/quantum-ohtu/WebMark)

Web platform for benchmarking quantum computing algorithms.

## Documentation

[Architecture](/docs/architecture.md)

## Requirements

See [requirements.txt](requirements.txt)

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

## Setting up the development environment manually (not recommended)

### Set up the database
Install PostgreSQL:

```
sudo apt install postgresql postgresql-contrib libpq-dev python3-dev
```

Create a database:
```
sudo -u postgres psql
postgres=# create database quantdb;
postgres=# create user quantuser with encrypted password 'secret';
postgres=# grant all privileges on database quantdb to quantuser;
postgres=# alter user quantuser createdb; --allow user to create a test database
postgres=# \q
```

### Setting up WebMark
Make a copy of [.env.example](.env.example) and rename it to `.env`.

Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Now you can run the development server with command:
```
python manage.py runserver
```

If you get an error message when running the server, for example "psycopg2.errors.UndefinedTable: relation "WebCLI_algorithm" does not exist" you can try making migrations
```
python manage.py makemigrations WebCLI
python manage.py migrate
```
And then run the development server again.

## Other commands

---
**NOTE**: all the next commands can be used from Docker with
```
sudo docker-compose run web <command_name_with_possible_parameters>
```
For example:
```
sudo docker-compose run web python manage.py makemigration
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

test commit
