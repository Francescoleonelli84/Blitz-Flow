from project import app
from project.models import *
from datetime import datetime
from functools import wraps
from flask import g, Flask, abort, render_template, request, redirect, session, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import email_validator
import sqlite3 



    
#from flask_marshmallow import Marshmallow
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)
login_manager.login_view = 'login'


# loads User_Class in the DB
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




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
@app.route('/profile', methods=["GET", "POST"])
@is_logged_in
def profile():
    form = ProfileForm()
    id = current_user.id
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
         name_to_update.name = request.form['username'] 
         name_to_update.sex = request.form['sex']
         name_to_update.age = request.form['age']
         name_to_update.country = request.form['country']
         name_to_update.company = request.form['company']
         name_to_update.position = request.form['position']

         #username_to_update.password = request.form['password']
         try:
                   db.session.commit()
                   flash("Profile Updated Successfully!")
                   return render_template('profile.html',form=form, username_to_update=name_to_update, id=id)
         except:
                   flash("Error! Looks like there was a problem...try again!")
                   return render_template('profile.html',form=form, name_to_update=name_to_update, id=id)

    else:
           #flash('Your profile is saved', 'success')
           return render_template('profile.html',form=form, name_to_update=name_to_update, id=id)  


#Logout-Route
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    #flash ('You have been logged out','success')
    return redirect(url_for('login'))


def get_db():
    DATABASE = './project/site.db'
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Dashboard      
@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard(): 
     cur = get_db().cursor()
     team_members = cur.execute("SELECT username FROM user").fetchall()
     tasks = db.session.query(Task).filter(Task.username==session.get('username'))
     
     to_do, doing, done = [],[],[]
     
     for task in tasks:
            if task.status == 'to_do':
                to_do.append(task)
                print("Now is in to do")
            elif task.status == 'doing':
                doing.append(task)
                print("Now is in doing")
            elif task.status == 'done':
                print("Now is in done")
                done.append(task)


     return render_template('dashboard.html', to_do=to_do, doing=doing, done=done, user=session.get('username'), team_members=team_members) 

@app.route('/add', methods=['POST'])
def add():
    selected_member = request.form.get('team_members_usernames')
    selected_task = request.form.get('task')  
    # Add new task
    # Need to be logged in to add task
    if not session.get('username'):
        abort(401)
    # If logged in, then add task to the database
    to_do = Task(
        username=session.get('username'),
        task=request.form['task'],
        status='to_do',
        team_member= request.form["team_members_usernames"]
    )
    #Add task to Task-Tabelle of the assigned Team-Member
    assigned = Task (
        username = selected_member,
        task = selected_task,
        status = 'to_do',
        team_member = session.get('username')
    )

    db.session.add(to_do)
    db.session.add(assigned)
    db.session.commit()
    return redirect(url_for('dashboard'))

#update status
@app.route('/task/<id>/<status>')
def change_status(id,status):
    # Change status of task
    # Need to be logged in to change the status of task
    selected_member = request.form.get('team_members_usernames')
    selected_task = request.form.get('task')  
    if not session.get('username'):
        abort(401)
    task = db.session.query(Task).filter(Task.id==int(id)).first()
    # If the task does not exist, abort
    if not task:
        abort(404)
    # Else, update the status
    task.status = status
    #assigned_updated = Task (
          #  username = task.team_member,
           # task = task.task,
            #status = task.status,
            #team_member = session.get('username')
        #)
    #db.session.add(assigned_updated)

    db.session.commit()  
    return redirect(url_for('dashboard'))

#delete status
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

@app.route('/create-comment/<task_id>', methods=[ 'POST'])
def create_comment(task_id):
    text = request.form.get('text')
    if not text:
        flash("Comment cannot be empty. ", category='error')
    else:
        task = Task.query.filter_by(id=task_id) 
        if task:
            comment= Comment(
                text=text, author=current_user.id, task_id=task_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Task does not exist ', category='error')
   
    return redirect(url_for('dashboard'))

