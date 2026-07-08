from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, QueuedRequest

admin_bp = Blueprint('admin', __name__)

def is_admin(user_id):
    """Check if user is admin"""
    user = User.query.get(user_id)
    return user and user.is_admin

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users"""
    try:
        current_user_id = get_jwt_identity()
        if not is_admin(current_user_id):
            return {'error': 'Admin access required'}, 403
        
        users = User.query.all()
        return [user.to_dict(include_email=True) for user in users], 200
    except Exception as e:
        return {'error': str(e)}, 500

@admin_bp.route('/requests', methods=['GET'])
@jwt_required()
def get_all_requests():
    """Get all queued requests"""
    try:
        current_user_id = get_jwt_identity()
        if not is_admin(current_user_id):
            return {'error': 'Admin access required'}, 403
        
        requests = QueuedRequest.query.all()
        return [req.to_dict(include_creator=True) for req in requests], 200
    except Exception as e:
        return {'error': str(e)}, 500

@admin_bp.route('/requests/<int:request_id>/approve', methods=['POST'])
@jwt_required()
def approve_request(request_id):
    """Approve a request"""
    try:
        current_user_id = get_jwt_identity()
        if not is_admin(current_user_id):
            return {'error': 'Admin access required'}, 403
        
        queued_request = QueuedRequest.query.get(request_id)
        if not queued_request:
            return {'error': 'Request not found'}, 404
        
        queued_request.status = 'approved'
        db.session.commit()
        
        return {'message': 'Request approved'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@admin_bp.route('/requests/<int:request_id>/reject', methods=['POST'])
@jwt_required()
def reject_request(request_id):
    """Reject a request"""
    try:
        current_user_id = get_jwt_identity()
        if not is_admin(current_user_id):
            return {'error': 'Admin access required'}, 403
        
        queued_request = QueuedRequest.query.get(request_id)
        if not queued_request:
            return {'error': 'Request not found'}, 404
        
        queued_request.status = 'rejected'
        db.session.commit()
        
        return {'message': 'Request rejected'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
