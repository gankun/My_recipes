from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, abort
from wtforms import Form, BooleanField, TextField, TextAreaField, \
     PasswordField, validators, IntegerField,  SubmitField
from flask.ext.login import LoginManager, login_user, current_user,\
     logout_user, login_required, UserMixin

# Form for registering recipes
class InsertForm(Form):
    
    R_name = TextField('name', [validators.Length(min=1, max=35) ,
        validators.Required()])
    R_serve = TextField('servings', [
            validators.Required(),])    
    R_time = TextField('time', [
            validators.Required(),])    
    Procedure = TextAreaField()
    
# Form for logining in
class LoginForm(Form):
    
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Required(),
    ])
# Form for Registering
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

# Form for search forms
class SearchForm(Form):
    search = TextField('search', [validators.Required(), validators.Length(min=3)])

# user class
class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
 
    def is_active(self):
        return self.active
''' 
function to flash errors for a form. code borrowed from 
http://stackoverflow.com/questions/13585663/
flask-wtfform-flash-does-not-display-errors
'''
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')