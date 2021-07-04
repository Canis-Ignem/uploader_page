from flask import Flask, render_template, request, session, url_for, redirect
import os
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from md5 import md5
import db
from subprocess import Popen, list2cmdline
import re
import sqlite3 as sql
import pandas as pd
from post_data import send_json
import time
import subprocess
from nbgrader.apps import NbGraderAPI
from traitlets.config import Config

'''
config = Config()
config.CourseDirectory.course_id = "./AI_Mar21"
'''

api = NbGraderAPI(coursedir="./AI_Mar21")



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
                
                os.popen("sudo -S %s"%("mkdir ./{}/submitted/{}/{}".format(batch, email,secure_filename(f.filename)[:-6] )), 'w').write(passwd)
                os.popen("sudo -S %s"%("mv {} ./{}/submitted/{}/{}".format(f.filename,batch, email,secure_filename(f.filename)[:-6] )), 'w').write(passwd)
                time.sleep(2)
                if os.path.isfile("./{}/submitted/{}/{}/{}".format(batch, email,secure_filename(f.filename)[:-6],secure_filename(f.filename) )):
                    
                    
                    api.autograde("py1", "mardukenterprises@gmail.com", force=True, create=True)
                    
                    grade, max_score = get_grade(email, secure_filename(f.filename)[:-6], batch)
                    response = send_json(email, secure_filename(f.filename)[:-6], max_score, grade)
                    
                    return render_template("index.html", name = user,  correct = "Your score: "+ str(grade/max_score*100)+'%'  ) # "Your score: "+ str(grade/max_score*100)+'%'
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
                os.popen("cd /home/{} \n source /home/anaconda3/bin/activate \n jupyter-notebook --no-browser ".format(user))
                return render_template("index.html", name = user, correct = '' )
                
            else:
                return "Pass missmatch"
            
            
    except:
        return "Something went wrong"

@app.route("/get_grade")
def get_grade(email,ex,batch):
    
    try:
        con = sql.connect("./{}/gradebook.db".format(batch))
        
        q1 = "SELECT id FROM assignment where name ='{}'".format(ex)
        ass_id = pd.read_sql_query( q1 , con).values[0][0]
        
        q2 = "Select id from submitted_assignment where student_id = '{}' and assignment_id = '{}' ".format(email,ass_id)  
        nb_id = pd.read_sql_query( q2 , con).values[0][0]
        
        q3 = "Select id from submitted_notebook where assignment_id = '{}'".format(nb_id)
        nb_id = pd.read_sql_query( q3 , con).values[0][0]

        q4 = "Select auto_score,cell_id from grade where notebook_id = '{}'".format(nb_id)
        grades = pd.read_sql_query( q4 , con)
        
        cell_list = grades['cell_id'].values.tolist()
        as_str = ','.join("\'"+str(cell_list[i])+ "\'"  for i in range(len(cell_list)))
        q5 = "Select max_score from grade_cells where id IN ({})".format( as_str )
        max_score = pd.read_sql_query( q5 , con)
        #print(max_score['max_score'].sum())
       
        #report = " The student:  {} \n Assigment:   {} \n Total marks: {}/{}".format(email,ex,grades['auto_score'].sum(),max_score['max_score'].sum())
        #print(report)
        return grades['auto_score'].sum(), max_score['max_score'].sum()
    except:
        #print("No submission for that student")
        return 0, 1
    

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
                
                os.popen("sudo -S %s"%("mkdir ./{}/submitted/{}".format(batch, email )), 'w').write(passwd)
                #os.popen("cd /home/{} \n source /home/anaconda3/bin/activate \n jupyter-notebook --no-browser ".format(user))
                return render_template("index.html", name = session['uname'] )
            else:
                return "Some of the fields where not correct"
            
    except:
        return "Something went wrong"
    

@app.route("/launch_jupyter")
def launch_jupyter():
    if os.path.isdir("/home/{}".format(session['uname'])):
        
        response = os.popen("jupyter-notebook list").readlines()
        for i in range(1, len(response)):
            
            if re.findall('[a-z]+',str(response[i].split("/home/")[1]))[0] == re.findall('[a-z]+',str(session['uname']))[0]:
                return redirect("http://88.1.56.23:" + response[i].split(":")[2])
    else:
        return render_template("index.html", name = session['uname'],  correct = "", warning = no_user_warning )
        
if __name__ == "__main__":
    app.run("192.168.1.44")
    #app.run()


