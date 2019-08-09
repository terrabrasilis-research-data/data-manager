# TerraBrasilis Research Data - Data Management
The Data Manager component is responsible for the management of Research Data Repositories and for providing mechanisms for searching and accessing all data available in the repositories.

## CKAN Installation
------------
1. cd terrabrasilis-research-data-ckan/contrib/docker
2. sudo docker-compose up -d --build
3. sudo docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan sysadmin -c /etc/ckan/production.ini add ckanadmin

## TBRD Installation
------------
1. cd terrabrasilis-research-data-api
2. virtualenv flask
3. flask/bin/pip install flask
4. flask/bin/pip install flask-httpauth
5. chmod a+x app.py
6. ./app.py