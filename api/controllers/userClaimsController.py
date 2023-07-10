from flask import Blueprint, request, jsonify
from flasgger import swag_from
from models.usersClaims import UserClaim
from db import db

userClaim_bp = Blueprint('useruserClaim_bp', __name__)

@userClaim_bp.route('/', methods=['GET'])
@swag_from('../docs/userClaims/get_userClaims.yaml')
def get_claims():
    claims = UserClaim.query.all()
    return jsonify({'user_claims': [claim.json() for claim in claims]})


@userClaim_bp.route('<int:id>', methods=['GET'])
@swag_from('../docs/userClaims/get_userClaim.yaml')
def get_claim(id):
    userClaim = UserClaim.find_userClaim(id)
    if userClaim != None:
        return jsonify({'user_claim': userClaim.json()})
    return jsonify({'message': 'user claim not found'}), 404


@userClaim_bp.route('/', methods=['POST'])
@swag_from('../docs/userClaims/create_userClaim.yaml')
def create_claim():
    try:
        user_id = request.json.get('user_id')
        claim_id = request.json.get('claim_id')

        if not user_id:
            return jsonify({'error': 'user_id are required'}), 400
        
        if type(user_id) != int:
            return jsonify({'error': 'user_id must be of type int'}), 400
    
        if not claim_id:
            return jsonify({'error': 'claim_id are required'}), 400

        if type(claim_id) != int:
            return jsonify({'error': 'claim_id must be of type int'}), 400

    
        userClaim = UserClaim(user_id, claim_id)
        userClaim.save_userClaim()

        return jsonify({
            'message': 'user claim created',
            'user_claim': userClaim.json()
        }), 201
    
    except:
        return jsonify({'error': 'Error on create user claim'}), 500
    

@userClaim_bp.route('<int:id>/', methods=['PUT'])
@swag_from('../docs/userClaims/update_userClaim.yaml')
def update_claim(id):
    data = request.get_json()
    try:
        userClaim = UserClaim.update_userClaim(id, data)

        if userClaim != None:
            return jsonify({
                'message': 'claim updated',
                'user_claim': userClaim.json(),
            }), 200
        else:
            return jsonify({'error': 'user_claim not found'}), 404
    
    except:
        return jsonify({'error': 'Error on update user claim'}), 500
    
@userClaim_bp.route('<int:id>/', methods=['DELETE'])
@swag_from('../docs/userClaims/delete_userClaim.yaml')
def delete_claim(id):
    try:
        userClaim = UserClaim.delete_userClaim(id)

        if userClaim == None:
            return jsonify({
                'error': 'user claim not found',
            }), 404
 
        return jsonify({
            'message': 'user claim deleted',
        }), 200
        
    except:
        return jsonify({'error': 'Error on delete user claim'}), 500
