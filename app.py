from pip._internal import main as pipmain

pipmain(['install', 'werkzeug.utils'])

from flask import Flask, request, g, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import hashlib
import os, sys
from datetime import timedelta

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.sqlite3'
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/webapp/userInfo'
app.secret_key = 'asdasdasdasdasdasdasdasdasdasdasdasdasd'
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)
#database for users and their info
class login(db.Model):
    __table_args__ = {'extend_existing': True}
    _id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    uname = db.Column(db.String(100))
    password = db.Column(db.String(256))
    def __init__(self, fname, lname, email, uname, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.uname = uname
        self.password = password

#starting of login page. Determine if user has correct login and password
@app.route('/', methods = ['POST','GET'])
def startingPage():
    if(request.method == 'POST'):
        userName = request.form.get('username')
        password = str(request.form.get('password'))
        encPass = hashlib.sha256(password.encode()).hexdigest()
        valid = login.query.filter_by(uname=userName, password=encPass).first()
        if valid:
            session['uname'] = valid.uname
            session['fname'] = valid.fname
            session['lname'] = valid.lname
            session['email'] = valid.email
            return redirect("/dashboard")
        else:
            flash('Login failed')

    return render_template("login.html")

#create account post request for new sers
@app.route('/createaccount', methods = ['POST', 'GET'])
def createAccountPage():
    if(request.method == 'POST'):
        session.permanent = True
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        email = request.form.get('email')
        userName = request.form.get('username')
        password = str(request.form.get('password'))
        encPass = hashlib.sha256(password.encode()).hexdigest()
        newUser = login(firstName, lastName, email, userName, encPass)

        db.session.add(newUser)
        db.session.commit()
        return redirect("/")

    return render_template("createaccount.html")

@app.route('/dashboard', methods = ['POST', 'GET'])
def displayDashboard():
	if(request.method == 'POST'):
		return
	
	return render_template("dashboard.html", data=null)

	
@app.route('/getHouseHolds')
def v_timestamp():
	#
    return render_template("dashboard.html", data=data)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)