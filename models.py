
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # TODO: ids should not iterate up by one, id only assigned after login, not registering
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    wishlist_items = db.relationship('WishlistItem', backref='user', lazy=True)
    friends = db.relationship('User', 
                              secondary='friendship',
                              primaryjoin='User.id == friendship.c.user_id',
                              secondaryjoin='User.id == friendship.c.friend_id',
                              backref='friend_of')

    def __repr__(self):
        return f'<User ({self.id}, {self.username}, {self.password})>'
    

friendship = db.Table('friendship',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    name = db.Column(db.String(200), nullable=False)
    image_link = db.Column(db.String(200))
    url = db.Column(db.String(200), nullable=False)
    checked_off = db.Column(db.Boolean, default=False) 
    notes = db.Column(db.String(400))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'image_link': self.image_link,
            'url': self.url,
            'checked_off': self.checked_off,
            'notes': self.notes
            # 'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<Item {self.id} - User {self.user_id}>'