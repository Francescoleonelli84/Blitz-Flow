from project import db
from datetime import datetime
from functools import wraps
from flask import g, Flask, abort, render_template, request, redirect, session, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, func
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import email_validator
import sqlite3 



# User_Class_Model for the Database
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
   # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

# Task_Class_Model for the database
class Task(db.Model):
    __tablename__ = 'tasks' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    task = db.Column(db.String, nullable=False)
    status = db.Column(Enum('to_do', 'doing', 'done'))
    team_member = db.Column(db.String,  db.ForeignKey('user.username'))
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    date = db.Column(db.String)


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

class Comment(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    text= db.Column(db.String(200), nullable=False)
    date_created= db.Column(db.DateTime(timezone=True), default= func.now())
    author= db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    task_id= db.Column(db.Integer, db.ForeignKey(
        'tasks.id', ondelete='CASCADE'), nullable=False)


