
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config.from_object(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ultraman6'
app.config['MYSQL_DATABASE_DB'] = 'my_recipes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def hello_world():
    
     
    
    cursor = mysql.connect().cursor()
    
    query = ("SELECT * FROM USER")
     
    cursor.execute(query)
    entry = cursor.fetchall()
    i = 'zero'
    for (user_name) in cursor:
        i += "user_name"
        #return "tada"
     #   print user_name
        return render_template("index.html", title = 'home', user = user_name[2])
    
    cursor.close()
    cnx.close()   
def get_db():
    """Opens up a new dabase connection if there isn't one already"""
    if not hasattr(g, 'my_recipes'):
        g.my_recipes = connect_db()
        return g.my_recipes
def close_db(error):
    """Closes the database at end of request"""
    if hasattr(g,'my_recipes'):
        g.my_recipes.close()
def connect_db():
    """Connects to the specific database."""
    rv = mysql.connect()
    rv.row_factory = mysql.row
    return rv

@app.route('/index')
def index():
    user = {'nickname': 'Matt'}
    return render_template("index.html", title = 'home', user = user)

if __name__ == '__main__':
    app.run(debug=True)