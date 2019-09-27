# TerraBrasilis Research Data - Data Management
The Data Manager component is responsible for the management of Research Data Repositories and for providing mechanisms for searching and accessing all data available in the repositories.


Documentation
------------
#### create_user()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"username": "gabriel", "full_name": "Gabriel Sansigolo", "password":"gabriel", "email":"gabrielsansigolo@gmail.com", "image":"assets/images/img_avatar2.png", "created_on":"2019-09-04T14:48:54+00:00", "last_login":"2019-09-04T14:48:54+00:00"}' http://localhost:5000/api/v1.0/users
```

#### read_users()
```sh
curl -i http://localhost:5000/api/v1.0/users
```

#### read_user(user_id)
```sh
curl -i http://localhost:5000/api/v1.0/users/1
```

#### update_user(user_id)
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X PUT -d '{"username": "gabriel", "full_name": "Gabriel Sansigolo", "password":"gabriel", "email":"gabrielsansigolo@gmail.com", "image":"assets/images/img_avatar2.png", "created_on":"2019-09-04T14:48:54+00:00", "last_login":"2019-09-04T14:48:54+00:00"}' http://localhost:5000/api/v1.0/users/1
```

#### delete_user(user_id)
```sh
curl -u gabriel:gabriel -X DELETE http://localhost:5000/api/v1.0/users/3
```

#### create_services() 
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "PostgreSQL", "machine": 1, "host_id": 3, "created_on": "2019-09-04T14:48:54+00:00"}' http://localhost:5000/api/v1.0/services
```

#### read_services() 
```sh
curl -i http://localhost:5000/api/v1.0/services
```

#### read_service(service_id)
```sh
curl -i http://localhost:5000/api/v1.0/services/1
```

#### delete_service(service_id)
```sh
curl -u gabriel:gabriel -X DELETE http://localhost:5000/api/v1.0/services/7
```

#### create_categorie()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "Observação da Terra"}' http://localhost:5000/api/v1.0/categories
```

#### read_categories() 
```sh
curl -i http://localhost:5000/api/v1.0/categories

```

#### create_keywords()
```sh
curl -i curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "Processamento de Imagens"}' http://localhost:5000/api/v1.0/keywords
```

#### read_keywords()
```sh
curl -i http://localhost:5000/api/v1.0/keywords

```

#### create_hosts()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "Servidor_3","address": "172.19.0","created_on":"2019-09-04T14:48:54+00:00" }' http://localhost:5000/api/v1.0/hosts
```

#### read_hosts()
```sh
curl -i http://localhost:5000/api/v1.0/hosts

```

#### read_ports(repo_id)
```sh
curl -i http://localhost:5000/api/v1.0/ports/1

```
#### create_repositorie()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"name": "Teste","abstract": "Teste","maintainer": "username","created_on": "2019-09-04T14:48:54+00:00","language": "Português","email": "email@email.com","bbox": "POLYGON((-70.0588433406 -33.3848757513,-35.2541558406 -33.3848757513, -35.2541558406 0.2315631899,-70.0588433406 0.2315631899,-70.0588433406 -33.3848757513))","custom_fields": []}' http://localhost:5000/api/v1.0/repositories
```

#### read_repositories()
```sh
curl -i http://localhost:5000/api/v1.0/repositories
```

#### read_repositorie(repo_id)
```sh
curl -i http://localhost:5000/api/v1.0/repositories/1

```

#### update_repositorie(repo_id)
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X PUT -d '{"name": "Teste","abstract": "Teste","maintainer": "username","created_on": "2019-09-04T14:48:54+00:00","language": "Português","email": "email@email.com","bbox": "POLYGON((-70.0588433406 -33.3848757513,-35.2541558406 -33.3848757513, -35.2541558406 0.2315631899,-70.0588433406 0.2315631899,-70.0588433406 -33.3848757513))","custom_fields": []}' http://localhost:5000/api/v1.0/repositories/3
```

#### delete_repositorie(repo_id)
```sh
curl -u gabriel:gabriel -X DELETE http://localhost:5000/api/v1.0/repositories/3
```

#### create_service_repositorie_rel()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"repo_id": 1, "service_id": 4}' http://localhost:5000/api/v1.0/service_repositorie_rel
```

 #### delete_service_repositorie_rel(service_id,repo_id)
```sh
curl -u gabriel:gabriel -X DELETE http://localhost:5000/api/v1.0/service_repositorie_rel/1/3
```

#### create_user_repositorie_rel()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"repo_id": 1, "user_id": 3}' http://localhost:5000/api/v1.0/user_repositorie_rel
```

 #### delete_user_repositorie_rel(service_id,repo_id)
```sh
curl -u gabriel:gabriel -X DELETE http://localhost:5000/api/v1.0/user_repositorie_rel/4/1
```

#### create_categorie_repositorie_rel()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"repo_id": 1, "categorie_id": 3}' http://localhost:5000/api/v1.0/categorie_repositorie_rel

```

#### delete_categorie_repositorie_rel(categorie_id,repo_id)
```sh
curl -u gabriel:gabriel -X DELETE http://localhost:5000/api/v1.0/categorie_repositorie_rel/1/3
```

#### create_keyword_repositorie_rel()
```sh
curl -u gabriel:gabriel -i -H "Content-Type: application/json" -X POST -d '{"repo_id": 1, "keyword_id": 7}' http://localhost:5000/api/v1.0/keyword_repositorie_rel
```

#### delete_keyword_repositorie_rel(categorie_id,repo_id)
```sh
curl -u gabriel:gabriel -X DELETE http://localhost:5000/api/v1.0/keyword_repositorie_rel/7/1
```
