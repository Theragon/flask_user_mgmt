from app import app
from home import home_api
from login import login_api
#from flask import render_template


app.register_blueprint(login_api)
app.register_blueprint(home_api)


#@app.route('/')
#def index():
	#return render_template('index.html')