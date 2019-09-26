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
            new_service[field] = service[field]
            #new_service['uri'] = url_for('get_service', service_id=service['service_id'], _external=True)
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

#create_user_repositorie_rel()
@app.route('/api/v1.0/user_repositorie_rel', methods=['POST'])
@auth.login_required
def create_user_repositorie_rel():
    if not request.json or not 'user_id' and 'repo_id' in request.json:
        abort(400)
    user_id=request.json['user_id']
    repo_id=request.json['repo_id']
    try:
        user_repositorie=Repositorie_User(
            repo_id = repo_id,
            user_id = user_id
        )
        db.session.add(user_repositorie)
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

#create_service_repositorie_rel()
@app.route('/api/v1.0/service_repositorie_rel', methods=['POST'])
@auth.login_required
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

#get_categories()
@app.route("/api/v1.0/categories", methods=['GET'])
def get_categories():
    try:
        categories=Categorie.query.all()
        return jsonify([e.serialize() for e in categories])

    except Exception as e:
	    return(str(e))

#create_categorie()
@app.route('/api/v1.0/categories', methods=['POST'])
@auth.login_required
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
@auth.login_required
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

#get_keywords()
@app.route("/api/v1.0/keywords", methods=['GET'])
def get_keywords():
    try:
        keywords=Keywords.query.all()
        return jsonify([e.serialize() for e in keywords])

    except Exception as e:
	    return(str(e))

#create_keywords()
@app.route('/api/v1.0/keywords', methods=['POST'])
@auth.login_required
def create_keywords():
    if not request.json or not 'name' in request.json:
        abort(400)
    name=request.json['name']
    try:
        keyword=Keywords(
            name = name
        )
        db.session.add(keyword)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#create_keyword_repositorie_rel()
@app.route('/api/v1.0/keyword_repositorie_rel', methods=['POST'])
@auth.login_required
def create_keyword_repositorie_rel():
    if not request.json or not 'repo_id' and 'keyword_id' in request.json:
        abort(400)
    repo_id=request.json['repo_id']
    keyword_id=request.json['keyword_id']
    try:
        keyword_repositorie=Repositorie_Keyword(
            repo_id = repo_id,
            keyword_id = keyword_id,
        )
        db.session.add(keyword_repositorie)
        db.session.commit()
        return jsonify({'result': True})
    except Exception as e:
        return(str(e))

#get_hosts()
@app.route("/api/v1.0/hosts", methods=['GET'])
def get_hosts():
    try:
        hosts=Host.query.all()
        return jsonify([e.serialize() for e in hosts])

    except Exception as e:
	    return(str(e))

#get_ports(repo_id)
@app.route("/api/v1.0/ports/<int:repo_id>", methods=['GET'])
def get_ports(repo_id):
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

#get_repositories()
@app.route("/api/v1.0/repositories", methods=['GET'])
def get_repositories():
    try:
        #query all
        repositories=Repositorie.query.all()
       
        #get lists
        data = ([remove_bbox(make_public_repositorie(e.serialize())) for e in repositories])
        id_data = ([e.serialize() for e in repositories])
        bbox = ([new_bbox(e.serialize()) for e in repositories])
        
        #create data dict
        json_data = {}
        for val in data: 
            json_data.setdefault('repositorie', []).append(val)
        
        #create bboxs dict
        json_bbox = {}
        for val in bbox: 
            json_bbox.setdefault('bbox', []).append(val)
        
        lista = []

        #create response dict
        json_response = {}
        for i in range(len(data)):

            #create lists
            list_ser = []
            list_user = []
            list_cat = []
            list_key = []

            #create lists
            repo_ser = Repositorie_Service.query.filter(Repositorie_Service.repo_id.in_([id_data[i]['repo_id']]))
            r_ser = ([e.serialize() for e in repo_ser])
          
            repo_usr = Repositorie_User.query.filter(Repositorie_User.repo_id.in_([id_data[i]['repo_id']]))
            r_user = ([e.serialize() for e in repo_usr])

            repo_cat = Repositorie_Categorie.query.filter(Repositorie_Categorie.repo_id.in_([id_data[i]['repo_id']]))
            r_cat = ([e.serialize() for e in repo_cat])

            repo_key = Repositorie_Keyword.query.filter(Repositorie_Keyword.repo_id.in_([id_data[i]['repo_id']]))
            r_key = ([e.serialize() for e in repo_key])

            for j in range(len(r_ser)):
                list_ser.append(r_ser[j]['service_id'])

            for k in range(len(r_user)):
                list_user.append(r_user[k]['user_id'])

            for l in range(len(r_cat)):
                list_cat.append(r_cat[l]['categorie_id'])

            for m in range(len(r_key)):
                list_key.append(r_key[m]['keyword_id'])
  
            #create keywords dict
            keywords=Keywords.query.filter(Keywords.keyword_id.in_(list_key))
            keyw = ([e.serialize() for e in keywords])
            json_keyword = {}
            for val in keyw: 
                json_keyword.setdefault('keywords', []).append(val['name'])
  
            #create categories dict
            categories=Categorie.query.filter(Categorie.categorie_id.in_(list_cat))
            cate = ([e.serialize() for e in categories])
            json_cate = {}
            for val in cate: 
                json_cate.setdefault('categories', []).append(val['name'])

            #create users dict
            users=User.query.filter(User.user_id.in_(list_user))
            members = ([make_public_user(e.serialize()) for e in users])
            json_users = {}
            for val in members: 
                json_users.setdefault('users', []).append(val)
            
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
            json_data['repositorie'][i].update(json_bbox['bbox'][i])
            json_data['repositorie'][i].update({"services": json_ser['services']})
            json_data['repositorie'][i].update({"users": json_users['users']})
            json_data['repositorie'][i].update({"categories": json_cate['categories']})
            json_data['repositorie'][i].update({"keywords": json_keyword['keywords']})
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

        #create lists
        list_ser = []
        list_user = []
        list_cat = []
        list_key = []

        #create lists 
        repo_ser = Repositorie_Service.query.filter(Repositorie_Service.repo_id.in_([repo_id]))
        r_ser = ([e.serialize() for e in repo_ser])
        
        repo_usr = Repositorie_User.query.filter(Repositorie_User.repo_id.in_([repo_id]))
        r_user = ([e.serialize() for e in repo_usr])

        repo_cat = Repositorie_Categorie.query.filter(Repositorie_Categorie.repo_id.in_([repo_id]))
        r_cat = ([e.serialize() for e in repo_cat])

        repo_key = Repositorie_Keyword.query.filter(Repositorie_Keyword.repo_id.in_([repo_id]))
        r_key = ([e.serialize() for e in repo_key])

        for j in range(len(r_ser)):
            list_ser.append(r_ser[j]['service_id'])

        for k in range(len(r_user)):
            list_user.append(r_user[k]['user_id'])

        for l in range(len(r_cat)):
            list_cat.append(r_cat[l]['categorie_id'])

        for m in range(len(r_key)):
            list_key.append(r_key[m]['keyword_id'])

        #create keywords dict
        keywords=Keywords.query.filter(Keywords.keyword_id.in_(list_key))
        keyw = ([e.serialize() for e in keywords])
        json_keyword = {}
        for val in keyw: 
            json_keyword.setdefault('keywords', []).append(val['name'])

        #create categories dict
        categories=Categorie.query.filter(Categorie.categorie_id.in_(list_cat))
        cate = ([e.serialize() for e in categories])
        json_cate = {}
        for val in cate: 
            json_cate.setdefault('categories', []).append(val['name'])

        #create users dict
        users=User.query.filter(User.user_id.in_(list_user))
        members = ([make_public_user(e.serialize()) for e in users])
        json_users = {}
        for val in members: 
            json_users.setdefault('users', []).append(val)
        
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
        json_data.update(json_bbox)
        json_data.update(json_ser)
        json_data.update(json_users)
        json_data.update(json_cate)
        json_data.update(json_keyword)
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