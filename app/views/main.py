from app import app
from home import home_api
from login import login_api

app.register_blueprint(login_api)
app.register_blueprint(home_api)