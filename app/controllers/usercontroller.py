from ..models import User
from app import database as db


def get_user_by_id(id):
	user = User.query.get(int(id))
	return user

def get_user_by_name(name):
	print('getting user ' + name + ' by username')
	user = User.query.filter(User.name == name).first()
	return user

def get_user_by_email(email):
	print('getting user ' + email + ' by email')
	user = User.query.filter(User.email == email).first()
	return user

def get_user_by_name_or_email(name_or_email):
	if name_or_email != None:
		user = get_user_by_name(name_or_email)
	if user is None:
		user = get_user_by_email(name_or_email)
	return user

def username_exists(username):
	user = get_user_by_name(username)
	if user == None:
		return False
	else:
		return True

def email_exists(email):
	user = get_user_by_email(email)
	if user == None:
		return False
	else:
		return True

def create_user(username, email, password):
	print('creating new user: ' + username + ' ' + email + ' ' + password)
	user = User(username, email, password)
	return db.save(user)

def get_all_users():
	users = User.query.all()
	return users