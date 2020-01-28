CREATE TABLE "users"(
  user_id serial PRIMARY KEY, 
  username VARCHAR (50) UNIQUE NOT NULL, 
  "password" VARCHAR (255) NOT NULL, 
  full_name VARCHAR (355) NOT NULL, 
  email VARCHAR (355) UNIQUE NOT NULL, 
  image VARCHAR (355) NOT NULL, 
  created_on TIMESTAMP NOT NULL, 
  ckan_api_key VARCHAR (255) NOT NULL, 
  last_login TIMESTAMP
);

CREATE TABLE keywords(
  keyword_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL
);

CREATE TABLE revoked_tokens(
  id serial PRIMARY KEY, 
  jti VARCHAR (355) NOT NULL
);

CREATE TABLE categories(
  categorie_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL
);

CREATE TABLE hosts(
  host_id serial PRIMARY KEY, 
  name VARCHAR (50) NOT NULL,
  address VARCHAR (15) UNIQUE NOT NULL, 
  created_on TIMESTAMP NOT NULL
);

CREATE TABLE services(
  service_id serial PRIMARY KEY, 
  name VARCHAR (50) NOT NULL,
  machine INT NOT NULL,
  host_id INT NOT NULL,
  created_on TIMESTAMP NOT NULL,
  FOREIGN KEY (host_id) REFERENCES hosts (host_id)
);

CREATE TABLE ports(
 port_id serial PRIMARY KEY, 
 port VARCHAR (10) NOT NULL
);

CREATE TABLE research_data_repositories (
  repo_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL, 
  abstract VARCHAR (500) NOT NULL, 
  maintainer VARCHAR (355) NULL, 
  created_on TIMESTAMP NOT NULL
);

CREATE TABLE research_group(
  group_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL, 
  abstract VARCHAR (500) NOT NULL, 
  created_on TIMESTAMP NOT NULL, 
  maintainer VARCHAR (355) NULL, 
  image VARCHAR (355) NOT NULL, 
  language VARCHAR (50) NOT NULL, 
  custom_fields json NULL
);

CREATE TABLE research_data_repositories_services(
  repo_id INT NOT NULL, 
  service_id INT NOT NULL, 
  FOREIGN KEY (repo_id) REFERENCES research_data_repositories (repo_id), 
  FOREIGN KEY (service_id) REFERENCES services (service_id)
);

CREATE TABLE services_ports(
 port_id INT NOT NULL, 
 service_id INT NOT NULL, 
 FOREIGN KEY (port_id) REFERENCES ports (port_id), 
 FOREIGN KEY (service_id) REFERENCES services (service_id)
);

CREATE TABLE research_data_repositories_group(
  repo_id INT NOT NULL, 
  group_id INT NOT NULL, 
  FOREIGN KEY (repo_id) REFERENCES research_data_repositories (repo_id), 
  FOREIGN KEY (group_id) REFERENCES research_group (group_id)
);

CREATE TABLE research_group_users(
  group_id INT NOT NULL, 
  user_id INT NOT NULL, 
  FOREIGN KEY (group_id) REFERENCES research_group (group_id), 
  FOREIGN KEY (user_id) REFERENCES "users" (user_id)
);

CREATE TABLE research_data_repositories_keywords(
  repo_id INT NOT NULL, 
  keyword_id INT NOT NULL, 
  FOREIGN KEY (repo_id) REFERENCES research_data_repositories (repo_id), 
  FOREIGN KEY (keyword_id) REFERENCES keywords (keyword_id)
);

CREATE TABLE research_data_repositories_categories(
  repo_id INT NOT NULL, 
  categorie_id INT NOT NULL, 
  FOREIGN KEY (repo_id) REFERENCES research_data_repositories (repo_id), 
  FOREIGN KEY (categorie_id) REFERENCES categories (categorie_id)
);

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('LiSS', 'O Laboratório de Investigação Sistemas Socioambientais (LiSS) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. Ele tem como objeto estudar a influencia das atividade antrópicas nas mudanças de uso e cobertura da Terra. A principal área de estudo do LiSS é a Amazônia Legal, porém pesquisas também vem sendo feitas na região do Vale Paraibano (SP) e no bioma do Pantanal.', 'username', '2019-09-04T14:48:54+00:00', 'Português','assets/images/liss.png');

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('LabISA', 'O Laboratório de Instrumentação de Sistemas Aquáticos (LabISA) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. O laboratório foi motivado pelo aumento no número de estudos voltados à aplicações de sensoriamento remoto para estimativa de propriedades físicas, biológicas e químicas de águas continentais. A principal atividade do laboratório é coleta de dados sobre propriedades óticas e limnológicas de águas interiores e costeiras.', 'username', '2019-09-04T14:48:54+00:00', 'Português', 'assets/images/labisa.png');

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('LAF', 'O Laboratório de Investigação Sistemas Socioambientais (LiSS) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. Ele tem como objeto estudar a influencia das atividade antrópicas nas mudanças de uso e cobertura da Terra. A principal área de estudo do LiSS é a Amazônia Legal, porém pesquisas também vem sendo feitas na região do Vale Paraibano (SP) e no bioma do Pantanal.', 'username', '2019-09-04T14:48:54+00:00', 'Português', 'assets/images/laf.png');

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('TREES', 'O Laboratório de Instrumentação de Sistemas Aquáticos (LabISA) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. O laboratório foi motivado pelo aumento no número de estudos voltados à aplicações de sensoriamento remoto para estimativa de propriedades físicas, biológicas e químicas de águas continentais. A principal atividade do laboratório é coleta de dados sobre propriedades óticas e limnológicas de águas interiores e costeiras.', 'username', '2019-09-04T14:48:54+00:00', 'Português', 'assets/images/trees.png');

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('LOA', 'O Laboratório de Instrumentação de Sistemas Aquáticos (LabISA) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. O laboratório foi motivado pelo aumento no número de estudos voltados à aplicações de sensoriamento remoto para estimativa de propriedades físicas, biológicas e químicas de águas continentais. A principal atividade do laboratório é coleta de dados sobre propriedades óticas e limnológicas de águas interiores e costeiras.', 'username', '2019-09-04T14:48:54+00:00', 'Português', 'assets/images/loa.png');

INSERT INTO research_data_repositories ("name", abstract, maintainer, created_on) VALUES ('LiSS Repository', 'O Laboratório de Investigação Sistemas Socioambientais (LiSS) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. Ele tem como objeto estudar a influencia das atividade antrópicas nas mudanças de uso e cobertura da Terra. A principal área de estudo do LiSS é a Amazônia Legal, porém pesquisas também vem sendo feitas na região do Vale Paraibano (SP) e no bioma do Pantanal.', 'username', '2019-09-04T14:48:54+00:00');

INSERT INTO research_data_repositories ("name", abstract, maintainer, created_on) VALUES ('LabISA Repository', 'O Laboratório de Instrumentação de Sistemas Aquáticos (LabISA) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. O laboratório foi motivado pelo aumento no número de estudos voltados à aplicações de sensoriamento remoto para estimativa de propriedades físicas, biológicas e químicas de águas continentais. A principal atividade do laboratório é coleta de dados sobre propriedades óticas e limnológicas de águas interiores e costeiras.', 'username', '2019-09-04T14:48:54+00:00');

INSERT INTO ports (port) VALUES ('5432');
INSERT INTO ports (port) VALUES ('5555');
INSERT INTO ports (port) VALUES ('5050');
INSERT INTO ports (port) VALUES ('5000');

INSERT INTO hosts ("name", address, created_on) VALUES ('Servidor_1','172.17.0','2019-09-04T14:48:54+00:00');
INSERT INTO hosts ("name", address, created_on) VALUES ('Servidor_2','172.18.0','2019-09-04T14:48:54+00:00');

INSERT INTO keywords ("name") VALUES ('Sistemas Socioambientais');
INSERT INTO keywords ("name") VALUES ('Atividade Antrópicas');
INSERT INTO keywords ("name") VALUES ('Uso e Cobertura da Terra');
INSERT INTO keywords ("name") VALUES ('Sensoriamento Remoto');
INSERT INTO keywords ("name") VALUES ('Sistemas Aquáticos');
INSERT INTO keywords ("name") VALUES ('Águas Continentais');

INSERT INTO categories ("name") VALUES ('Sensoriamento Remoto');
INSERT INTO categories ("name") VALUES ('Uso e Cobertura da Terra');

INSERT INTO users (username, full_name, "password", email, image, created_on, last_login, ckan_api_key) VALUES ('username_1', 'username_full_name', 'userpass', 'email@email.com','assets/images/img_avatar.png','2019-09-04T14:48:54+00:00','2019-09-04T14:48:54+00:00','');
INSERT INTO users (username, full_name, "password", email, image, created_on, last_login, ckan_api_key) VALUES ('username_2', 'username2_full_name', 'userpass', 'email2@email2.com','assets/images/img_avatar2.png','2019-09-04T14:48:54+00:00','2019-09-04T14:48:54+00:00','');

INSERT INTO services ("name", host_id, machine, created_on) VALUES ('PostgreSQL', 1, 01, '2019-09-04T14:48:54+00:00');
INSERT INTO services ("name", host_id, machine, created_on) VALUES ('GeoServer', 1, 02, '2019-09-04T14:48:54+00:00');
INSERT INTO services ("name", host_id, machine, created_on) VALUES ('GeoNetwork', 1, 03, '2019-09-04T14:48:54+00:00');
INSERT INTO services ("name", host_id, machine, created_on) VALUES ('PostgreSQL', 2, 01, '2019-09-04T14:48:54+00:00');
INSERT INTO services ("name", host_id, machine, created_on) VALUES ('GeoServer', 2, 02, '2019-09-04T14:48:54+00:00');
INSERT INTO services ("name", host_id, machine, created_on) VALUES ('GeoNetwork', 2, 03, '2019-09-04T14:48:54+00:00');

INSERT INTO research_data_repositories_services (repo_id, service_id) VALUES (1,1);
INSERT INTO research_data_repositories_services (repo_id, service_id) VALUES (1,2);
INSERT INTO research_data_repositories_services (repo_id, service_id) VALUES (1,3);
INSERT INTO research_data_repositories_services (repo_id, service_id) VALUES (2,4);
INSERT INTO research_data_repositories_services (repo_id, service_id) VALUES (2,5);
INSERT INTO research_data_repositories_services (repo_id, service_id) VALUES (2,6);

INSERT INTO services_ports (service_id, port_id) VALUES (1,1);
INSERT INTO services_ports (service_id, port_id) VALUES (2,2);
INSERT INTO services_ports (service_id, port_id) VALUES (2,3);
INSERT INTO services_ports (service_id, port_id) VALUES (3,4);
INSERT INTO services_ports (service_id, port_id) VALUES (4,1);
INSERT INTO services_ports (service_id, port_id) VALUES (5,2);
INSERT INTO services_ports (service_id, port_id) VALUES (5,3);
INSERT INTO services_ports (service_id, port_id) VALUES (6,4);

INSERT INTO research_data_repositories_group (repo_id, group_id) VALUES (1,1);
INSERT INTO research_data_repositories_group (repo_id, group_id) VALUES (2,2);

INSERT INTO research_group_users (group_id, user_id) VALUES (1,1);
INSERT INTO research_group_users (group_id, user_id) VALUES (1,2);
INSERT INTO research_group_users (group_id, user_id) VALUES (2,1);
INSERT INTO research_group_users (group_id, user_id) VALUES (2,2);
INSERT INTO research_group_users (group_id, user_id) VALUES (3,1);
INSERT INTO research_group_users (group_id, user_id) VALUES (3,2);
INSERT INTO research_group_users (group_id, user_id) VALUES (4,1);
INSERT INTO research_group_users (group_id, user_id) VALUES (4,2);
INSERT INTO research_group_users (group_id, user_id) VALUES (5,1);
INSERT INTO research_group_users (group_id, user_id) VALUES (5,2);

INSERT INTO research_data_repositories_keywords (repo_id, keyword_id) VALUES (1,1);
INSERT INTO research_data_repositories_keywords (repo_id, keyword_id) VALUES (1,2);
INSERT INTO research_data_repositories_keywords (repo_id, keyword_id) VALUES (1,3);
INSERT INTO research_data_repositories_keywords (repo_id, keyword_id) VALUES (2,4);
INSERT INTO research_data_repositories_keywords (repo_id, keyword_id) VALUES (2,5);
INSERT INTO research_data_repositories_keywords (repo_id, keyword_id) VALUES (2,6);

INSERT INTO research_data_repositories_categories (repo_id, categorie_id) VALUES (1,1);
INSERT INTO research_data_repositories_categories (repo_id, categorie_id) VALUES (2,2);


