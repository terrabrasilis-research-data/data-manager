FROM mdillon/postgis

RUN mkdir -p /tmp/psql_data/

COPY db/schema.sql /tmp/psql_data/

COPY db/init_docker_postgres.sh /docker-entrypoint-initdb.d/