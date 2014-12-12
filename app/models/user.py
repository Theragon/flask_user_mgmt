#!/usr/bin/env python
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from app import db

class User(db.Model):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True)
	email = Column(String(120), unique=True)
	pw_hash = Column(String(120), unique=False)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __init__(self, name=None, email=None, password=None):
		self.name = name
		self.email = email
		self.set_password(password)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def __repr__(self):
		return '<User %r>' % (self.name)