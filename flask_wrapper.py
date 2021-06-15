from flask import Flask, render_template, request
import os


app = Flask(__name__, template_folder="./templates")

@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(host="192.168.1.33", port= 8080)
    

