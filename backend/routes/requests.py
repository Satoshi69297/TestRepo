from flask import Blueprint, request
from models import QueuedRequest

requests_bp = Blueprint('requests', __name__)

@requests_bp.route('/', methods=['GET'])
def get_pending_requests():
    """Get all pending requests"""
    try:
        requests = QueuedRequest.query.filter_by(status='pending').all()
        return [req.to_dict(include_creator=True) for req in requests], 200
    except Exception as e:
        return {'error': str(e)}, 500

@requests_bp.route('/<int:request_id>', methods=['GET'])
def get_request(request_id):
    """Get request by ID"""
    try:
        queued_request = QueuedRequest.query.get(request_id)
        if not queued_request:
            return {'error': 'Request not found'}, 404
        return queued_request.to_dict(include_creator=True), 200
    except Exception as e:
        return {'error': str(e)}, 500
