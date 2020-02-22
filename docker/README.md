# Dockerfiles for Data Manager API

This directory contains Dockerfiles to facilitate the use of the data manager api

## Dockerfiles available

The following Dockerfiles are available in this directory:

- `api`: Dockerfile to load and configure the necessary environment for using the data manager api
- `postgres`: Customized dockerfile for postgres configuration and API database initialization

## Usage

To use these Dockerfiles together it is possible to use the docker-compose, for this, use the following command

```shell
$ docker-compose up -d --build
```

> If necessary, the .env file helps in editing the api's connection options with the database
