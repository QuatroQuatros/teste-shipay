from flask import Blueprint, request, jsonify
from models.users import User
from models.roles import Role
from db import db

role_bp = Blueprint('roles', __name__)

@role_bp.route('/', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.json() for role in roles])

@role_bp.route('<int:id>/', methods=['GET'])
def get_role(id):
    role = Role.query.filter_by(id=id).first()
    return jsonify(role.json())


@role_bp.route('/', methods=['POST'])
# @swag_from('docs/post.yaml')
def create_role():
    description = request.json.get('description')

    if not description:
        return jsonify({'error': 'Description are required'}), 400
    
    if type(description) != str:
        return jsonify({'error': 'Description must be a string'}), 400
    
    try:
        role = Role(description)
        role.save_user()

        return jsonify({
            'message': 'Role created',
            'user': role.json(),
        }), 201
    
    except:
        return jsonify({'error': 'Error on create role'}), 500


@role_bp.route('<int:id>/users', methods=['GET'])
def get_role(id):
    users = db.session.query(User.id, User.name, Role.description.label("role"))\
    .join(Role, User.role_id == Role.id)\
    .filter(Role.id == id)\
    .all()

    if(users):
        user_data = []
        for user in users:
            data = {
                'user_id': user.id,
                'name': user.name,
                'role': user.role
            }
            user_data.append(data)
        return jsonify(user_data), 200
    return jsonify({'message': 'user not found'}), 400

