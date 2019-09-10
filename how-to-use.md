# TerraBrasilis Research Data - Data Management
The Data Manager component is responsible for the management of Research Data Repositories and for providing mechanisms for searching and accessing all data available in the repositories.


How to use
------------
#### get_users()
```sh
curl -i http://localhost:5000/api/v1.0/users
```

#### get_user(user_id)
```sh
curl -i http://localhost:5000/api/v1.0/users/1
```

#### create_user()
```sh
curl -i curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"username": "gabriel", "full_name": "Gabriel Sansigolo", "password":"gabriel", "email":"gabrielsansigolo@gmail.com", "image":"assets/images/img_avatar2.png", "created_on":"2019-09-04T14:48:54+00:00", "last_login":"2019-09-04T14:48:54+00:00"}' http://localhost:5000/api/v1.0/users
```

#### get_services()
```sh
curl -i http://localhost:5000/api/v1.0/services
```

#### get_service(service_id)
```sh
curl -i http://localhost:5000/api/v1.0/services/1
```

<!---
#### get_repositories()
```sh
curl -i http://localhost:5000/api/v1.0/repositories
```

#### get_repositorie(repositorie_id)
```sh
curl -i http://localhost:5000/api/v1.0/repositories/1
```

#### create_repositorie()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "AAA","abstract": "AAA","maintainer": "username","created_on": "2019-09-04T14:48:54+00:00","language": "Português","email": "email@email.com","bbox": [[[-70.0588433406, -33.3848757513],[-35.2541558406, -33.3848757513],[-35.2541558406, 0.2315631899],[-70.0588433406, 0.2315631899],[-70.0588433406, -33.3848757513]]],"keywords": ["Sistemas Socioambientais", "Atividade Antrópicas", "Uso e Cobertura da Terra"],"categories": ["Uso e Cobertura da Terra"],"users": [{"user_id": 1,"name": "username_1","image": "assets/images/img_avatar2.png"}, {"user_id": 2,"name": "username_2","image": "assets/images/img_avatar.png"}],"services": [{"service_id": 1,"name": "PostgreSQL","host": "137.012.125.01","ports": [5432],"created_on": "2019-09-04T14:48:54+00:00"},{"service_id": 2,"name": "GeoServer","host": "137.012.125.02","ports": [5555, 5050],"created_on": "2019-09-04T14:48:54+00:00"},{"service_id": 3,"name": "GeoNetwork","host": "137.012.125.03","ports": [5000],"created_on": "2019-09-04T14:48:54+00:00"}],"custom_fields": [{}]}' http://localhost:5000/api/v1.0/repositories
```

#### update_repositorie(repositorie_id)
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X PUT -d '{"name": "BBB","abstract": "BBB","maintainer": "username","created_on": "2019-09-04T14:48:54+00:00","language": "Português","email": "email@email.com","bbox": [[[-70.0588433406, -33.3848757513],[-35.2541558406, -33.3848757513],[-35.2541558406, 0.2315631899],[-70.0588433406, 0.2315631899],[-70.0588433406, -33.3848757513]]],"keywords": ["Sistemas Socioambientais", "Atividade Antrópicas", "Uso e Cobertura da Terra"],"categories": ["Uso e Cobertura da Terra"],"users": [{"user_id": 1,"name": "username_1","image": "assets/images/img_avatar2.png"}, {"user_id": 2,"name": "username_2","image": "assets/images/img_avatar.png"}],"services": [{"service_id": 1,"name": "PostgreSQL","host": "137.012.125.01","ports": [5432],"created_on": "2019-09-04T14:48:54+00:00"},{"service_id": 2,"name": "GeoServer","host": "137.012.125.02","ports": [5555, 5050],"created_on": "2019-09-04T14:48:54+00:00"},{"service_id": 3,"name": "GeoNetwork","host": "137.012.125.03","ports": [5000],"created_on": "2019-09-04T14:48:54+00:00"}],"custom_fields": [{}]}' http://localhost:5000/api/v1.0/repositories/3
```

#### delete_repositorie(repositorie_id)  
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X DELETE -d '{"id":3}' http://localhost:5000/api/v1.0/repositories/3
```
-->