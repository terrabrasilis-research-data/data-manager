# TerraBrasilis Research Data - Data Management
The Data Manager component is responsible for the management of Research Data Repositories and for providing mechanisms for searching and accessing all data available in the repositories.


Installation
------------

1. git clone https://github.com/terrabrasilis-research-data/data-management
2. `cd data-management`
3. `cd terrabrasilis-research-data-ckan/contrib/docker`
4. run the following command: `sudo docker-compose up -d --build` # it will run all the needed containers
5. run the following command: `sudo docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan sysadmin -c /etc/ckan/production.ini add ckanadmin`
6. `cd ..`
7. `cd terrabrasilis-research-data-api`
8. run the following command: `virtualenv flask` 
9. run the following command: `flask/bin/pip install flask` 
10.  run the following command: `flask/bin/pip install flask-httpauth` 
11.  run the following command: `chmod a+x app.py`
12.  run the following command: `./app.py`
