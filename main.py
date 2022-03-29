from pickle import FALSE
from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for, session, logging, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt 
from flask_bootstrap import Bootstrap
from os import path


#1. Create a flask app which connects to MongoDB
app = Flask(__name__)
db = app.config["MONGO_URI"] = "mongodb://localhost:27017/wad"
app.config['SECRET_KEY']='thisisansecretkey'
mongo = PyMongo(app)
auth = HTTPBasicAuth()
bootstrap = Bootstrap(app)

#--------------- FOR FILE UPLOAD -------------------------------------------------------#
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#------------------------------AUTHENTICATION------------------------------------------#

@app.route("/") 
def default():
    return redirect(url_for('index'))


@app.route("/auth",methods=["GET", "POST"])
#@auth.login_required
def index():
    if request.method == "GET":
        return render_template("login.html", username="", password="")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        print(username)
        print(password)
        if mongo.db.users.find_one({"username": username, "password": password}):
            return redirect(url_for('secret'))
        else:
            flash('This user is not registered yet. Please register the User first!', 'warning')
            
            return render_template("failed.html")


@app.route("/secret", methods=['GET', 'POST'])
def secret():
    return render_template("secret.html")


#-------------------------------SIGNUP----------------------------------------------------------#

     
@app.route("/signup",methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if mongo.db.users.find_one({"username": username}):
            flash('Please choose another Username, this one is already taken!', 'warning')
            return render_template("signup.html")
        else:
            mongo.db.users.insert_one({
            'username': username,
            'password': password
            })
            flash('Registration was successfull! You can now log in!', 'success')
            return redirect(url_for('index'))

#--------------------------IMAGE UPLOAD---------------------------------------------------------#
def accepted_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload",methods=["GET", "POST"])
def upload_file():

    if request.method == "GET":
        return render_template('upload.html')
    else:

        if request.method == "POST":
           if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        if not accepted_file(file.filename):
            flash('Invalid file extension', 'danger')
            return redirect(request.url)
            
        if file and accepted_file(file.filename):


            file = request.files['file']
            file.save(app.config['UPLOAD_FOLDER'] + file.filename)
            fn = file.filename
            return redirect(url_for('uploaded_file', filename=fn))

    return render_template("upload.html")


        
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#1.Runs at ‘http://localhost:5000’
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)