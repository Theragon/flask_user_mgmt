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
from models import User
import database as db

login_api = Blueprint('login_api', __name__)

POST = 'POST'
GET = 'GET'
PUT = 'PUT'
DELETE = 'DELETE'


@lm.user_loader
def load_user(id):
	user = User.query.get(int(id))
	return user


@login_api.route("/secret")
@fresh_login_required
def secret():
	return render_template("secret.html")


@login_api.route("/signin", methods=[GET, POST])
def signin():
	print('def signin')
	if request.method == "POST":
		print('request is POST')
		success = False
		message = ''
		if "username" in request.form:
			username = request.form["username"]
			password = request.form["password"]
			print('username: ' + username)
			print('password: ' + password)
			user = get_user_by_name(username)
			if user is None:
				print('user is None')
				user = get_user_by_email(username)
			if user is None:
				message = 'Invalid username or email'
			if username == user.name:
				if user.check_password(password):
					print('password: ' + password)
					#remember = request.form.get("remember", "no") == "yes"
					#if login_user(USER_NAMES[username], remember=remember):
					login_user(user)
					message = 'Logged in!'
					success = True
					flash("Logged in!")
					return redirect(request.args.get("next") or url_for("index"))
				else:
					message = 'Did you type your username and password correctly ?'
			else:
				message = 'Sorry, but you could not log in'
		else:
			message = 'Ivalid username or email'
			flash(u"Invalid username.")
		if success:
			flash(message)
			return redirect(request.args.get('next') or url_for('index'))
		if not success:
			flash(message)
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

		if not username_exists(username):
			print(username + ' is available')
			if not email_exists(email):
				print(email + ' is not registered')
				success = create_user(username, email, password)
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
	users = get_all_users()
	return render_template('listusers.html', users=users)


def get_all_users():
	users = User.query.all()
	return users


def get_user_by_name(username):
	print('getting user ' + username + ' by username')
	user = User.query.filter(User.name == username).first()
	return user


def get_user_by_email(email):
	print('getting user ' + email + ' by email')
	user = User.query.filter(User.email == email).first()
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