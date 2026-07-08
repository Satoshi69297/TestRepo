from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, QueuedRequest
from datetime import datetime

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile"""
    try:
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(include_email=True), 200
    except Exception as e:
        return {'error': str(e)}, 500

@users_bp.route('/profile/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_profile(user_id):
    """Update user profile"""
    try:
        current_user_id = get_jwt_identity()
        
        if current_user_id != user_id:
            return {'error': 'Unauthorized'}, 403
        
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        data = request.get_json()
        
        if 'username' in data:
            # Check if username is already taken by another user
            existing = User.query.filter_by(username=data['username']).first()
            if existing and existing.id != user_id:
                return {'error': 'Username already taken'}, 409
            user.username = data['username']
        
        if 'email' in data:
            # Check if email is already taken by another user
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return {'error': 'Email already taken'}, 409
            user.email = data['email']
        
        if 'profile' in data:
            user.profile = data['profile']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return {'message': 'Profile updated successfully'}, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@users_bp.route('/requests', methods=['POST'])
@jwt_required()
def register_request():
    """Register a new queued request"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('title'):
            return {'error': 'Missing required fields'}, 400
        
        new_request = QueuedRequest(
            user_id=current_user_id,
            title=data['title'],
            description=data.get('description', ''),
            points_offered=data.get('points_offered', 0)
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        return {
            'id': new_request.id,
            'message': 'Request created successfully'
        }, 201
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@users_bp.route('/requests', methods=['GET'])
@jwt_required()
def get_user_requests():
    """Get user's registered requests"""
    try:
        current_user_id = get_jwt_identity()
        requests = QueuedRequest.query.filter_by(user_id=current_user_id).all()
        return [req.to_dict() for req in requests], 200
    except Exception as e:
        return {'error': str(e)}, 500

@users_bp.route('/assigned-requests', methods=['GET'])
@jwt_required()
def get_assigned_requests():
    """Get requests assigned to current user"""
    try:
        current_user_id = get_jwt_identity()
        requests = QueuedRequest.query.filter_by(assigned_to=current_user_id).all()
        return [req.to_dict(include_creator=True) for req in requests], 200
    except Exception as e:
        return {'error': str(e)}, 500

@users_bp.route('/requests/<int:request_id>/acquire', methods=['POST'])
@jwt_required()
def acquire_request(request_id):
    """Acquire (claim) a request"""
    try:
        current_user_id = get_jwt_identity()
        queued_request = QueuedRequest.query.get(request_id)
        
        if not queued_request:
            return {'error': 'Request not found'}, 404
        
        if queued_request.status != 'pending':
            return {'error': 'Request is not available'}, 400
        
        queued_request.assigned_to = current_user_id
        queued_request.status = 'assigned'
        db.session.commit()
        
        return {'message': 'Request acquired successfully'}, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@users_bp.route('/requests/<int:request_id>/complete', methods=['POST'])
@jwt_required()
def complete_request(request_id):
    """Complete a request"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        queued_request = QueuedRequest.query.get(request_id)
        
        if not queued_request:
            return {'error': 'Request not found'}, 404
        
        if queued_request.assigned_to != current_user_id:
            return {'error': 'Unauthorized'}, 403
        
        points_given = data.get('points_given', 0)
        
        # Update request
        queued_request.status = 'completed'
        queued_request.points_given = points_given
        queued_request.completed_at = datetime.utcnow()
        
        # Add points to user
        user = User.query.get(current_user_id)
        user.points += points_given
        
        db.session.commit()
        
        return {'message': 'Request completed successfully'}, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
