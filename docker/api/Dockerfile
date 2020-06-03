FROM python:3.7-alpine3.9
MAINTAINER TerraBrasilis Research Data

# Ports
EXPOSE 8090

# env variables
ENV POSTGRES_USER postgres
ENV POSTGRES_PW postgres
ENV POSTGRES_DB terrabrasilisrd
ENV TBRD_REPO_DB_USER geonetwork
ENV TBRD_REPO_DB_PASS geonetwork
ENV KUBERNETES_API_PORT 8070
ENV KUBERNETES_API_HOST http://localhost

# Install app
COPY . /data_manager
WORKDIR /data_manager

# app requirements
RUN apk add build-base && \
    apk add postgresql-dev gcc python3-dev musl-dev && \
    pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "data_manager/app.py" ]
