from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from md5 import md5
import db

app = Flask(__name__, template_folder="./templates")

#UPLOAD_FOLDER = "/home/{}/Downloads"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
                f.save(f.filename)
                return render_template("index.html")
    except:
        print("Something went wrong")
        
@app.route("/log", methods = ['POST', 'GET'])
def validate():
    
    try:
        
        if request.method == "POST":
            return "test2"
            user = request.form["uname"]
            if db.get_sum(user) == md5(request.form["psw"]):
                return render_template("index.html")
            else:
                return "Pass missmatch"
            
            
    except:
        return "Something went wrong"
    

if __name__ == "__main__":
    app.run("192.168.1.33")
    #app.run()


