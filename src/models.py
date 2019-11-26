import json
from app import db
from geoalchemy2 import Geometry
from geoalchemy2 import functions
from flask.json import jsonify
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    full_name = db.Column(db.String(355), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(355), unique=False, nullable=False)
    image = db.Column(db.String(355), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)
    last_login = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, username, full_name, password, email, image, created_on, last_login):
        self.username = username
        self.full_name = full_name
        self.password = password
        self.email = email
        self.image = image
        self.created_on = created_on
        self.last_login = last_login

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
            'name': self.name
        }

class Host(db.Model):

    __tablename__ = 'hosts'

    host_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    address = db.Column(db.String(15), unique=False, nullable=False)
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

class Keywords(db.Model):

    __tablename__ = 'keywords'

    keyword_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'name': self.name
        }

class Group(db.Model):

    __tablename__ = 'research_group'

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    abstract = db.Column(db.String(500), unique=False, nullable=False)
    maintainer = db.Column(db.String(355), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)
    language = db.Column(db.String(50), unique=False, nullable=False)
    bbox = db.Column(Geometry(geometry_type='POLYGON'), unique=False, nullable=False)
    custom_fields = db.Column(JSONB, unique=False, nullable=False)
    
    def __init__(self, name, abstract, maintainer, created_on, language, bbox, custom_fields):
        self.name = name
        self.abstract = abstract
        self.maintainer = maintainer
        self.created_on = created_on
        self.language = language
        self.bbox = bbox
        self.custom_fields = custom_fields
   
    def serialize(self):

        return {            
            'group_id': self.group_id, 
            'name': self.name,
            'abstract':self.abstract,
            'maintainer':self.maintainer,
            'created_on':self.created_on,
            'language':self.language,
            'bbox': db.session.scalar(functions.ST_AsGeoJSON(self.bbox)),
            'custom_fields':self.custom_fields
        }

class Repositorie(db.Model):

    __tablename__ = 'research_data_repositories'

    repo_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    abstract = db.Column(db.String(500), unique=False, nullable=False)
    maintainer = db.Column(db.String(355), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)
    
    
    def __init__(self, name, abstract, maintainer, created_on):
        self.name = name
        self.abstract = abstract
        self.maintainer = maintainer
        self.created_on = created_on
   
    def serialize(self):

        return {            
            'repo_id': self.repo_id, 
            'name': self.name,
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

class Repositorie_User(db.Model):

    __tablename__ = 'research_data_repositories_users'
    __table_args__ = (
        PrimaryKeyConstraint('repo_id', 'user_id'),
    )

    repo_id = db.Column(db.Integer, db.ForeignKey('research_data_repositories.repo_id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)

    def __init__(self, repo_id, user_id):
        self.repo_id = repo_id
        self.user_id = user_id

    def serialize(self):

        return {            
            'repo_id': self.repo_id, 
            'user_id': self.user_id
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
     
class Repositorie_Keyword(db.Model):

    __tablename__ = 'research_data_repositories_keywords'
    __table_args__ = (
        PrimaryKeyConstraint('repo_id', 'keyword_id'),
    )

    repo_id = db.Column(db.Integer, db.ForeignKey('research_data_repositories.repo_id'),nullable=False)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.keyword_id'),nullable=False)

    def __init__(self, repo_id, keyword_id):
        self.repo_id = repo_id
        self.keyword_id = keyword_id

    def serialize(self):

        return {            
            'repo_id': self.repo_id, 
            'keyword_id': self.keyword_id
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
       