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

#uri repositories
def make_public_repositorie(repositorie):
    new_repositorie = {}
    for field in repositorie:
        if field == 'id':
            new_repositorie['uri'] = url_for('get_repositorie', repositorie_id=repositorie['id'], _external=True)
        else:
            new_repositorie[field] = repositorie[field]
    data = new_repositorie
    return {"name": data['name'], "users": [make_public_user(user) for user in data['users']], "abstract":data['abstract'], "categories": data['categories'], "uri": data['uri'], "maintainer": data['maintainer'], "created_on": data['created_on'], "language": data['language'], "email": data['email'], "bbox": data['bbox'], "start_date": data['start_date'], "end_data": data['end_data'], "keywords": data['keywords'], "services": data['services'], "custom_fields": data['custom_fields']}

#uri users
def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'user_id':
            new_user['uri'] = url_for('get_user', user_id=user['user_id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user

#create_user()
@app.route('/api/v1.0/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' and 'password' and 'image' in request.json:
        abort(400)
    username=request.args.get('username')
    full_name=request.args.get('full_name')
    password=request.args.get('password')
    email=request.args.get('email')
    image=request.args.get('image')
    created_on=request.args.get('created_on')
    last_login=request.args.get('last_login')
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
        return "User added. user id={}".format(user.user_id)
    except Exception as e:
        return(str(e))

#get_users()
@app.route("/api/v1.0/users")
def get_users():
    try:
        users=User.query.all()
        return jsonify([make_public_user(e.serialize()) for e in users])

    except Exception as e:
	    return(str(e))
		
#get_user(user_id)
@app.route("/api/v1.0/users/<int:user_id>")
def get_user(user_id):
    try:
        user=User.query.filter_by(user_id=user_id).first()
        return jsonify(user.serialize())
    except Exception as e:
	    return(str(e))











#get_repositories()
@app.route('/api/v1.0/repositories', methods=['GET'])
def get_repositories():
    data = {'repositories': [make_public_repositorie(repositorie) for repositorie in repositories] }
    return jsonify(data)

#get_repositorie(repositorie_id)
@app.route('/api/v1.0/repositories/<int:repositorie_id>', methods=['GET'])
def get_repositorie(repositorie_id):
    repositorie = [repositorie for repositorie in repositories if repositorie['id'] == repositorie_id]
    if len(repositorie) == 0:
        abort(404)
    return jsonify({'repositorie': make_public_repositorie(repositorie[0])})

#create_repositorie()
@app.route('/api/v1.0/repositories', methods=['POST'])
@auth.login_required
def create_repositorie():
    if not request.json or not 'name' and 'users' and 'abstract' in request.json:
        abort(400)
    repositorie = {
        "id": repositories[-1]['id'] + 1,
		"name": request.json['name'],
		"users": request.json['users'],
		"abstract": request.json['abstract'],
		"categories": request.json['categories'],
		"maintainer": request.json['maintainer'],
		"created_on": request.json['created_on'],
		"language": request.json['language'],
		"email":request.json['email'],
		"bbox": request.json['bbox'],
		"keywords": request.json['keywords'],
		"services": request.json['services'],
		"custom_fields": request.json['custom_fields']
    }
    repositories.append(repositorie)
    return jsonify({'repositorie': repositorie}), 201

#update_repositorie(repositorie_id)
@app.route('/api/v1.0/repositories/<int:repositorie_id>', methods=['PUT'])
@auth.login_required
def update_repositorie(repositorie_id):
    repositorie = [repositorie for repositorie in repositories if repositorie['id'] == repositorie_id]
    if len(repositorie) == 0:
        abort(404)
    if not request.json:
        abort(400)
    #if 'name' in request.json and type(request.json['name']) != unicode:
    #    abort(400)
    #if 'users' in request.json and type(request.json['users']) != unicode:
    #    abort(400)
    #if 'abstract' in request.json and type(request.json['abstract']) != unicode:
    #    abort(400)
    repositorie[0]['name'] = request.json.get('name', repositorie[0]['name'])
    repositorie[0]['users'] = request.json.get('users', repositorie[0]['users'])
    repositorie[0]['abstract'] = request.json.get('abstract', repositorie[0]['abstract'])
    return jsonify({'repositorie': repositorie[0]})

#delete_repositorie(repositorie_id)    
@app.route('/api/v1.0/repositories/<int:repositorie_id>', methods=['DELETE'])
@auth.login_required
def delete_repositorie(repositorie_id):
    repositorie = [repositorie for repositorie in repositories if repositorie['id'] == repositorie_id]
    if len(repositorie) == 0:
        abort(404)
    repositories.remove(repositorie[0])
    return jsonify({'result': True})

#app
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)