from app import db

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    full_name = db.Column(db.String(355), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(355), unique=False, nullable=False)
    image = db.Column(db.String(355), unique=False, nullable=False)
    created_on = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    last_login = db.Column(db.TIMESTAMP, unique=False, nullable=False)

    def __init__(self, username, full_name, password, email, image, created_on, last_login):
        self.username = username
        self.full_name = full_name
        self.password = password
        self.email = email
        self.image = image
        self.created_on = created_on
        self.last_login = last_login

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
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
    created_on = db.Column(db.TIMESTAMP, unique=False, nullable=False)

    def __init__(self, name, machine, host_id, created_on):
        self.name = name
        self.machine = machine
        self.host_id = host_id
        self.created_on = created_on

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
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
            'id': self.categorie_id, 
            'name': self.name
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
            'id': self.keyword_id, 
            'name': self.name
        }


#class Repositorie(db.Model):
#    __tablename__ = 'research_data_repositories'
