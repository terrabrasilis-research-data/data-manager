# TerraBrasilis Research Data - Data Manager
The Data Manager component is responsible for the management of Research Data Repositories and for providing mechanisms for searching and accessing all data available in the repositories. It uses a flask aplication with a relational database to CRUD metadata.

## API run

To run the API on your machine, use the start.sh script.

```sh
./start.sh
```

## API run (Docker)

To run the API on a container use the Dockerfile provided in the repository.

```
docker build -t "inpe/terrabrasilisapi" .
```

After that, run the container.

```
docker run -d --name terrabrasilis_data_manager_api --restart unless-stopped \
        -p 5000:5000 inpe/terrabrasilisapi
```

If required, the following environment variables are available.

* `POSTGRES_URL` Database Address, with port (e.g. 127.0.0.1:5432)
* `POSTGRES_USER`  Database user (e.g. postgres)
* `POSTGRES_PW` Database password (e.g. postgres)
* `POSTGRES_DB` Database name (e.g. terrabrasilisrd)
