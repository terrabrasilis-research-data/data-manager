# TerraBrasilis Research Data - Data Management
The Data Manager component is responsible for the management of Research Data Repositories and for providing mechanisms for searching and accessing all data available in the repositories.


Documentation
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

#### get_categories() 
```sh
curl -i http://localhost:5000/api/v1.0/categories

```

#### create_categories()
```sh
curl -i curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "Observação da Terra"}' http://localhost:5000/api/v1.0/categories
```

#### get_keywords()
```sh
curl -i http://localhost:5000/api/v1.0/keywords

```

#### create_keywords()
```sh
curl -i curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "Processamento de Imagens"}' http://localhost:5000/api/v1.0/keywords
```

#### get_hosts()
```sh
curl -i http://localhost:5000/api/v1.0/hosts

```

#### get_ports(repo_id)
```sh
curl -i http://localhost:5000/api/v1.0/ports/1

```

#### get_repositories()
```sh
curl -i http://localhost:5000/api/v1.0/repositories
```

#### get_repositorie(repo_id)
```sh
curl -i http://localhost:5000/api/v1.0/repositories/1

```
#### create_repositorie()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "AAA","abstract": "AAA","maintainer": "username","created_on": "2019-09-04T14:48:54+00:00","language": "Português","email": "email@email.com","bbox": "POLYGON((-70.0588433406 -33.3848757513,-35.2541558406 -33.3848757513, -35.2541558406 0.2315631899,-70.0588433406 0.2315631899,-70.0588433406 -33.3848757513))","custom_fields": [], "start_date": "2019-09-04T14:48:54+00:00", "end_date": "2019-09-04T14:48:54+00:00"}' http://localhost:5000/api/v1.0/repositories
```
