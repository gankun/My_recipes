import os
import unicodedata, cgi
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, abort
from flaskext.mysql import MySQL
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask.ext.login import LoginManager, login_user, current_user,\
     logout_user, login_required, UserMixin

import MySQLdb

#import login.py
mysql = MySQL()
app = Flask(__name__)
app.config.from_object(__name__)

app.config['MYSQL_DATABASE_USER'] = 'Guest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'guest@Password'
app.config['MYSQL_DATABASE_DB'] = 'my_recipes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
mysql.init_app(app)

class LoginForm(Form):
    
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Required(),
    ])

# user class
class User(UserMixin):
    def __init__(self, db, id):
        self.db = db
        self.id = id

#--------------------------
# DATABASE CONNECT FUNCTIONS

def connect_db():
    """Connects to the specific database."""
    rv = mysql.connect()
    
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()



# -----------------------------------------
# LOGIN FUNCTIONS

# callback is used to reload user object from ID stored in session.
'''
@login_manager.user_loader
def load_user(userid):
    return User.get(userid)
'''

@app.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    cur = db.cursor()
    #Execute Query
    cur.execute("SELECT * FROM user WHERE email = teset@test1.com")    
    user = 5
    
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
                WHERE user_info.email = test@test1.com")  
    user_id = cursor.fetchone()
    # Check if any valid users.
    if user_id == 'none':
        return false
    return user_id
    
    '''
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.email.data,
                        form.password.data)
        db_session.add(user)
        login_user(user)
        flash('Thanks for Logging in')
        return redirect(url_for('login'))
    return render_template('login.html', title = 'Sign In', form = form)
'''
@app.route("/logi", methods=["GET", "POST"])
def logi():
    # check if user is already authenticated
    #if g.user is not None and g.user.is_authenticated():
     #   return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        # Function to authenticate the login.
        return try_login()
    return render_template('login.html',
                           title = 'Sign In', form = form)

@app.route('/test')
def test():
    if authenticate('test@test1.com', 'hi'):
        return 'yes'
    else:
        return 'no'

@app.route('/index')
@login_required
def show_entries():
    # connect to the database, if not connected
    db = get_db()
    cur = db.cursor()
    #Execute Query
    cur.execute("SELECT * FROM user")
    #entries = cur.fetchall()
    # go through username and recipes and print message.
    for user_name in cur:
        user = user_name[2]
 
        cur.execute("SELECT * FROM recipe")
        for food in cur:
            dish = food[1]
        
        return render_template("index.html", title = 'home', user = user, dish = dish)



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    login_manager = LoginManager()    
    login_manager.init_app(app)
    login_manager.login_view = '/login'

    app.run(debug=True)