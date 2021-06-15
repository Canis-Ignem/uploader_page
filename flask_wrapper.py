from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename



app = Flask(__name__, template_folder="./templates")

UPLOAD_FOLDER = "~/Downloads/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods = ['GET', 'POST'])
def get_file():
    try:
        if request.method == "POST":
            if request.files["uploaded_file"] != None:
                f = request.files["uploaded_file"]
                f.save(secure_filename(f.filename))
                return "ALL OKEY"
    except:
        print("Something went wrong")

if __name__ == "__main__":
    app.run(host="192.168.1.33", port= 8080)


