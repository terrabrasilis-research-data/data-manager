## Terrabrasilis Research Data API - Docker

> The commands presented in this document are used to execute the API container. If you use this approach, be aware of the need for a database configured to store API data

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
