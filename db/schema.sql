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

CREATE TABLE services_hosts(
 host_id INT NOT NULL, 
 service_id INT NOT NULL, 
 FOREIGN KEY (host_id) REFERENCES hosts (host_id), 
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

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('LabISA', 'O Laboratório de Instrumentação de Sistemas Aquáticos (LabISA) foi criado no final de 2013 por um grupo de pesquisadores das divisões de Sensoriamento Remoto (DSR) e de Processamento de Imagens (DPI) da Coordenação de Observação da Terra (OBT) do Instituto Nacional de Pesquisas Espaciais (INPE). Ele foi motivado pelo aumento no número de estudos voltados à aplicações de sensoriamento remoto para estimativa de propriedades físicas, biológicas e químicas de águas continentais, por ganhos tecnológicos recentes e pela demanda crescente do uso racional da água doce.', 'username', '2019-09-04T14:48:54+00:00', 'Português', 'assets/images/labisa.png');

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('LAF', 'O LAF é um grupo de pesquisa formado por pessoas com conhecimento das áreas de sensoriamento remoto, computacão, geografia, estatística, agricultura, floresta e biologia, entre outras. O laboratório se envolve basicamente em atividades relacionadas com mapeamento e monitoramento ambiental. Desta forma, o Laboratório gera tanto dados matriciais, vetorias, tabulares e programas para manipular os dados.', 'username', '2019-09-04T14:48:54+00:00', 'Português', 'assets/images/laf.png');

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('TREES', 'TREES laboratory is a research group led by Dr Luiz Aragão. The group was created in 2009 when Dr Aragão moved from the Environmental Change Institute, University of Oxford to the School of Life and Environmental Sciences, University of Exeter in UK. Dr Aragão is now based at the National Institute for Space Research in Brazil, the current headquarters of TREES.', 'username', '2019-09-04T14:48:54+00:00', 'Português', 'assets/images/trees.png');

INSERT INTO research_group ("name", abstract, maintainer, created_on, "language", image) VALUES ('LOA', 'Laboratório de Estudos do Oceano e da Atmosfera (LOA) tem suas principais linhas de pesquisa voltadas ao estudo da física do oceano, física da atmosfera e da interação entre estes dois meios. O LOA integra várias projetos multi-institucionais de pesquisa. Realiza  e apoia campanhas de coletas de dados em cruzeiros oceanográficos no Atlântico Tropical, Atlântico Sul e Antártica (Oceano Austral). Associado a estas observações in situ, muitos estudos sobre as trocas de momentum, calor e CO2 na interface oceano-atmosfera são desenvolvidos.', 'username', '2019-09-04T14:48:54+00:00', 'Português', 'assets/images/loa.png');

INSERT INTO ports (port) VALUES ('30040');
INSERT INTO ports (port) VALUES ('30045');

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


