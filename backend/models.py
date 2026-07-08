from app import db
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile = db.Column(db.Text, default='')
    points = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    registered_requests = db.relationship('QueuedRequest', foreign_keys='QueuedRequest.user_id', backref='creator')
    assigned_requests = db.relationship('QueuedRequest', foreign_keys='QueuedRequest.assigned_to', backref='assigned_user')
    
    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'profile': self.profile,
            'points': self.points,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }
        if include_email:
            data['email'] = self.email
        return data

class QueuedRequest(db.Model):
    __tablename__ = 'queued_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, assigned, completed, rejected
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    points_offered = db.Column(db.Integer, default=0)
    points_given = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self, include_creator=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'user_id': self.user_id,
            'assigned_to': self.assigned_to,
            'points_offered': self.points_offered,
            'points_given': self.points_given,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
        if include_creator and self.creator:
            data['creator'] = self.creator.to_dict()
        return data
