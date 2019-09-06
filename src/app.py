#!flask/bin/python
from flask_httpauth import HTTPBasicAuth
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import url_for
from flask import abort
auth = HTTPBasicAuth()

#app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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

#data
users = [
	{
			"user_id": 1,
			"name": "username_1",
			"image": "assets/images/img_avatar.png"
		}, {
			"user_id": 2,
			"name": "username_2",
			"image": "assets/images/img_avatar2.png"
		}
]

#data
repositories = [
    {

		"id": 1,
		"name": "LiSS",
		"abstract": "O Laboratório de Investigação Sistemas Socioambientais (LiSS) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. Ele tem como objeto estudar a influencia das atividade antrópicas nas mudanças de uso e cobertura da Terra. A principal área de estudo do LiSS é a Amazônia Legal, porém pesquisas também vem sendo feitas na região do Vale Paraibano (SP) e no bioma do Pantanal.",
		"maintainer": "username",
		"created_on": "2019-09-04T14:48:54+00:00",
		"language": "Português",
		"email": "email@email.com",
		"bbox": [
			[
				[-70.0588433406, -33.3848757513],
				[-35.2541558406, -33.3848757513],
				[-35.2541558406, 0.2315631899],
				[-70.0588433406, 0.2315631899],
				[-70.0588433406, -33.3848757513]
			]
		],
		"keywords": ["Sistemas Socioambientais", "Atividade Antrópicas", "Uso e Cobertura da Terra"],
		"categories": ["Uso e Cobertura da Terra"],
		"users": [{
			"user_id": 1,
			"name": "username_1",
			"image": "assets/images/img_avatar2.png"
		}, {
			"user_id": 2,
			"name": "username_2",
			"image": "assets/images/img_avatar.png"
		}],
		"services": [{
				"service_id": 1,
				"name": "PostgreSQL",
				"host": "137.012.125.01",
				"ports": [5432],
				"created_on": "2019-09-04T14:48:54+00:00"
			},
			{
				"service_id": 2,
				"name": "GeoServer",
				"host": "137.012.125.02",
				"ports": [5555, 5050],
				"created_on": "2019-09-04T14:48:54+00:00"
			},
			{
				"service_id": 3,
				"name": "GeoNetwork",
				"host": "137.012.125.03",
				"ports": [5000],
				"created_on": "2019-09-04T14:48:54+00:00"
			}
		],
		"custom_fields": [{}]
	},
	{
		"id": 2,
		"name": "LabISA",
		"abstract": "O Laboratório de Instrumentação de Sistemas Aquáticos (LabISA) é um dos laboratórios que compõe a Coordenação-Geral de Observação da Terra OBT-INPE. O laboratório foi motivado pelo aumento no número de estudos voltados à aplicações de sensoriamento remoto para estimativa de propriedades físicas, biológicas e químicas de águas continentais. A principal atividade do laboratório é coleta de dados sobre propriedades óticas e limnológicas de águas interiores e costeiras. A principal área de estudo do LabISA são sistemas de águas interiores de diferentes biomas do Brasil.",
		"maintainer": "username",
		"created_on": "2019-09-04T14:48:54+00:00",
		"language": "Português",
		"email": "email@email.com",
		"bbox": [
			[
				[-70.0588433406, -33.3848757513],
				[-35.2541558406, -33.3848757513],
				[-35.2541558406, 0.2315631899],
				[-70.0588433406, 0.2315631899],
				[-70.0588433406, -33.3848757513]
			]
		],
		"keywords": ["Sensoriamento Remoto", "Sistemas Aquáticos", "Águas Continentais"],
		"categories": ["Sensoriamento Remoto"],
		"users": [{
			"user_id": 1,
			"name": "username_1",
			"image": "assets/images/img_avatar.png"
		}, {
			"user_id": 2,
			"name": "username_2",
			"image": "assets/images/img_avatar2.png"
		}],
		"services": [{
				"service_id": 1,
				"name": "PostgreSQL",
				"host": "137.012.125.01",
				"ports": [5432],
				"created_on": "2019-09-04T14:48:54+00:00"
			},
			{
				"service_id": 2,
				"name": "GeoServer",
				"host": "137.012.125.02",
				"ports": [5555, 5050],
				"created_on": "2019-09-04T14:48:54+00:00"
			},
			{
				"service_id": 3,
				"name": "GeoNetwork",
				"host": "137.012.125.03",
				"ports": [5000],
				"created_on": "2019-09-04T14:48:54+00:00"
			}
		],
		"custom_fields": [{}]
	}
]

#uri repositories
def make_public_repositorie(repositorie):
    new_repositorie = {}
    for field in repositorie:
        if field == 'id':
            new_repositorie['uri'] = url_for('get_repositorie', repositorie_id=repositorie['id'], _external=True)
        else:
            new_repositorie[field] = repositorie[field]
    data = new_repositorie
    return {"name": data['name'], "users": [make_public_user(user) for user in data['users']], "abstract":data['abstract'], "categories": data['categories'], "uri": data['uri'], "maintainer": data['maintainer'], "created_on": data['created_on'], "language": data['language'], "email": data['email'], "bbox": data['bbox'], "keywords": data['keywords'], "services": data['services'], "custom_fields": data['custom_fields']}

#uri users
def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'user_id':
            new_user['uri'] = url_for('get_user', user_id=user['user_id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user

#get_users()
@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    return jsonify({'users': [make_public_user(user) for user in users] })

#get_user(user_id)
@app.route('/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['user_id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

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