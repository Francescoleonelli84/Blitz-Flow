from datetime import datetime
from flask import Flask, abort, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#Debug Mode Activated
app.debug = True
#Configuration steps (lately they should be stored in a config file!)
app.config['SECRET_KEY'] = 'secretkey'
# !! Change here the directory to your project to create the database inside your project folder !!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Flask_Projects/Blitz_Flow_Project/site.db'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)
login_manager.login_view = 'login'

# User_Class_Model for the Database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

# loads User_Class in the DB
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Login-Validation through Wtf_Forms
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

# Register-Validation through Register_Forms
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

#Decorator for "Home" (in this case "Register-Page")
@app.route('/')
def index():
    return render_template('index.html')
    
#Route to Register-Page
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        #return '<h1>New user has been created!</h1>'
        flash('You have successfully registered ! ')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


#Route to Login_Page after Registration-Auth
@app.route('/login', methods=["GET", "POST"])
def login():
     form = LoginForm()
     if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
     return render_template('login.html', form=form)


#Logout-Route(Still not functioning)
@app.route('/logout')
@login_required
def logout():
    #logout_user()
    return redirect(url_for('index.html'))

#It runs the app (Standard Syntax)
if __name__ == "__main__":
        app.run(debug=True)
        db.create_all()
        