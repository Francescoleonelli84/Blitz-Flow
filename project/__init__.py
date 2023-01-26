
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow

app = Flask(__name__)

#Debug Mode Activated
app.debug = True
#Configuration steps (lately they should be stored in a config file!)
app.config['SECRET_KEY'] = 'secretkey'
# !! Change here the directory to your project to create the database inside your project folder !!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Pfad/zum/Projekt/site.db'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)
login_manager.login_view = 'login'


from project import routes