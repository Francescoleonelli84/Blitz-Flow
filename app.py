from datetime import datetime
from functools import wraps
from flask import Flask, abort, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#Debug Mode Activated
app.debug = True
#Configuration steps (lately they should be stored in a config file!)
app.config['SECRET_KEY'] = 'secretkey'
# !! Change here the directory to your project to create the database inside your project folder !!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/wyf6623/myproject/Blitz_Flow_Project/sql/test.db'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)
login_manager.login_view = 'login'

# User_Class_Model for the Database
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

# Task_Class_Model for the database
class Task(db.Model):
    """Task class
    Attributes:
        id (int): Unique id, primary key, auto increment.
        username (str): Foreign key referencing Users table.
        task (str): Details of the task.
        status (enum): Status of the task, with the following values
            - 'to_do'
            - 'doing'
            - 'done'
    """
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    task = db.Column(db.String, nullable=False)
    status = db.Column(Enum('to_do', 'doing', 'done'))

# Profile_Class_Model for the Database
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    name = db.Column(db.String(20), unique=True, nullable=False)
    country = db.Column(db.String(120), unique=False, nullable=False)
    company = db.Column(db.String(120), unique=False, nullable=False)
    position = db.Column(db.String(120), unique=False, nullable=False)
    sex = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)

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

# Profile through wtf_Forms
class ProfileForm(FlaskForm):
   # username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=15)])
    sex = StringField('sex', validators=[InputRequired(), Length(min=1, max=15)])
    age = IntegerField('age', validators=[InputRequired(), Length(min=2, max=3)])
    country = StringField('country', validators=[InputRequired(), Length(min=4, max=50)])
    company = StringField('company', validators=[InputRequired(), Length(min=4, max=100)])
    position = StringField('position', validators=[InputRequired(), Length(min=4, max=50)])

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
        flash('You have successfully registered!')
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
                #passed
                session['logged_in'] = True
                session['username']= form.username.data
                #flash('You are now logged in', 'success')                
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
     return render_template('login.html', form=form)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# edit the profile
@app.route('/profile')
@is_logged_in
def profile():

    #flash('Your profile is saved', 'success')
    return redirect(url_for('profile'))


#Logout-Route(Still not functioning)
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    #flash ('You have been logged out','success')
    return redirect(url_for('login'))

# Dashboard      
@app.route('/dashboard')
@is_logged_in
def dashboard(): 
     tasks = db.session.query(Task).filter(Task.username==session.get('username'))
     to_do, doing, done = [],[],[]
     for task in tasks:
            if task.status == 'to_do':
                to_do.append(task)
            elif task.status == 'doing':
                doing.append(task)
            elif task.status == 'done':
                done.append(task)

     return render_template('dashboard.html', to_do=to_do, doing=doing, done=done, user=session.get('username'))

@app.route('/add', methods=['POST'])
def add():
    # Add new task
    # Need to be logged in to add task
    if not session.get('username'):
        abort(401)
    # If logged in, then add task to the database
    to_do = Task(
        username=session.get('username'),
        task=request.form['task'],
        status='to_do'
    )
    db.session.add(to_do)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/task/<id>/<status>')
def change_status(id,status):
    # Change status of task
    # Need to be logged in to change the status of task
    if not session.get('username'):
        abort(401)
    task = db.session.query(Task).filter(Task.id==int(id)).first()
    # If the task does not exist, abort
    if not task:
        abort(404)
    # Else, update the status
    task.status = status
    db.session.commit()  
    return redirect(url_for('dashboard'))

@app.route('/task/<id>', methods=['GET', 'POST', 'DELETE'])
def delete(id):
    #Delete task
    # Need to be logged in to change the status of task
    if not session.get('username'):
        abort(401)
    task = db.session.query(Task).filter(Task.id==int(id)).first()
    # If the task does not exist, abort
    if not task:
        abort(404)
    # Else, delete the status from database
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

#It runs the app (Standard Syntax)
if __name__ == '__main__':
        app.run(debug=True)

# create user table before the first request
@app.before_first_request
def create_tables():
    db.create_all()
