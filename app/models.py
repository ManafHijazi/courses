from flask_login import UserMixin
from app.extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    profile_picture = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)

from app.extensions import db
from datetime import datetime

from datetime import datetime
from app.extensions import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    video_url = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, nullable=False)
    languages = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)

    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    added_by_user = db.relationship('User', backref='courses', lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

