CREATE DATABASE terrabrasilisrd;

\c terrabrasilisrd

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
  address VARCHAR (60) UNIQUE NOT NULL, 
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
  path VARCHAR (50) UNIQUE NOT NULL, 
  abstract VARCHAR (500) NOT NULL, 
  maintainer VARCHAR (355) NULL, 
  created_on TIMESTAMP NOT NULL
);

CREATE TABLE research_group(
  group_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL, 
  abstract VARCHAR (1000) NOT NULL, 
  created_on TIMESTAMP NOT NULL, 
  maintainer VARCHAR (355) NULL, 
  ckan_group_id VARCHAR(355) NOT NULL,
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

CREATE TABLE research_data_repositories_categories(
  repo_id INT NOT NULL, 
  categorie_id INT NOT NULL, 
  FOREIGN KEY (repo_id) REFERENCES research_data_repositories (repo_id), 
  FOREIGN KEY (categorie_id) REFERENCES categories (categorie_id)
);

INSERT INTO ports (port) VALUES ('30040');
INSERT INTO ports (port) VALUES ('30045');

INSERT INTO categories ("name") VALUES ('Sensoriamento Remoto');
INSERT INTO categories ("name") VALUES ('Uso e Cobertura da Terra');

INSERT INTO hosts (name, address, created_on ) VALUES ('Host_1', '192.168.122.1', '2019-09-04T14:48:54+00:00');
