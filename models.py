
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # TODO: ids should not iterate up by one, id only assigned after login, not registering
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    wishlist_items = db.relationship('WishlistItem', backref='user', lazy=True)

    def __repr__(self):
        return f'<User ({self.id}, {self.username}, {self.password})>'

class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    name = db.Column(db.String(200), nullable=False)
    image_link = db.Column(db.String(200))
    url = db.Column(db.String(200), nullable=False)
    checked_off = db.Column(db.Boolean, default=False) 
    notes = db.Column(db.String(400))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Item {self.id} - User {self.user_id}>'