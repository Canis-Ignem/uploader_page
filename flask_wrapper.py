from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename



app = Flask(__name__, template_folder="./")

#UPLOAD_FOLDER = "/home/{}/Downloads"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run("192.168.1.33")


