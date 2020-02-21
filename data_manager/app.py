#!flask/bin/python
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, request, redirect, url_for
from flask_migrate import Migrate, MigrateCommand
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from flask import make_response
from sqlalchemy import update
from flask_cors import CORS
from flask import request
from flask import url_for
from flask import abort
from models import *
import datetime
import json
import os

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
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#app
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jwt = JWTManager(app)

#check_if_token_in_blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:8090/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "TerraBrasilis Research Data"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

#db
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

#errorhandler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#uri repositories
def make_public_repositorie(repositorie):
    new_repositorie = {}
    for field in repositorie:
            new_repositorie[field] = repositorie[field]
    return new_repositorie

#uri groups
def make_public_group(group):
    new_groups = {}
    for field in group:
        new_groups[field] = group[field]
    return new_groups

#uri users
def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'user_id':
            new_user[field] = user[field]
            #new_user['uri'] = url_for('read_user', user_id=user['user_id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user

#uri service
def make_public_service(service):
    new_service = {}
    for field in service:
        if field == 'service_id':
            new_service[field] = service[field]
            #new_service['uri'] = url_for('get_service', service_id=service['service_id'], _external=True)
        else:
            new_service[field] = service[field]
    return new_service

#create_user()
@app.route('/api/v1.0/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' and 'password' and 'image' and "full_name" and "email" and "created_on" and "last_login" and 'ckan_api_key' in request.json:
        abort(400)
    username=request.json['username']
    password=request.json['password']
    full_name=request.json['full_name']
    email=request.json['email']
    image=request.json['image']
    created_on=request.json['created_on']
    last_login=request.json['last_login']
    ckan_api_key = request.json['ckan_api_key']
    try:
        user=User(
            username = username,
            password = User.generate_hash(password),
            full_name = full_name,
            email = email,
            image = image,
            created_on = created_on,
            last_login = last_login,
            ckan_api_key = ckan_api_key
        )
        db.session.add(user)
        db.session.commit()
 
        access_token = create_access_token(identity = request.json['username'], expires_delta = datetime.timedelta(days=365))
        refresh_token = create_refresh_token(identity = request.json['username'], expires_delta = datetime.timedelta(days=365))

        return jsonify({
            'message': 'User {} was created'.format(request.json['username']),
            'access_token': access_token,
            'refresh_token': refresh_token,
            'ckan_api_key': request.json['ckan_api_key']})
           
    except Exception as e:
        return(str(e))

#read_users()
@app.route("/api/v1.0/users")
def read_users():
    try:
        users=User.query.all()
        return jsonify([make_public_user(e.serialize()) for e in users])
    except Exception as e:
	    return(str(e))
		
#read_user(user_id)
@app.route("/api/v1.0/users/<int:user_id>", methods=['GET'])
def read_user(user_id):
    try:
        user=User.query.filter_by(user_id=user_id).first()
        return jsonify(user.serialize())
    except Exception as e:
	    return(str(e))

#update_user(user_id)
@app.route("/api/v1.0/users/<int:user_id>", methods=['PUT'])
@jwt_required
def update_user(user_id):
    if not request.json or not 'username' and "password" and  'image' and "full_name" and "email" and "created_on" and "last_login" and "ckan_api_key" in request.json:
        abort(400)
    username=request.json['username']
    full_name=request.json['full_name']
    password=request.json['password']
    email=request.json['email']
    image=request.json['image']
    created_on=request.json['created_on']
    last_login=request.json['last_login']
    ckan_api_key= request.json['ckan_api_key']
    try:

        q = (db.session.query(User)
            .filter(User.user_id == user_id)
        )

        new_user = q.one()
        new_user.username = username
        new_user.full_name = full_name
        new_password = User.generate_hash(password),
        new_user.email = email
        new_user.image = image
        new_user.created_on = created_on
        new_user.last_login = last_login
        new_user.ckan_api_key = ckan_api_key

        db.session.commit()

        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#delete_user(service_id)
@app.route("/api/v1.0/users/<int:user_id>", methods=['DELETE'])
@jwt_required
def delete_user(user_id):
    try:
        user = db.session.query(User).filter_by(user_id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#create_group_repositorie_rel()
@app.route('/api/v1.0/group_repositorie_rel', methods=['POST'])
@jwt_required
def create_group_repositorie_rel():
    if not request.json or not 'group_id' and 'repo_id' in request.json:
        abort(400)
    group_id=request.json['group_id']
    repo_id=request.json['repo_id']
    try:
        group_repositorie=Repositorie_Group(
            repo_id = repo_id,
            group_id = group_id
        )
        db.session.add(group_repositorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#read_group_repositorie_rel()
@app.route('/api/v1.0/group_repositorie_rel/<int:repo_id>', methods=['GET'])
def read_group_repositorie_rel(repo_id):
    try:
        group_repositorie=Repositorie_Group.query.filter_by(repo_id=repo_id).first()
        return jsonify(group_repositorie.serialize())
    except Exception as e:
	    return(str(e))

#delete_group_repositorie_rel(group_id,repo_id)
@app.route("/api/v1.0/group_repositorie_rel/<int:group_id>/<int:repo_id>", methods=['DELETE'])
@jwt_required
def delete_group_repositorie_rel(group_id,repo_id):
    try:
        group_repositorie = db.session.query(Repositorie_Group).filter_by(group_id=group_id, repo_id=repo_id).first()
        db.session.delete(group_repositorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#create_user_group_rel()
@app.route('/api/v1.0/user_group_rel', methods=['POST'])
@jwt_required
def create_user_group_rel():
    if not request.json or not 'user_id' and 'group_id' in request.json:
        abort(400)
    user_id=request.json['user_id']
    group_id=request.json['group_id']
    try:
        user_group=Groups_User(
            group_id = group_id,
            user_id = user_id
        )
        db.session.add(user_group)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#delete_user_group_rel(user_id,group_id)
@app.route("/api/v1.0/user_group_rel/<int:user_id>/<int:group_id>", methods=['DELETE'])
@jwt_required
def delete_user_group_rel(user_id,group_id):
    try:
        group_user = db.session.query(Groups_User).filter_by(user_id=user_id, group_id=group_id).first()
        db.session.delete(group_user)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#create_service()
@app.route('/api/v1.0/services', methods=['POST'])
@jwt_required
def create_service():
    if not request.json or not 'name' and 'machine' and 'host_id' and 'created_on' in request.json:
        abort(400)
    name=request.json['name']
    machine=request.json['machine']
    host_id=request.json['host_id']
    created_on=request.json['created_on']
    
    try:
        service=Service(
            name=name,
            machine=machine,
            host_id=host_id,
            created_on=created_on
        )
        db.session.add(service)
        db.session.commit()
        services=Service.query.filter_by(name = request.json['name'], host_id = request.json['host_id'])
        return jsonify([make_public_service(e.serialize()) for e in services])
    except Exception as e:
        return(str(e))

#read_services()
@app.route("/api/v1.0/services", methods=['GET'])
def read_services():
    try:
        services=Service.query.all()
        return jsonify([make_public_service(e.serialize()) for e in services])

    except Exception as e:
	    return(str(e))	

#read_service(service_id)
@app.route("/api/v1.0/services/<int:service_id>", methods=['GET'])
def read_service(service_id):
    try:
        db.session.commit()
        return jsonify(service.serialize())
    except Exception as e:
	    return(str(e))

#delete_service(service_id)
@app.route("/api/v1.0/services/<int:service_id>", methods=['DELETE'])
@jwt_required
def delete_service(service_id):
    try:
        service = db.session.query(Service).filter_by(service_id=service_id).first()
        db.session.delete(service)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#create_service_repositorie_rel()
@app.route('/api/v1.0/service_repositorie_rel', methods=['POST'])
@jwt_required
def create_service_repositorie_rel():
    if not request.json or not 'service_id' and 'repo_id' in request.json:
        abort(400)
    service_id=request.json['service_id']
    repo_id=request.json['repo_id']
    try:
        service_repositorie=Repositorie_Service(
            repo_id = repo_id,
            service_id = service_id
        )
        db.session.add(service_repositorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#delete_service_repositorie_rel(service_id,repo_id)
@app.route("/api/v1.0/service_repositorie_rel/<int:service_id>/<int:repo_id>", methods=['DELETE'])
@jwt_required
def delete_service_repositorie_rel(service_id,repo_id):
    try:
        repo_service = db.session.query(Repositorie_Service).filter_by(service_id=service_id, repo_id=repo_id).first()
        db.session.delete(repo_service)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#read_categories()
@app.route("/api/v1.0/categories", methods=['GET'])
def read_categories():
    try:
        categories=Categorie.query.all()
        return jsonify([e.serialize() for e in categories])

    except Exception as e:
	    return(str(e))

#create_categorie()
@app.route('/api/v1.0/categories', methods=['POST'])
@jwt_required
def create_categorie():
    if not request.json or not 'name' in request.json:
        abort(400)
    name=request.json['name']
    try:
        categorie=Categorie(
            name = name
        )
        db.session.add(categorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#create_categorie_repositorie_rel()
@app.route('/api/v1.0/categorie_repositorie_rel', methods=['POST'])
@jwt_required
def create_categorie_repositorie_rel():
    if not request.json or not 'repo_id' and 'categorie_id' in request.json:
        abort(400)
    repo_id=request.json['repo_id']
    categorie_id=request.json['categorie_id']
    try:
        categorie_repositorie=Repositorie_Categorie(
            repo_id = repo_id,
            categorie_id = categorie_id,
        )
        db.session.add(categorie_repositorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#delete_categorie_repositorie_rel(categorie_id,repo_id)
@app.route("/api/v1.0/categorie_repositorie_rel/<int:categorie_id>/<int:repo_id>", methods=['DELETE'])
@jwt_required
def delete_categorie_repositorie_rel(categorie_id,repo_id):
    try:
        repo_categorie = db.session.query(Repositorie_Categorie).filter_by(categorie_id=categorie_id, repo_id=repo_id).first()
        db.session.delete(repo_categorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#create_service_port_rel()
@app.route('/api/v1.0/service_port_rel', methods=['POST'])
@jwt_required
def create_service_port_rel():
    if not request.json or not 'port_id' and 'service_id' in request.json:
        abort(400)
    port_id=request.json['port_id']
    service_id=request.json['service_id']
    try:
        service_port=Service_Port(
            port_id = port_id,
            service_id = service_id,
        )
        db.session.add(service_port)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#create_service_host_rel()
@app.route('/api/v1.0/service_host_rel', methods=['POST'])
@jwt_required
def create_service_host_rel():
    if not request.json or not 'host_id' and 'service_id' in request.json:
        abort(400)
    host_id=request.json['host_id']
    service_id=request.json['service_id']
    try:
        service_host=Service_Host(
            host_id = host_id,
            service_id = service_id,
        )
        db.session.add(service_host)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#read_hosts()
@app.route("/api/v1.0/hosts", methods=['GET'])
def read_hosts():
    try:
        hosts=Host.query.all()
        return jsonify([e.serialize() for e in hosts])

    except Exception as e:
	    return(str(e))

#create_host()
@app.route('/api/v1.0/hosts', methods=['POST'])
@jwt_required
def create_host():
    if not request.json or not 'name' and 'address' and 'created_on' in request.json:
        abort(400)

    name = request.json['name']
    address = request.json['address']
    created_on = request.json['created_on']
    try:
        host=Host(
            name = name,
            address = address,
            created_on = created_on
        )
        db.session.add(host)
        db.session.commit()
        hosts=Host.query.filter_by(address = request.json['address'])
        return jsonify([e.serialize() for e in hosts])
    except Exception as e:
        return(str(e))

#read_ports(repo_id)
@app.route("/api/v1.0/ports/<int:repo_id>", methods=['GET'])
def read_ports(repo_id):
    try:
        
        #create lists
        list_ser = []
        list_por = []

        repo_ser = Repositorie_Service.query.filter(Repositorie_Service.repo_id.in_([repo_id]))
        r_ser = ([e.serialize() for e in repo_ser])

        for j in range(len(r_ser)):
            list_ser.append(r_ser[j]['service_id'])

        ser_port = Service_Port.query.filter(Service_Port.service_id.in_(list_ser))
        s_port = ([e.serialize() for e in ser_port])

        for k in range(len(s_port)):
            list_por.append(s_port[k]['port_id'])

        #create port dict
        ports = Port.query.filter(Port.port_id.in_(list_por))

        return jsonify([e.serialize() for e in ports])

    except Exception as e:
	    return(str(e))

#create_repositorie()
@app.route('/api/v1.0/repositories', methods=['POST'])
@jwt_required
def create_repositorie():
    if not request.json or not 'name' and 'abstract' and 'maintainer' and 'created_on' in request.json:
        abort(400)

    name = request.json['name']
    abstract = request.json['abstract']
    maintainer = request.json['maintainer']
    created_on = request.json['created_on']
    try:
        repositorie=Repositorie(
            name = name,
            abstract = abstract,
            maintainer = maintainer,
            created_on = created_on
        )
        db.session.add(repositorie)
        db.session.commit()
        repositorie=Repositorie.query.filter_by(name = request.json['name'])
        return jsonify([e.serialize() for e in repositorie])
    except Exception as e:
        return(str(e))

#read_repositories()
@app.route("/api/v1.0/repositories", methods=['GET'])
def read_repositories():
    try:
        #query all
        repositories=Repositorie.query.all()
       
        #get lists
        data = ([(make_public_repositorie(e.serialize())) for e in repositories])
        id_data = ([e.serialize() for e in repositories])
        
        #create data dict
        json_data = {}
        for val in data: 
            json_data.setdefault('repositorie', []).append(val)
        
        lista = []

        #create response dict
        json_response = {}
        for i in range(len(data)):

            #create lists
            list_ser = []
            list_cat = []
            list_key = []

            #create lists
            repo_ser = Repositorie_Service.query.filter(Repositorie_Service.repo_id.in_([id_data[i]['repo_id']]))
            r_ser = ([e.serialize() for e in repo_ser])
          
            repo_cat = Repositorie_Categorie.query.filter(Repositorie_Categorie.repo_id.in_([id_data[i]['repo_id']]))
            r_cat = ([e.serialize() for e in repo_cat])

            for j in range(len(r_ser)):
                list_ser.append(r_ser[j]['service_id'])

            for l in range(len(r_cat)):
                list_cat.append(r_cat[l]['categorie_id'])
  
            #create categories dict
            categories=Categorie.query.filter(Categorie.categorie_id.in_(list_cat))
            cate = ([e.serialize() for e in categories])
            json_cate = {}
            for val in cate: 
                json_cate.setdefault('categories', []).append(val['name'])
            
            #create services dict
            services = Service.query.filter(Service.service_id.in_(list_ser))
            ser = ([make_public_service(e.serialize()) for e in services])
            json_ser = {}
            for val in ser: 
                json_ser.setdefault('services', []).append(val)
            
            for n in range(len(ser)):
                hosts = Host.query.filter(Host.host_id.in_([json_ser['services'][n]['host_id']]))
                hos = ([e.serialize() for e in hosts])
                
                ser_port = Service_Port.query.filter(Service_Port.service_id.in_( [json_ser['services'][n]['service_id']] ))
                s_port = ([e.serialize() for e in ser_port])

                list_por = []
                for k in range(len(s_port)):
                    list_por.append(s_port[k]['port_id'])

                ports = Port.query.filter(Port.port_id.in_(list_por))
                por = ([e.serialize() for e in ports])

                json_ports = {}
                for val in por: 
                    json_ports.setdefault('ports', []).append(val['port'])

                json_ser['services'][n].update({ "ports" : json_ports['ports'] })

                json_ser['services'][n].update({ "address" : str(hos[0]['address']) + str(json_ser['services'][n]['machine']) })
                del json_ser['services'][n]['host_id']
                del json_ser['services'][n]['machine']
                del json_ser['services'][n]['service_id']

            #compose
            json_data['repositorie'][i].update({"services": json_ser['services']})
            json_data['repositorie'][i].update({"categories": json_cate['categories']})
            json_response.setdefault("repositorie", []).append(json_data['repositorie'][i])

        return jsonify(json_response)

    except Exception as e:
	    return(str(e))

#read_repositories(repo_id)
@app.route("/api/v1.0/repositories/<int:repo_id>", methods=['GET'])
def read_repositorie(repo_id):
    try:
        
        #query single id
        repositories=Repositorie.query.filter_by(repo_id=repo_id).first()

        #create data dict
        json_data = (repositories.serialize())
        

        #create lists
        list_ser = []
        list_cat = []
        list_key = []

        #create lists 
        repo_ser = Repositorie_Service.query.filter(Repositorie_Service.repo_id.in_([repo_id]))
        r_ser = ([e.serialize() for e in repo_ser])

        repo_cat = Repositorie_Categorie.query.filter(Repositorie_Categorie.repo_id.in_([repo_id]))
        r_cat = ([e.serialize() for e in repo_cat])

        for j in range(len(r_ser)):
            list_ser.append(r_ser[j]['service_id'])

        for l in range(len(r_cat)):
            list_cat.append(r_cat[l]['categorie_id'])

        #create categories dict
        categories=Categorie.query.filter(Categorie.categorie_id.in_(list_cat))
        cate = ([e.serialize() for e in categories])
        json_cate = {}
        for val in cate: 
            json_cate.setdefault('categories', []).append(val['name'])
        
        #create services dict
        services = Service.query.filter(Service.service_id.in_(list_ser))
        ser = ([make_public_service(e.serialize()) for e in services])
        json_ser = {}
        for val in ser: 
            json_ser.setdefault('services', []).append(val)

        for n in range(len(ser)):
            hosts = Host.query.filter(Host.host_id.in_([json_ser['services'][n]['host_id']]))
            hos = ([e.serialize() for e in hosts])

            ser_port = Service_Port.query.filter(Service_Port.service_id.in_( [json_ser['services'][n]['service_id']] ))
            s_port = ([e.serialize() for e in ser_port])

            list_por = []
            for k in range(len(s_port)):
                list_por.append(s_port[k]['port_id'])

            ports = Port.query.filter(Port.port_id.in_(list_por))
            por = ([e.serialize() for e in ports])
            
            json_ports = {}
            for val in por: 
                json_ports.setdefault('ports', []).append(val['port'])

            json_ser['services'][n].update({ "ports" : json_ports['ports'] })
            json_ser['services'][n].update({ "address" : str(hos[0]['address']) + str(json_ser['services'][n]['machine']) })

            del json_ser['services'][n]['host_id']
            del json_ser['services'][n]['machine']
            del json_ser['services'][n]['service_id']
            
        #create response dict
        json_response = {}
        json_data.update(json_ser)
        json_data.update(json_cate)
        json_response.setdefault("repositorie", []).append(json_data)

        return jsonify(json_response)

    except Exception as e:
	    return(str(e))

#update_repositorie(repo_id)
@app.route('/api/v1.0/repositories/<int:repo_id>', methods=['PUT'])
@jwt_required
def update_repositorie(repo_id):
    if not request.json or not 'name' and 'abstract' and 'maintainer' and 'created_on' and 'language' in request.json:
        abort(400)
    name = request.json['name']
    abstract = request.json['abstract']
    maintainer = request.json['maintainer']
    created_on = request.json['created_on']
    language = request.json['language']
    try:

        q = (db.session.query(Repositorie)
            .filter(Repositorie.repo_id == repo_id)
        )

        new_repo = q.one()
        new_repo.name = name
        new_repo.abstract = abstract
        new_repo.maintainer = maintainer
        new_repo.created_on = created_on
        new_repo.language = language

        db.session.commit()

        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#delete_repositorie(repo_id)
@app.route("/api/v1.0/repositories/<int:repo_id>", methods=['DELETE'])
@jwt_required
def delete_repositorie(repo_id):
    try:
        repositorie = db.session.query(Repositorie).filter_by(repo_id=repo_id).first()
        db.session.delete(repositorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#create_group()
@app.route("/api/v1.0/groups", methods=['POST'])
@jwt_required
def create_group():
    if not request.json or not 'name' and 'abstract' and 'maintainer' and 'created_on' and 'language' and 'image' in request.json:
        abort(400)

    name = request.json['name']
    abstract = request.json['abstract']
    maintainer = request.json['maintainer']
    created_on = request.json['created_on']
    language = request.json['language']
    image = request.json['image']

    try:
        group=Group(
            name = name,
            abstract = abstract,
            maintainer = maintainer,
            created_on = created_on,
            language = language,
            image = image

        )
        db.session.add(group)
        db.session.commit()        
        group=Group.query.filter_by(name = request.json['name'], abstract = request.json['abstract'])
        return jsonify([e.serialize() for e in group])
    except Exception as e:
        return(str(e))

#read_groups()
@app.route("/api/v1.0/groups", methods=['GET'])
def read_groups():
    try:
        #query all
        groups=Group.query.all()
       
        #get lists
        data = ([(make_public_group(e.serialize())) for e in groups])
        id_data = ([e.serialize() for e in groups])
        
        #create data dict
        json_data = {}
        for val in data: 
            json_data.setdefault('groups', []).append(val)
        
        lista = []

        #create response dict
        json_response = {}
        for i in range(len(data)):

            #create lists
            list_user = []
          
            #create lists
            grup_usr = Groups_User.query.filter(Groups_User.group_id.in_([id_data[i]['group_id']]))

            r_user = ([e.serialize() for e in grup_usr])

            for k in range(len(r_user)):
                list_user.append(r_user[k]['user_id'])

            #create users dict
            users=User.query.filter(User.user_id.in_(list_user))
            
            members = ([make_public_user(e.serialize()) for e in users])

            json_users = {}

            for val in members: 
                json_users.setdefault('users', []).append(val)

            #compose
            json_data['groups'][i].update({"users": json_users['users']})
            json_response.setdefault("groups", []).append(json_data['groups'][i])

        return jsonify(json_response)

    except Exception as e:
	    return(str(e))

#read_groups(group_id)
@app.route("/api/v1.0/groups/<int:group_id>", methods=['GET'])
def read_group(group_id):
    try:
        
        #query single id
        groups=Group.query.filter_by(group_id=group_id).first()

        #create data dict
        json_data = (groups.serialize())

        #create lists
        list_user = []

        #create lists 
        grup_usr = Groups_User.query.filter(Groups_User.group_id.in_([group_id]))
        r_user = ([e.serialize() for e in grup_usr])

        for k in range(len(r_user)):
            list_user.append(r_user[k]['user_id'])

        #create users dict
        users=User.query.filter(User.user_id.in_(list_user))
        members = ([make_public_user(e.serialize()) for e in users])
        json_users = {}
        for val in members: 
            json_users.setdefault('users', []).append(val)

        #create response dict
        json_response = {}
        json_data.update(json_users)
        json_response.setdefault("groups", []).append(json_data)

        return jsonify(json_response)

    except Exception as e:
	    return(str(e))

#update_group(group_id)
@app.route('/api/v1.0/groups/<int:group_id>', methods=['PUT'])
@jwt_required
def update_group(group_id):
    if not request.json or not 'name' and 'abstract' and 'maintainer' and 'created_on' and 'language' and 'image' in request.json:
        abort(400)
    name = request.json['name']
    abstract = request.json['abstract']
    maintainer = request.json['maintainer']
    created_on = request.json['created_on']
    language = request.json['language']
    image = request.json['image']
    custom_fields = request.json['custom_fields']
    try:

        q = (db.session.query(Group)
            .filter(Groups.group_id == group_id)
        )

        new_group = q.one()
        new_group.name = name
        new_group.abstract = abstract
        new_group.maintainer = maintainer
        new_group.created_on = created_on
        new_group.language = language
        new_group.image = image
        new_group.custom_fields = custom_fields

        db.session.commit()

        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#delete_group(group_id)
@app.route("/api/v1.0/groups/<int:group_id>", methods=['DELETE'])
@jwt_required
def delete_group(group_id):
    try:
        group = db.session.query(Group).filter_by(group_id=group_id).first()
        db.session.delete(group)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
	    return(str(e))

#UserLogin()
@app.route("/api/v1.0/login", methods=['POST'])
def UserLogin():
    if not request.json or not 'username' and 'password' in request.json:
        abort(400)

    username = request.json['username']
    password = request.json['password']

    current_user = User.find_by_username(request.json['username'])
    
    if not current_user:
        return jsonify({'message': 'User {} doesn\'t exist'.format(request.json['username'])})
    
    if User.verify_hash(request.json['password'], current_user.password):

        access_token = create_access_token(identity = request.json['username'], expires_delta = datetime.timedelta(days=365))
        refresh_token = create_refresh_token(identity = request.json['username'], expires_delta = datetime.timedelta(days=365))

        return jsonify({'user_id': current_user.user_id, 
                        'full_name': current_user.full_name,
                        'access_token': access_token,
                        'message': 'User {} log in successfully.'.format(current_user.full_name),
                        'refresh_token': refresh_token,
                        'ckan_api_key': current_user.ckan_api_key})
    else:
        return jsonify({'message': 'Wrong credentials'})

#TokenRefresh()
@app.route("/api/v1.0/token/refresh", methods=['POST'])
@jwt_refresh_token_required
def TokenRefresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity = current_user, expires_delta = datetime.timedelta(days=365))

    return jsonify({'access_token': access_token})

#UserLogoutAccess()
@app.route("/api/v1.0/logout/access", methods=['POST'])
@jwt_required
def UserLogoutAccess():
    jti = get_raw_jwt()['jti']
    try:
        
        revoked_token=RevokedTokenModel(
            jti = jti
        )
        db.session.add(revoked_token)
        db.session.commit()

        return jsonify({'message': 'Access token has been revoked'})
    except:
        return jsonify({'message': 'Something went wrong'}, 500)

#UserLogoutRefresh()
@app.route("/api/v1.0/logout/refresh", methods=['POST'])
@jwt_refresh_token_required
def UserLogoutRefresh():
    jti = get_raw_jwt()['jti']
    try:
        
        revoked_token=RevokedTokenModel(
            jti = jti
        )
        db.session.add(revoked_token)
        db.session.commit()

        return jsonify({'message': 'Refresh token has been revoked'})
    except:
        return jsonify({'message': 'Something went wrong'}, 500)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
#imageUpload
@app.route("/api/v1.0/image_upload", methods=['POST'])
def imageUpload():
    try:
        # Retrieves file upload
        image = request.files.get('image')
        image.save(os.path.join(UPLOAD_FOLDER, image.filename))

        return jsonify({'message': 'Success'})
    except:
        return jsonify({'message': 'Something went wrong'}, 500)

#download_file
@app.route("/api/v1.0/uploads/<path:filename>", methods=['GET'])
def download_file(filename):
    #try:
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)
    #except:
    #    return jsonify({'message': 'Something went wrong'}, 500)

if __name__ == '__main__':
    app.run(get_env_variable("HOST_IP"), debug=True, port=8090)
