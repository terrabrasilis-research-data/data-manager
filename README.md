# TerraBrasilis Research Data - Data Manager
The Data Manager is responsible for the support portion of the platform. In the context of infrastructure, this includes the creation, management and delivery of Research Data Repositories. It uses a flask aplication with a relational database to CRUD metadata.

## API run

To run the API on your machine, use the start.sh script.

```sh
./start.sh
```

## API run (Docker)

To run the API on a container use the Docker-compose file provided in the repository.

```sh
cd docker
```

The following Dockerfiles are available in this directory:

- `api`: Dockerfile to load and configure the necessary environment for using the data manager api
- `postgres`: Customized dockerfile for postgres configuration and API database initialization

To use these Dockerfiles together it is possible to use the docker-compose, for this, use the following command

```shell
$ docker-compose up -d --build
```

> If necessary, the .env file helps in editing the api's connection options with the database
