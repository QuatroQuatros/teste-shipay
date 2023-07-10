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
def get_users():
    users = User.query.all()
    return jsonify([user.json() for user in users])

@user_bp.route('<int:id>/', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(user.json())

@user_bp.route('/', methods=['POST'])
# @swag_from('docs/post.yaml')
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
    

@user_bp.route('<int:id>/roles', methods=['GET'])
def get_role(id):
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
    return jsonify({'message': 'user not found'}), 400

@user_bp.route('/<int:id>/claims', methods=['GET'])
def get_claims(id):

    # Consulta utilizando Flask-SQLAlchemy
    results = db.session.query(User.name, User.email, Role.description.label("role"), Claim.description.label("claim")) \
        .join(Role, User.role_id == Role.id) \
        .join(UserClaim, User.id == UserClaim.user_id) \
        .join(Claim, Claim.id == UserClaim.claim_id) \
        .filter(User.id == id) \
        .all()

    # Exibir os resultados
    if results is None:
        return jsonify({'error': 'User not found'})

    # Retornar o resultado em formato JSON

    user_data = []

    for result in results:
        data = {
            'name': result.name,
            'email': result.email,
            'role': result.role,
            'claim': result.claim
        }
        user_data.append(data)
    return jsonify(user_data), 200