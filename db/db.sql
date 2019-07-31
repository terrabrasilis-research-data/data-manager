CREATE TABLE "users"(
  user_id serial PRIMARY KEY, 
  username VARCHAR (50) UNIQUE NOT NULL, 
  full_name VARCHAR (355) NOT NULL, 
  "password" VARCHAR (50) NOT NULL, 
  email VARCHAR (355) UNIQUE NOT NULL, 
  image VARCHAR (355) NOT NULL, 
  created_on TIMESTAMP NOT NULL, 
  last_login TIMESTAMP
);

CREATE TABLE keywords(
  keyword_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL
);

CREATE TABLE categories(
  categorie_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL
);

CREATE TABLE hosts(
  host_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL,
  address VARCHAR (10) UNIQUE NOT NULL, 
  created_on TIMESTAMP NOT NULL
);

CREATE TABLE services(
  service_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL,
  host_id INT NOT NULL,
  created_on TIMESTAMP NOT NULL,
  FOREIGN KEY (host_id) REFERENCES hosts (host_id)
);

CREATE TABLE ports(
 port_id serial PRIMARY KEY, 
 port VARCHAR (10) NOT NULL
);

CREATE TABLE research_data_repositories(
  repo_id serial PRIMARY KEY, 
  name VARCHAR (50) UNIQUE NOT NULL, 
  abstract VARCHAR (500) NOT NULL, 
  topic_id INT NOT NULL, 
  maintainer VARCHAR (355) NULL, 
  created_on TIMESTAMP NOT NULL, 
  language VARCHAR (50) NOT NULL, 
  address  VARCHAR (20) UNIQUE NOT NULL, 
  bbox geometry NOT NULL, 
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

CREATE TABLE research_data_repositories_users(
  repo_id INT NOT NULL, 
  repo_user INT NOT NULL, 
  FOREIGN KEY (repo_id) REFERENCES research_data_repositories (repo_id), 
  FOREIGN KEY (repo_user) REFERENCES "users" (user_id)
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
