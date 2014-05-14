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

#set up login manager
login_manager = LoginManager() 

app = Flask(__name__)
app.config.from_object(__name__)

app.config['MYSQL_DATABASE_USER'] = 'Guest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'guest@Password'
app.config['MYSQL_DATABASE_DB'] = 'my_recipes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
mysql.init_app(app)

# Form for loging in
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

# user class
class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
 
    def is_active(self):
        return self.active

USERS = {
    1: User(u"Matt", 1),
    2: User(u"Steve", 2),
    3: User(u"Creeper", 3, False),
    }
USER_NAMES = dict((u.name, u) for u in USERS.itervalues())
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


@app.before_request
def before_request():
    """Will be executed before each request."""
    g.user = current_user
    
# callback is used to reload user object from ID stored in session.
@login_manager.user_loader
def user_loader(id):
    ''' Uses the get function to find a user for a given user_id '''
    print "UserLaodere"
    return User('Matt', 1)
    return USERS.get(int(id)) 
#User.get(userid)

'''
Function to login the user. Users will be sent back to this page if not
logged in. Request using the form the email and password. 
'''
@app.route('/login', methods=['GET', 'POST'])
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        '''Check if the input is in our list of valid users.'''
        if username in USER_NAMES:
            #remember = request.form.get("remember", "no") == "yes"
            '''login the user.'''
            user = User(username, USER_NAMES[username])
            login_user(user, remember=False)
            flash("Logged in!")
            return redirect(request.args.get("next") or url_for("cook"))
            #else:       
             #   flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html",form=form)

@app.route("/logout", methods=["GET"])
#@login_required
def logout():
    '''Log out the current user.'''
    user = current_user
    user.authenticated = False
    logout_user()
    return "LOGGED OUT"
  
@app.route("/logout2/")
def logout_page():
    """
    Web Page to Logout User, then Redirect them to Index Page.
    """
    logout_user()
    return redirect("/")  

'''authenticates if a user's login request.
it checks their username with the inputed password.
If the password + salt doesn't match, then the function
returns false. If the salted password matches the hash, return
true'''    
def authenticate(email, password):

    db = get_db()
    cur = db.cursor()
    # Verify if a email belongs to a user, retrieve id.    
        #Execute Query
    cur.execute("SELECT user_id FROM user \
                WHERE user_info.i = test@test1.com")  
    user_id = cursor.fetchone()
    # Check if any valid users.
    if user_id == 'none':
        return false
    return user_id
    


'''
Function to register a user. User is sent here fom login screen and can enter 
in username, email, and password data.
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/test')
def test():
    if authenticate('test@test1.com', 'hi'):
        return 'yes'
    else:
        return 'no'

@app.route('/')

def home():
    return render_template("home.html")


@app.route('/index')
@login_required
def index():
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
        
        return render_template("index.html", title = 'home', user = 'Matt', dish = dish)


@app.route('/cook')
#@login_required
def cook():
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
            prep = food[2]
            serve = food[3]
            proc = food[4]
            return render_template("recipe.html", title = 'home', user = user, dish = dish,\
                               prep = prep, serve = serve, proc = proc)



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    
    login_manager.init_app(app)
    login_manager.login_view = '/login'

    app.run(debug=True)