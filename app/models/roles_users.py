from app import db
#from user import User
from role import Role

roles_users = db.Table('roles_users', 
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))