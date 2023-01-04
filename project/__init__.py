
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

#Debug Mode Activated
app.debug = True
#Configuration steps (lately they should be stored in a config file!)
app.config['SECRET_KEY'] = 'secretkey'
# !! Change here the directory to your project to create the database inside your project folder !!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/wyf6623/MyProject/Blitz_Flow_Project/project/site.db'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
db = SQLAlchemy(app)
#ma = Marshmallow(app)


from project import routes