from flask import Blueprint
from flask import render_template

home_api = Blueprint('home_api', __name__)

@home_api.route('/')
def index():
	return render_template('index.html')