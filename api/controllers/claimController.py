from flask import Blueprint, request, jsonify
from flasgger import swag_from
from models.claims import Claim
from db import db

claim_bp = Blueprint('claim_bp', __name__)

@claim_bp.route('/', methods=['GET'])
@swag_from('../docs/claims/get_claims.yaml')
def get_claims():
    claims = Claim.query.all()
    return jsonify({'claims': [claim.json() for claim in claims]})


@claim_bp.route('<int:id>', methods=['GET'])
@swag_from('../docs/claims/get_claim.yaml')
def get_claim(id):
    claim = Claim.find_claim(id)
    if claim != None:
        return jsonify({'claim': claim.json()})
    return jsonify({'message': 'claim not found'}), 404


@claim_bp.route('/', methods=['POST'])
@swag_from('../docs/claims/create_claim.yaml')
def create_claim():
    description = request.json.get('description')
  
    if not description:
        return jsonify({'error': 'description are required'}), 400

    
    try:
        claim = Claim(description)
        claim.save_claim()

        return jsonify({
            'message': 'claim created',
            'claim': claim.json()
        }), 201
    
    except:
        return jsonify({'error': 'Error on create claim'}), 500
    

@claim_bp.route('<int:id>/', methods=['PUT'])
@swag_from('../docs/claims/update_claim.yaml')
def update_claim(id):
    data = request.get_json()
    try:
        claim = Claim.update_claim(id, data)

        if claim != None:
            return jsonify({
                'message': 'claim updated',
                'claim': claim.json(),
            }), 200
        else:
            return jsonify({'error': 'claim not found'}), 404
    
    except:
        return jsonify({'error': 'Error on update claim'}), 500
    
@claim_bp.route('<int:id>/', methods=['DELETE'])
@swag_from('../docs/claims/delete_claim.yaml')
def delete_claim(id):
    try:
        claim = Claim.delete_claim(id)

        if claim == None:
            return jsonify({
                'error': 'claim not found',
            }), 404
 
        return jsonify({
            'message': 'claim deleted',
        }), 200
        
    except:
        return jsonify({'error': 'Error on delete claim'}), 500
