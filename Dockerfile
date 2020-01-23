FROM python:3.7-alpine3.9
LABEL maintainer="TerraBrasilis Research Data"

# Ports
EXPOSE 8090

# env variables
ENV POSTGRES_URL 127.0.0.1:5432
ENV POSTGRES_USER postgres
ENV POSTGRES_PW postgres
ENV POSTGRES_DB terrabrasilisrd

# Install app
COPY . /data_manager_api
WORKDIR /data_manager_api

# app requirements
RUN apk add build-base && \
    apk add postgresql-dev gcc python3-dev musl-dev && \
    pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "data_manager/app.py" ]
