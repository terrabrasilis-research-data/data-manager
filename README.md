# TerraBrasilis Research Data - Data Manager Repositories
The Data Manager component is responsible for the management of Research Data Repositories and for providing mechanisms for searching and accessing all data available in the repositories. It uses a flask aplication with a relational database to CRUD metadata.

API Installation
------------
```sh
cd src

virtualenv flask

flask/bin/pip install -r requirements.txt

chmod a+x app.py

source .env

./app.py
```
