from app import db
#from user import User
#from flask.ext.security import RoleMixin

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))