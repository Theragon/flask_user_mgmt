# -*- coding: utf-8 -*-
"""
Flask-Login example
===================
This is a small application that provides a trivial demonstration of
Flask-Login, including remember me functionality.
"""
from flask import request, render_template, redirect, url_for, flash
from flask.ext.login import (login_required, login_user, logout_user,
							confirm_login, fresh_login_required, current_user)

from flask import Blueprint

from app import lm
#from .. import usercontroller as usr
from ..controllers import usercontroller as usr

login_api = Blueprint('login_api', __name__)

POST = 'POST'
GET = 'GET'
PUT = 'PUT'
DELETE = 'DELETE'


@lm.user_loader
def load_user(id):
	return usr.get_user_by_id(id)


@login_api.route("/secret")
@fresh_login_required
def secret():
	return render_template("secret.html")


@login_api.route("/signin", methods=[GET, POST])
def signin():
	if request.method == POST:
		success = False
		message = ''
		if "username" in request.form:
			username = request.form["username"]
			password = request.form["password"]
			print('username: ' + username)
			print('password: ' + password)
			user = usr.get_user_by_name_or_email(username)
			if user is None:
				message = 'Invalid username or email'
			if user is not None:
				if user.validate(username, password):
					print('password: ' + password)
					remember = request.form.get("remember")
					success = login_user(user, remember=remember)
					if success:
						print('remember: ' + str(remember))
						message = 'Logged in!'
					if not success:
						print('login_user returned: ' + str(success))
				else:
					message = 'Failed to validate user'
			else:
				message = 'Did you type your username and password correctly ?'
		else:
			message = 'Ivalid username or email'
		flash(message)
		if success:
			return redirect(request.args.get('next') or url_for('home_api.index'))
		if not success:
			return render_template('signin.html')
	else:
		return render_template("signin.html")


@login_api.route("/reauth", methods=[GET, POST])
@login_required
def reauth():
	if request.method == "POST":
		confirm_login()
		flash(u"Reauthenticated.")
		return redirect(request.args.get("next") or url_for("index"))
	return render_template("reauth.html")


@login_api.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logged out.")
	return redirect(url_for("index"))


@login_api.route('/signup', methods=[GET, POST])
def signup():
	if request.method == POST:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']

		print('signing up user ' + username + ' ' + email + ' ' + password)

		success = False
		message = ''

		if not usr.username_exists(username):
			print(username + ' is available')
			if not usr.email_exists(email):
				print(email + ' is not registered')
				success = usr.create_user(username, email, password)
				message = 'You have successfully signed up!'
				print(username + ' signed up')
				print('password: ' + password)
				print('email: ' + email)
				
			else:
				message = 'email already exists'
		else:
			message = 'username already exists'

		if success:
			return render_template('index.html')
		else:
			flash(message)
			return render_template('signin.html')

	else:
		return render_template('signup.html')


@login_api.route('/listusers')
def listusers():
	users = usr.get_all_users()
	return render_template('listusers.html', users=users)