from flask import Flask, render_template, request, session, url_for, redirect
import os
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from md5 import md5
import db
from subprocess import Popen, list2cmdline
import re
import pandas as pd
import time




app = Flask(__name__, template_folder="./templates")

uploads_dir = os.path.join(app.instance_path, 'uploads')
app.secret_key = "283xzgt451sadf9823hgbn6913qdj12"

no_user_warning = "You have no user in the machine contact administration"

user_dic = {"username": None, "email": None}

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/file_up", methods = ['POST', 'GET'])
def get_file():
    #return render_template("upload.html")
    try:
        if request.method == "POST":
            
            if request.files["uploaded_file"] != None:
                
                user = session['uname']
                f = request.files["uploaded_file"]
                f.save( secure_filename(f.filename))
                passwd = ""
                with open("pass",'r') as p:
                    passwd = p.read()
                os.popen("sudo -S %s"%("mkdir /home/{}/uploads".format(user)), 'w').write(passwd)
                os.popen("sudo -S %s"%("mv \"{}\" /home/{}/uploads".format(secure_filename(f.filename), user)), 'w').write(passwd)
                
                return render_template("index.html",  name = user, correct2 = "File uploaded correctly" )
    except:
        return render_template("index.html", name = user,  correct2 = "File failed upload")
        
        
        
@app.route("/nbg", methods = ['POST'])
def nbgrader_ex():
    try:
        if request.method == "POST":
            
            if request.files["uploaded_file"] != None:
                
                user = session['uname']
                batch = db.get_batch(user)
                email = db.get_email(user)
                
                f = request.files["uploaded_file"]
                f.save( secure_filename(f.filename))
                passwd = ""
                with open("pass",'r') as p:
                    passwd = p.read()
                
                os.popen("sudo -S %s"%("mkdir /home/keystone/Autograding/{}/submitted/{}/{}".format(batch, email,secure_filename(f.filename)[:-6] )), 'w').write(passwd)
                os.popen("sudo -S %s"%("mv {} /home/keystone/Autograding/{}/submitted/{}/{}".format(f.filename,batch, email,secure_filename(f.filename)[:-6] )), 'w').write(passwd)
                time.sleep(2)
                if os.path.isfile("/home/keystone/Autograding/{}/submitted/{}/{}/{}".format(batch, email,secure_filename(f.filename)[:-6],secure_filename(f.filename) )):
                    
                    #os.popen("cd AI-Mar21 \n nbgrader autograde --student mardukenterprises@gmail.com --assignment py1  ")
                    #response = api.autograde("py1", "mardukenterprises@gmail.com", force=True, create=True)
                    #return response
                    #grade, max_score = get_grade(email, secure_filename(f.filename)[:-6], batch)
                    #response = send_json(email, secure_filename(f.filename)[:-6], max_score, grade)
                    
                    return render_template("index.html", name = user,  correct = "File uploaded successfully"  ) # "Your score: "+ str(grade/max_score*100)+'%'
                else:
                    return render_template("index.html", name = user,  correct = "File failed to upload")
                
    except:
        print("Something went wrong")

@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    session.pop("uname", None)
    session.pop("batch", None)
    session.pop("email", None)
    return render_template("login.html")
    
@app.route("/log", methods = ['POST', 'GET'])
def login():
    
    try:
        
        if request.method == "POST":
            user = request.form["uname"].lower()
            if db.get_sum(user) == md5(request.form["psw"]):
                
                session['uname'] = user
                session['email'] = db.get_email(user)
                
                passwd = ""
                with open("pass",'r') as p:
                    passwd = p.read()
                
                os.popen("cd /home/keystone/{} \n source /home/anaconda3/bin/activate \n jupyter-notebook --allow-root ".format(user))
                return render_template("index.html", name = user, correct = '' )
                
            else:
                return "Pass missmatch"
            
            
    except:
        return "Something went wrong"

 

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/sign", methods = ['POST', 'GET'])
def sign_in():
    
    try:
        
        if request.method == "POST":
            user = request.form["uname"].lower()
            assert request.form["psw"] == request.form["psw2"]
            email = request.form["email"].lower()
            DoB = request.form["age"]
            country = request.form["country"].lower()
            batch = request.form["batch"]
            gender = request.form["gender"]

            
            
            if db.add_user(user,request.form["psw"], email, DoB, country, batch, gender):
                session['uname'] = user
                session['email'] = email
                session['batch'] = batch
                
                passwd = ""
                with open("pass",'r') as p:
                    passwd = p.read()
                
                os.popen("sudo -S %s"%("mkdir /home/keystone/Autograding/{}/submitted/{}".format(batch, email )), 'w').write(passwd)
                #os.popen("cd /home/{} \n source /home/anaconda3/bin/activate \n jupyter-notebook --no-browser ".format(user))
                return render_template("index.html", name = session['uname'] )
            else:
                return "Some of the fields where not correct"
            
    except:
        return "Something went wrong"
    

@app.route("/launch_jupyter")
def launch_jupyter():
    
    if os.path.isdir("/home/keystone/{}".format(session['uname'])): 
        response = os.popen(" jupyter-notebook list").readlines()
        return "response"
        for i in range(1, len(response)):
            
            return re.findall('[a-z]+',str(response[i].split("/home/")[1].split("/")[0]))[0]
            if re.findall('[a-z]+',str(response[i].split("/home/")[1].split("/")[0]))[0] == re.findall('[a-z]+',str(session['uname']))[0]:
                return redirect("http://88.1.56.23:" + response[i].split(":")[2])
    else:
        return render_template("index.html", name = session['uname'],  correct = "", warning = no_user_warning )
        
if __name__ == "__main__":
    app.run("192.168.1.44")
    #app.run()


