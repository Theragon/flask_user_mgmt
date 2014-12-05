# -*- coding: utf-8 -*-
"""
Flask-Login example
===================
This is a small application that provides a trivial demonstration of
Flask-Login, including remember me functionality.

:copyright: (C) 2011 by Matthew Frazier.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.login import (login_required, login_user, logout_user,
							confirm_login, fresh_login_required, current_user)

from flask import Blueprint

from app import app, lm
#from models import User
import usercontroller as usrcntrlr

login_api = Blueprint('login_api', __name__)

POST = 'POST'
GET = 'GET'
PUT = 'PUT'
DELETE = 'DELETE'


@lm.user_loader
def load_user(id):
	return usrcntrlr.get_user_by_id(id)


@login_api.route("/secret")
@fresh_login_required
def secret():
	return render_template("secret.html")


@login_api.route("/signin", methods=[GET, POST])
def signin():
	print('def signin')
	if request.method == POST:
		print('request is POST')
		success = False
		message = ''
		if "username" in request.form:
			username = request.form["username"]
			password = request.form["password"]
			print('username: ' + username)
			print('password: ' + password)
			user = usrcntrlr.get_user_by_name(username)
			if user is None:
				print('user is None')
				user = usrcntrlr.get_user_by_email(username)
			if user is None:
				message = 'Invalid username or email'
			if username == user.name:
				if user.check_password(password):
					print('password: ' + password)
					remember = request.form.get("remember")
					if login_user(user, remember=remember):
						print('remember: ' + str(remember))
						#print(dir(request))
						message = 'Logged in!'
						success = True
				else:
					message = 'Did you type your username and password correctly ?'
			else:
				message = 'Did you type your username and password correctly ?'
		else:
			message = 'Ivalid username or email'
		flash(message)
		if success:
			return redirect(request.args.get('next') or url_for('index'))
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

		if not usrcntrlr.username_exists(username):
			print(username + ' is available')
			if not usrcntrlr.email_exists(email):
				print(email + ' is not registered')
				success = usrcntrlr.create_user(username, email, password)
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
	users = usrcntrlr.get_all_users()
	return render_template('listusers.html', users=users)