from datetime import datetime
import os
import hashlib
import sqlalchemy as sa
from flask_login import UserMixin
from flask import current_app, url_for
from app import db
from user_policy import UserPolicy

# Таблица связи книг и категорий
book_category = db.Table('book_category',
                         db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete="CASCADE"), primary_key=True),
                         db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), primary key=True))

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    publication_year = db.Column(db.String(4), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    writer = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    total_ratings = db.Column(db.Integer, nullable=False, default=0)
    ratings_count = db.Column(db.Integer, nullable=False, default=0)
    cover_image = db.Column(db.String(100), db.ForeignKey('files.id'))

    categories = db.relationship('Category', secondary=book_category, backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return '<Book %r>' % self.title
    
    @property
    def rating(self):
        if self.ratings_count > 0:
            return self.total_ratings / self.ratings_count
        return 0

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary key=True, autoincrement=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.category_name

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.String(100), primary key=True)
    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    hash = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<File %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('serve_image', image_id=self.id)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))

    user = db.relationship('User', backref=db.backref('feedback', lazy='dynamic'))
    book = db.relationship('Book', backref=db.backref('feedback', lazy='dynamic'))

    def get_user(self):
        return db.session.query(User).filter_by(id=self.user_id).first().login

    def __repr__(self):
        return '<Feedback %r>' % self.comment

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary key=True, autoincrement=True)
    surname = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(32), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id', ondelete="CASCADE"))

    def set_password(self, password):
        self.password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.md5(password.encode('utf-8')).hexdigest()
    
    def is_admin(self):
        return self.role_id == current_app.config["ADMIN_ROLE_ID"]
    
    def is_moderator(self):
        return self.role_id == current_app.config["MODERATOR_ROLE_ID"]
    
    def can(self, action, record=None):
        policy = UserPolicy(record)
        method = getattr(policy, action, None)
        if method:
            return method()
        return False

    @property
    def full_name(self):
        return ' '.join([self.surname, self.given_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.username

class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary key=True, autoincrement=True)
    role_name = db.Column(db.String(100), nullable=False)
    role_description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<UserRole %r>' % self.role_name

class VersionControl(db.Model):
    __tablename__ = 'version_control'
    version = db.Column(db.String(32), primary key=True)
