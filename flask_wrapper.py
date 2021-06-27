from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
from md5 import md5
import db
import sqlite3
app = Flask(__name__, template_folder="./templates")

uploads_dir = os.path.join(app.instance_path, 'uploads')


user_dic = {"username": None, "email": None}

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/flask", methods = ['POST', 'GET'])
def get_file():
    #return render_template("upload.html")
    try:
        if request.method == "POST":
            
            if request.files["uploaded_file"] != None:
                
                user = session["user"].lower()
                f = request.files["uploaded_file"]
                f.save( secure_filename(f.filename))
                passwd = ""
                with open("pass",'r') as p:
                    passwd = p.read()
                os.popen("sudo -S %s"%("mkdir /home/{}/uploads".format(user)), 'w').write(passwd)
                os.popen("sudo -S %s"%("mv {} /home/{}/uploads".format(f.filename, user)), 'w').write(passwd)
                
                return render_template("index.html",  name = user)
    except:
        print("Something went wrong")
        
@app.route("/log", methods = ['POST', 'GET'])
def login():
    
    try:
        
        if request.method == "POST":
            user = request.form["uname"].lower()
            passwd = md5(request.form["psw"])
        
            if db.get_sum(user) == passwd:
                passwd

            if db.get_sum(user) == md5(request.form["psw"]):
                
                session["uname"] = user
                return render_template("index.html", name = session['uname'] )
            else:
                db.get_sum(user)
                return "Pass missmatch"
            
            
    except:
        return "Something went wrong"
    
    
@app.route("/sign", methods = ['POST', 'GET'])
def sign_in():
    
    try:
        
        if request.method == "POST":
            user = request.form["uname"].lower()
            assert request.form["psw"] == request.form["psw2"]

            db.add_user(user,request.form["psw2"])
            return render_template("index.html", name = user)
            
    except:
        return "Something went wrong"
    

if __name__ == "__main__":
    app.run("192.168.1.44")
    #app.run()


