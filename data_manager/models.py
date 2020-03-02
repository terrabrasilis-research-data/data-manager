import json
from app import db
from geoalchemy2 import Geometry
from geoalchemy2 import functions
from flask.json import jsonify
from sqlalchemy import PrimaryKeyConstraint
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.dialects.postgresql import JSONB

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    full_name = db.Column(db.String(355), unique=False, nullable=False)
    email = db.Column(db.String(355), unique=False, nullable=False)
    image = db.Column(db.String(355), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)
    last_login = db.Column(db.DateTime, unique=False, nullable=False)
    ckan_api_key = db.Column(db.String(355), unique=False, nullable=False)

    def __init__(self, username, password, full_name, email, image, created_on, last_login, ckan_api_key):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.image = image
        self.created_on = created_on
        self.last_login = last_login
        self.ckan_api_key = ckan_api_key

    def __repr__(self):
        return '<user_id {}>'.format(self.user_id)
    
    def serialize(self):
        return {
            'user_id': self.user_id, 
            'username': self.username,
            'full_name': self.full_name,
            'email':self.email,
            'image':self.image,
            'created_on':self.created_on,
            'last_login':self.last_login
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)    
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class Service(db.Model):

    __tablename__ = 'services'

    service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    machine = db.Column(db.Integer, unique=False, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.host_id'),nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, name, machine, host_id, created_on):
        self.name = name
        self.machine = machine
        self.host_id = host_id
        self.created_on = created_on

    def __repr__(self):
        return '<id {}>'.format(self.service_id)
    
    def serialize(self):
        return {
            'service_id': self.service_id, 
            'name': self.name,
            'machine':self.machine,
            'host_id':self.host_id,
            'created_on':self.created_on,
        }

class RevokedTokenModel(db.Model):

    __tablename__ = 'revoked_tokens'
    
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def __init__(self, jti):
        self.jti = jti

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'jti': self.jti,
        }

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

class Categorie(db.Model):

    __tablename__ = 'categories'

    categorie_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'categorie_id': self.categorie_id,
            'name': self.name
        }

class Host(db.Model):

    __tablename__ = 'hosts'

    host_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    address = db.Column(db.String(60), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, name, address, created_on):
        self.name = name
        self.address = address
        self.created_on = created_on
        
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'host_id': self.host_id, 
            'name': self.name, 
            'address': self.address,
            'created_on': self.created_on
        }

class Port(db.Model):

    __tablename__ = 'ports'

    port_id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.String(10), unique=False, nullable=False)
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'port': self.port
        }

class Group(db.Model):

    __tablename__ = 'research_group'

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    abstract = db.Column(db.String(500), unique=False, nullable=False)
    maintainer = db.Column(db.String(355), unique=False, nullable=False)
    ckan_group_id = db.Column(db.String(355), unique=False, nullable=False)
    image = db.Column(db.String(355), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)
    language = db.Column(db.String(50), unique=False, nullable=False)
    
    def __init__(self, name, abstract, maintainer, created_on, language, image, ckan_group_id):
        self.name = name
        self.abstract = abstract
        self.maintainer = maintainer
        self.created_on = created_on
        self.image = image
        self.ckan_group_id = ckan_group_id
        self.language = language
   
    def serialize(self):

        return {            
            'group_id': self.group_id, 
            'name': self.name,
            'abstract':self.abstract,
            'maintainer':self.maintainer,
            'ckan_group_id':self.ckan_group_id,
            'image':self.image,
            'created_on':self.created_on,
            'language':self.language
        }

class Repositorie(db.Model):

    __tablename__ = 'research_data_repositories'

    repo_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    path = db.Column(db.String(50), unique=False, nullable=False)
    abstract = db.Column(db.String(500), unique=False, nullable=False)
    maintainer = db.Column(db.String(355), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)
    
    
    def __init__(self, name, path, abstract, maintainer, created_on):
        self.name = name
        self.path = path
        self.abstract = abstract
        self.maintainer = maintainer
        self.created_on = created_on
   
    def serialize(self):

        return {            
            'repo_id': self.repo_id, 
            'name': self.name,
            'path': self.path,
            'abstract':self.abstract,
            'maintainer':self.maintainer,
            'created_on':self.created_on
        }

class Repositorie_Service(db.Model):

    __tablename__ = 'research_data_repositories_services'
    __table_args__ = (
        PrimaryKeyConstraint('repo_id', 'service_id'),
    )

    repo_id = db.Column(db.Integer, db.ForeignKey('research_data_repositories.repo_id'),nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'),nullable=False)

    def __init__(self, repo_id, service_id):
        self.repo_id = repo_id
        self.service_id = service_id

    def serialize(self):

        return {            
            'repo_id': self.repo_id, 
            'service_id': self.service_id
        }

class Groups_User(db.Model):

    __tablename__ = 'research_group_users'
    __table_args__ = (
        PrimaryKeyConstraint('group_id', 'user_id'),
    )

    group_id = db.Column(db.Integer, db.ForeignKey('research_group.group_id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)

    def __init__(self, user_id, group_id):
        self.group_id = group_id
        self.user_id = user_id

    def serialize(self):

        return {            
            'group_id': self.group_id, 
            'user_id': self.user_id
        }

class Repositorie_Group(db.Model):

    __tablename__ = 'research_data_repositories_group'
    __table_args__ = (
        PrimaryKeyConstraint('repo_id', 'group_id'),
    )

    repo_id = db.Column(db.Integer, db.ForeignKey('research_data_repositories.repo_id'),nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('research_group.group_id'),nullable=False)

    def __init__(self, repo_id, group_id):
        self.repo_id = repo_id
        self.group_id = group_id

    def serialize(self):

        return {            
            'repo_id': self.repo_id, 
            'group_id': self.group_id
        }

class Repositorie_Categorie(db.Model):

    __tablename__ = 'research_data_repositories_categories'
    __table_args__ = (
        PrimaryKeyConstraint('repo_id', 'categorie_id'),
    )

    repo_id = db.Column(db.Integer, db.ForeignKey('research_data_repositories.repo_id'),nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.categorie_id'),nullable=False)

    def __init__(self, repo_id, categorie_id):
        self.repo_id = repo_id
        self.categorie_id = categorie_id

    def serialize(self):

        return {            
            'repo_id': self.repo_id, 
            'categorie_id': self.categorie_id
        }

class Service_Port(db.Model):

    __tablename__ = 'services_ports'
    __table_args__ = (
        PrimaryKeyConstraint('port_id', 'service_id'),
    )

    port_id = db.Column(db.Integer, db.ForeignKey('ports.port_id'),nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'),nullable=False)

    def __init__(self, port_id, service_id):
        self.port_id = port_id
        self.service_id = service_id

    def serialize(self):

        return {            
            'port_id': self.port_id, 
            'service_id': self.service_id
        }

class Service_Host(db.Model):

    __tablename__ = 'services_hosts'
    __table_args__ = (
        PrimaryKeyConstraint('host_id', 'service_id'),
    )

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.host_id'),nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'),nullable=False)

    def __init__(self, host_id, service_id):
        self.host_id = host_id
        self.service_id = service_id

    def serialize(self):

        return {            
            'host_id': self.host_id, 
            'service_id': self.service_id
        }
