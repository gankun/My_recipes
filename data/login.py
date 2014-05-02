import string
import random
from flask.ext.login import LoginManager, login_user, current_user,\
     logout_user, login_required, UserMixin
#from config import basedir
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.validators import Required
from flask import g, session, url_for, request, flash, redirect
#from models import User, ROLE_USER


login_manager = LoginManager()
login_manager.login_view = "login"

class LoginForm(Form):
    
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Required(),
    ])
class LoginForm2(Form):
    user_name = TextField('User Name', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

# callback is used to reload user object from ID stored in session.
@login_manager.user_loader
def load_user(userid):
    return User.get(userid)
    
# user class
class User(UserMixin):
    user_id = 1
    user_name = 2
    email = 2
    
def make_salt(num_chars):
    num_chars= min(20, num_chars)
    salt = ''
    keys = string.letters + string.digits + \
        '#$%&\()*+-./<=>?@[]^_{|}~'
    return ''.join(random.choice(keys) for _ in range(num_chars))

def authenticate(email, password):
    '''authenticates if a user's login request.
    it checks their username with the inputed password.
    If the password + salt doesn't match, then the function
    returns false. If the salted password matches the hash, return
    true'''
    db = get_db()
    cur = db.cursor()
    # Verify if a email belongs to a user, retrieve id.    
        #Execute Query
    cur.execute("SELECT user_id FROM user \
                WHERE user_info.email = ?", email)  
    user_id = cursor.fetchone()
    # Check if any valid users.
    if user_id == 'none':
        return false
    return user_id
    
@app.route("/login", methods=["GET", "POST"])
def login():
    # check if user is already authenticated
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        # Function to authenticate the login.
        return try_login()
    return render_template('login.html',
                           title = 'Sign In', form = form)
def try_login():
    # function to check the login info and act accordingly.
    login_user(user)
    flash("Logged in successfully")
    return redirect(url_for("index"))
   
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)

