# TerraBrasilis Research Data - Data Management
The Data Manager component is responsible for the management of Research Data Repositories and for providing mechanisms for searching and accessing all data available in the repositories.

CKAN Installation
------------
```sh
cd terrabrasilis-research-data-ckan/contrib/docker

sudo docker-compose up -d --build

sudo docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan sysadmin -c /etc/ckan/production.ini add ckanadmin
```

TBRD Installation
------------
```sh
cd terrabrasilis-research-data-api

virtualenv flask

flask/bin/pip install flask

flask/bin/pip install flask-httpauth

chmod a+x app.py

./app.py
```
