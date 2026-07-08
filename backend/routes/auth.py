from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from models import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return {'error': 'Missing required fields'}, 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already registered'}, 409
        
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already taken'}, 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            profile=data.get('profile', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'User registered successfully'
        }, 201
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return {'error': 'Missing email or password'}, 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return {
            'token': access_token,
            'user': user.to_dict(include_email=True)
        }, 200
    
    except Exception as e:
        return {'error': str(e)}, 500
