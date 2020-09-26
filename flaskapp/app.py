import yaml
from flask import Flask, redirect, render_template, request
from flask_mysqldb import MySQL

"""
NOTE: Must 'pip install' following modules
pip install flask flask_mysqldb pyyaml

Created MySQL database through command line:
  $ mysql -u root -p
  CREATE DATABASE flaskapp;
  USE flaskapp;
  CREATE TABLE users (
      name varchar(20) NOT NULL, 
      email varchar(40) NOT NULL UNIQUE
  );
"""

# Create Flask instance 'app'
app = Flask(__name__)

# Configuration of database:
# YAML file contains information. NOTE: only for learning since passwords
#   cannot be placed into files.
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email))
            mysql.connection.commit()
            cur.close()
            return redirect('/users')
        except:
            print("Duplicate email address.")
    # File 'index.html' is located inside 'flaskapp/templates'
    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        # File 'users.html' located inside 'flaskapp/templates'
        return render_template('users.html', userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)

