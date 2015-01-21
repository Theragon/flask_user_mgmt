#!/usr/bin/env python
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from roles_users import roles_users
from role import Role
#from user_roles import roles_users
from datetime import datetime

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120), unique=False)
	last_seen = db.Column(db.DateTime)
	created = db.Column(db.DateTime)
	active = db.Column(db.Boolean)
	roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

	def is_authenticated(self):
		return True

	def is_active(self):
		return self.active

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __init__(self, name=None, email=None, password=None):
		self.name = name
		self.email = email
		self.set_password(password)
		self.created = datetime.utcnow()
		self.last_seen = self.created
		self.active = True

	def update_last_seen(self):
		self.last_seen = datetime.utcnow()

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		if password == None:
			return False
		else:
			return check_password_hash(self.password, password)

	def check_username(self, username):
		if username == None:
			return False
		else:
			return self.name == username

	def validate(self, username, password):
		if username == None or password == None:
			return False
		else:
			return self.check_username(username) and self.check_password(password)

	def __repr__(self):
		return '<User %r>' % (self.name)