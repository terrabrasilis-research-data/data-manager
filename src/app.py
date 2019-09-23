#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_httpauth import HTTPBasicAuth
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import url_for
from flask import abort
from models import *
import datetime
import json
import os

#auth
auth = HTTPBasicAuth()

#env
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

#values
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

#app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#db
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)

#oath
@auth.get_password
def get_password(username):
    if username == 'gabriel':
        return 'gabriel'
    return None

#oath
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

#errorhandler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
       
#new_bbox
def new_bbox(repositories):
    new_repositorie = {}
    for field in repositories:
        if field == 'bbox':
            new_repositorie[field] = repositories[field]
    return new_repositorie

#remove_bbox
def remove_bbox(repositories):
    new_repositorie = {}
    for field in repositories:
        if field != 'bbox':
            new_repositorie[field] = repositories[field]
    return new_repositorie

#remove_id
def remove_id(categories):
    new_categories = {}
    for field in categories:
        if field != 'id':
            new_categories[field] = categories[field]
    return new_categories
        
#uri repositories
def make_public_repositorie(repositorie):
    new_repositorie = {}
    for field in repositorie:
        if field == 'repo_id':
            new_repositorie['uri'] = url_for('get_repositorie', repo_id=repositorie['repo_id'], _external=True)
        else:
            new_repositorie[field] = repositorie[field]
    return new_repositorie

#uri users
def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'user_id':
            new_user['uri'] = url_for('get_user', user_id=user['user_id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user

#uri service
def make_public_service(service):
    new_service = {}
    for field in service:
        if field == 'service_id':
            new_service['uri'] = url_for('get_service', service_id=service['service_id'], _external=True)
        else:
            new_service[field] = service[field]
    return new_service

#get_users()
@app.route("/api/v1.0/users")
def get_users():
    try:
        users=User.query.all()
        return jsonify([make_public_user(e.serialize()) for e in users])
    except Exception as e:
	    return(str(e))
		
#get_user(user_id)
@app.route("/api/v1.0/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    try:
        user=User.query.filter_by(user_id=user_id).first()
        return jsonify(user.serialize())
    except Exception as e:
	    return(str(e))

#create_user()
@app.route('/api/v1.0/users', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or not 'username' and 'password' and 'image' in request.json:
        abort(400)
    username=request.json['username']
    full_name=request.json['full_name']
    password=request.json['password']
    email=request.json['email']
    image=request.json['image']
    created_on=request.json['created_on']
    last_login=request.json['last_login']
    try:
        user=User(
            username = username,
            full_name = full_name,
            password = password,
            email = email,
            image = image,
            created_on = created_on,
            last_login = last_login
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#get_services()
@app.route("/api/v1.0/services", methods=['GET'])
def get_services():
    try:
        services=Service.query.all()
        return jsonify([make_public_service(e.serialize()) for e in services])

    except Exception as e:
	    return(str(e))	

#get_service(service_id)
@app.route("/api/v1.0/services/<int:service_id>")
def get_service(service_id):
    try:
        service=Service.query.filter_by(service_id=service_id).first()
        return jsonify(service.serialize())
    except Exception as e:
	    return(str(e))

#get_categories()
@app.route("/api/v1.0/categories", methods=['GET'])
def get_categories():
    try:
        categories=Categorie.query.all()
        return jsonify([e.serialize() for e in categories])

    except Exception as e:
	    return(str(e))

#get_keywords()
@app.route("/api/v1.0/keywords", methods=['GET'])
def get_keywords():
    try:
        keywords=Keywords.query.all()
        return jsonify([e.serialize() for e in keywords])

    except Exception as e:
	    return(str(e))

#get_repositories()
@app.route("/api/v1.0/repositories", methods=['GET'])
def get_repositories():
    try:
        #query all
        repositories=Repositorie.query.all()
       
        #get lists
        data = ([remove_bbox(make_public_repositorie(e.serialize())) for e in repositories])
        bbox = ([new_bbox(e.serialize()) for e in repositories])
        
        #create data dict
        json_data = {}
        for val in data: 
            json_data.setdefault('repositorie', []).append(val)
        
        #create bboxs dict
        json_bbox = {}
        for val in bbox: 
            json_bbox.setdefault('bbox', []).append(val)
        
        #create response dict
        json_response = {}
        for i in range(len(data)):
            
            #create categories dict
            categories=Categorie.query.all() #filter for each in FK table
            cate = ([remove_id(e.serialize()) for e in categories])
            json_cate = {}
            for val in cate: 
                json_cate.setdefault('categories', []).append(val)

            #create users dict
            users=User.query.all() #filter for each in FK table
            members = ([make_public_user(e.serialize()) for e in users])
            json_users = {}
            for val in members: 
                json_users.setdefault('users', []).append(val)
            
            #create services dict
            services = Service.query.all() #filter for each in FK table
            ser = ([make_public_service(e.serialize()) for e in services])
            json_ser = {}
            for val in ser: 
                json_ser.setdefault('services', []).append(val)
            
            #compose
            json_data['repositorie'][i].update(json_bbox['bbox'][i])
            json_data['repositorie'][i].update({"services": [json_ser['services']]})
            json_data['repositorie'][i].update({"users": [json_users['users']]})
            json_data['repositorie'][i].update({"categories": [json_cate['categories']]})
            json_response.setdefault("repositorie", []).append(json_data['repositorie'][i])

        return jsonify(json_response)

    except Exception as e:
	    return(str(e))

#get_repositories(repo_id)
@app.route("/api/v1.0/repositories/<int:repo_id>", methods=['GET'])
def get_repositorie(repo_id):
    try:
        
        #query single id
        repositories=Repositorie.query.filter_by(repo_id=repo_id).first()

        #create data dict
        json_data = remove_bbox(repositories.serialize())
        
        #create bbox dict
        json_bbox = new_bbox(repositories.serialize())

        #create users dict
        users=User.query.all()#filter for each in FK table
        members = ([make_public_user(e.serialize()) for e in users])
        json_users = {}
        for val in members: 
            json_users.setdefault('users', []).append(val)
        
        #create services dict    
        services = Service.query.all() #filter for each in FK table
        ser = ([make_public_service(e.serialize()) for e in services])
        json_ser = {}
        for val in ser: 
            json_ser.setdefault('services', []).append(val)

        #create categories dict
        categories=Categorie.query.all() #filter for each in FK table
        cate = ([remove_id(e.serialize()) for e in categories])
        json_cate = {}
        for val in cate: 
            json_cate.setdefault('categories', []).append(val)

        #create response dict
        json_response = {}
        json_data.update(json_bbox)
        json_data.update(json_ser)
        json_data.update(json_users)
        json_data.update(json_cate)
        json_response.setdefault("repositorie", []).append(json_data)

        return jsonify(json_response)

    except Exception as e:
	    return(str(e))

#create_repositorie()
@app.route('/api/v1.0/repositories', methods=['POST'])
@auth.login_required
def create_repositorie():
    if not request.json or not 'name' and 'abstract' and 'maintainer' in request.json:
        abort(400)

    name = request.json['name']
    abstract = request.json['abstract']
    maintainer = request.json['maintainer']
    created_on = request.json['created_on']
    language = request.json['language']
    bbox = request.json['bbox']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    custom_fields = request.json['custom_fields']
    try:
        repositorie=Repositorie(
            name = name,
            abstract = abstract,
            maintainer = maintainer,
            created_on = created_on,
            language = language,
            bbox = bbox,
            start_date = start_date,
            end_date = end_date,
            custom_fields = custom_fields
        )
        db.session.add(repositorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#app
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)