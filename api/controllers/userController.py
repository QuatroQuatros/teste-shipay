from flask import Blueprint, request, jsonify
from flasgger import swag_from
from models.users import User
from models.roles import Role
from models.claims import Claim
from models.usersClaims import UserClaim
import utils
from db import db

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
@swag_from('../docs/users/get_users.yaml')
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.json() for user in users]})


@user_bp.route('<int:id>', methods=['GET'])
@swag_from('../docs/users/get_user.yaml')
def get_user(id):
    user = User.find_user(id)
    if user != None:
        return jsonify({'user': user.json()})
    return jsonify({'message': 'user not found'}), 404


@user_bp.route('/', methods=['POST'])
@swag_from('../docs/users/create_user.yaml')
def create_user():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    role_id = request.json.get('role_id')

    if not name:
        return jsonify({'error': 'Name are required'}), 400
    
    if not email:
        return jsonify({'error': 'Email are required'}), 400
    
    if not role_id:
        return jsonify({'error': 'Role are required'}), 400
    
    if not password or password == "":
        password = utils.generate_random_password()
        # password = utils.generate_password_hash(password_raw)
    try:
        user = User(name, email, utils.generate_password_hash(password), role_id)
        user.save_user()

        return jsonify({
            'message': 'User created',
            'user': user.json(),
            'password-generated': password
        
        }), 201
    
    except:
        return jsonify({'error': 'Error on create user'}), 500
    

@user_bp.route('<int:id>/', methods=['PUT'])
@swag_from('../docs/users/update_user.yaml')
def update_user(id):
    data = request.get_json()
    try:
        user = User.update_user(id, data)

        if user != None:
            return jsonify({
                'message': 'User updated',
                'user': user.json(),
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    
    except:
        return jsonify({'error': 'Error on update user'}), 500
    
@user_bp.route('<int:id>/', methods=['DELETE'])
@swag_from('../docs/users/delete_user.yaml')
def delete_user(id):
    try:
        user = User.delete_user(id)

        if user == None:
            return jsonify({
                'error': 'User not found',
            }), 404
 
        return jsonify({
            'message': 'User deleted',
        }), 200
        
    
    except:
        return jsonify({'error': 'Error on delete user'}), 500
    

@user_bp.route('<int:id>/roles', methods=['GET'])
@swag_from('../docs/users/get_user_roles.yaml')
def get_role(id):
    try:
        user = db.session.query(User.id, User.name, Role.description.label("role"))\
        .join(Role, User.role_id == Role.id)\
        .filter(User.id == id)\
        .first()

        if(user):
            data = {
                'user_id': user.id,
                'name': user.name,
                'role': user.role
            }
            return jsonify(data), 200
        return jsonify({'message': 'user not found'}), 404

    except:
        return jsonify({'error': 'Error on get user roles'}), 500
    
@user_bp.route('/<int:id>/claims', methods=['GET'])
@swag_from('../docs/users/get_user_claims.yaml')
def get_claims(id):

    try:
        # Consulta utilizando Flask-SQLAlchemy
        results = db.session.query(User.id, User.name, User.email, Role.description.label("role"), Claim.description.label("claim")) \
            .join(Role, User.role_id == Role.id) \
            .join(UserClaim, User.id == UserClaim.user_id) \
            .join(Claim, Claim.id == UserClaim.claim_id) \
            .filter(User.id == id) \
            .all()

        # Exibir os resultados
        if results is None or results == []:
            return jsonify({'error': 'User not found'}), 404

        # Retornar o resultado em formato JSON
        user_data = []

        for result in results:
            data = {
                'user_id': result.id,
                'name': result.name,
                'email': result.email,
                'role': result.role,
                'claim': result.claim
            }
            user_data.append(data)
        return jsonify(user_data), 200
    except:
        return jsonify({'error': 'Error on get user claims'}), 500