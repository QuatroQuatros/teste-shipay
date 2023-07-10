from flask import Blueprint, request, jsonify
from flasgger import swag_from
from models.users import User
from models.roles import Role
from db import db

role_bp = Blueprint('roles', __name__)

@role_bp.route('/', methods=['GET'])
@swag_from('../docs/roles/get_roles.yaml')
def get_roles():
    try:
        roles = Role.query.all()
        return jsonify({'roles': [role.json() for role in roles]}), 200
    except:
        return jsonify({'message': 'error on get roles'}), 500

@role_bp.route('<int:id>', methods=['GET'])
@swag_from('../docs/roles/get_role.yaml')
def get_role(id):
    try:
        role = Role.query.filter_by(id=id).first()
        if role != None:
            return jsonify({'role': role.json()})
        return jsonify({'error': 'role not found'}), 404
    except:
        return jsonify({'message': 'error on get roles'}), 500
    


@role_bp.route('/', methods=['POST'])
@swag_from('../docs/roles/create_role.yaml')
def create_role():
    try:
        description = request.json.get('description')

        if not description:
            return jsonify({'error': 'Description are required'}), 400
        
        if type(description) != str:
            return jsonify({'error': 'Description must be a string'}), 400
        
        role = Role(description)
        role.save_role()

        return jsonify({
            'message': 'Role created',
            'role': role.json(),
        }), 201
    
    except:
        return jsonify({'error': 'Error on create role'}), 500
    
@role_bp.route('<int:id>/', methods=['PUT'])
@swag_from('../docs/roles/update_role.yaml')
def update_role(id):
    data = request.get_json()
    try:
        role = Role.update_role(id, data)

        if role != None:
            return jsonify({
                'message': 'role updated',
                'role': role.json(),
            }), 200
        else:
            return jsonify({'error': 'role not found'}), 404
    
    except:
        return jsonify({'error': 'Error on update role'}), 500


@role_bp.route('<int:id>/', methods=['DELETE'])
@swag_from('../docs/roles/delete_role.yaml')
def delete_role(id):
    try:
        role = Role.delete_role(id)

        if role == None:
            return jsonify({
                'error': 'role not found',
            }), 404
 
        return jsonify({
            'message': 'role deleted',
        }), 200
        
    except:
        return jsonify({'error': 'Error on delete role'}), 500

@role_bp.route('<int:id>/users', methods=['GET'])
@swag_from('../docs/roles/get_users_by_role.yaml')
def get_users_by_role(id):
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
    return jsonify({'message': 'role not found'}), 400

