# Architecture

## Glossary

There are a lot of potentially unfamiliar terminology used in this document so it might be helpful to briefly explain some of them.

**Django**: [Django](https://www.djangoproject.com/) is a Python web application framework that uses traditional [server-side scripting](https://en.wikipedia.org/wiki/Server-side_scripting). The framework follows [Model-view-controller (MVC)](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) design pattern.

**Docker**: [Docker](https://www.docker.com/) is a tool for bundling applications into *images* that contains all the libraries and resources that the application needs including a preferred Linux distribution. [Dockerfile](https://docs.docker.com/engine/reference/builder/) contains the instructions on how to create an image. These images can be used to created instances called [containers](https://www.docker.com/resources/what-container) that can be started, stopped and removed.

**Docker Compose**: [Docker Compose](https://docs.docker.com/compose/) is a tool for making the management of multiple Docker containers easier. The configuration is stored in a [docker-compose.yml](../docker-compose.yml) file.

**PostgreSQL**: [PostgreSQL](https://www.postgresql.org/) is a relational database management system.

## Environment
The full environment is set up using Docker Compose and consists of two Docker containers:
* **Web** contains Django web server (nicknamed WebMark)
* **DB** contains PostgreSQL database

## Web server

The web server has been nicknamed WebMark. Folder `/WebMark` contains project settings and `/WebCLI` contains the actual application.
Architecturally the web server consists of three parts: templates, views and models.

  * **Templates** contain HTML documents with occasional inline Javascript. [Django templating language](https://docs.djangoproject.com/en/3.1/ref/templates/language/) is used to generate some of the HTML using the data provided by view layer.
  * **Views** contain the logic used to populate the templates with correct data that are fetched using models.
  * **Models** represent the database schema and are used to execute database operations.

## Database

The database uses PostgreSQL and the schema is shown in the following diagram. User table has been automatically created by Django and most of the fields are not used. The relevant fields are username and password.

![Database schema](images/db_schema.png)

