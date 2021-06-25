from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from md5 import md5
import db
import sqlite3
app = Flask(__name__, template_folder="./templates")

uploads_dir = os.path.join(app.instance_path, 'uploads')
#os.popen("sudo -S %s"%("mkdir {}".format(uploads_dir)), 'w').write('Estocolmo597B')
os.popen("sudo -S %s"%("mkdir /home/keystone/testing"), 'w').write('Estocolmo597B')
LOGGED_USER = ""

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/flask", methods = ['POST', 'GET'])
def get_file():
    #return render_template("upload.html")
    try:
        if request.method == "POST":
            
            if request.files["uploaded_file"] != None:
                
                #user = request.form["user"]
                f = request.files["uploaded_file"]
                return os.path.join("/home/{}/".format(LOGGED_USER), secure_filename(f.name))
                f.save(os.path.join("/home/{}/".format(LOGGED_USER), secure_filename(f.name)))
                return "a"
                return render_template("index.html")
    except:
        print("Something went wrong")
        
@app.route("/log", methods = ['POST', 'GET'])
def validate():
    
    try:
        
        if request.method == "POST":
            user = request.form["uname"]
            passwd = md5(request.form["psw"])
        
            if db.get_sum(user) == passwd:
                passwd

            if db.get_sum(user) == md5(request.form["psw"]):
                
                LOGGED_USER = user
                return render_template("index.html")
            else:
                db.get_sum(user)
                return "Pass missmatch"
            
            
    except:
        return "Something went wrong"
    
    
@app.route("/sign", methods = ['POST', 'GET'])
def sign_in():
    
    try:
        
        if request.method == "POST":
            user = request.form["uname"]
            assert request.form["psw"] == request.form["psw2"]

            db.add_user(user,request.form["psw2"])
            LOGGED_USER = user
            return render_template("index.html")
            
    except:
        return "Something went wrong"
    

if __name__ == "__main__":
    app.run("192.168.1.44")
    #app.run()


