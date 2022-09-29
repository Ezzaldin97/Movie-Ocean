from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_ocean.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db=SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager=LoginManager(app)
login_manager.login_view="log_in_page"


from movie import routes