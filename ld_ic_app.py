from flask import Flask,render_template,request,redirect,session
from flask_session import Session
from database import DeepMindDB
from assests import langdetectmodel
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os
from werkzeug.utils import secure_filename
from assests import icmodel

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = 'static/images'
app.config['SECRET_KEY'] = 'supersecretkey'

dbo = DeepMindDB()

class UploadImage(FlaskForm):
    file = FileField("file")
    submit = SubmitField("upload a file")

Session(app)

@app.route("/")
def index():
    session['logged_in'] = 0
    if(session.get('logged_in') == 0):
        return render_template('login.html')
    else:
        return redirect("/profile")

@app.route("/register")
def register():
    if(session.get('logged_in')==0):
        return render_template("register.html")
    else:
        return redirect("/profile")

@app.route("/registration",methods=['post'])
def regisration():
    name = request.form.get("username")
    email = request.form.get("useremail")
    password = request.form.get("password")
    db_i_response = dbo.insert(name,email,password)
    if(db_i_response):
        return render_template("login.html",message = "Registration Successful.")
    else:
        return render_template("register.html",message="Email Already Exists.")

@app.route("/logging",methods=['post'])
def logging():
    email = request.form.get('useremail')
    password = request.form.get('password') 
    db_s_response = dbo.search(email,password)
    if(db_s_response):
        session["logged_in"] = db_s_response
        return redirect("/profile")
    else:
        return render_template("login.html",message="wrong email or wrong password")

@app.route("/profile")
def profile():
    if(session.get("logged_in")):
        return render_template("home.html")
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    return redirect('/')

@app.route("/text_upload")
def langdetect():
    if(session.get("logged_in")):
        return render_template("langdetect.html")
    else:
        return redirect("/")

@app.route("/langmodel",methods=['post'])
def langmodel():
    text = request.form.get('text')
    model = langdetectmodel.LanguageDetector()
    model_response = model.language_processor_model(text)
    return render_template("langdetect.html",result=model_response)

@app.route("/image_upload")
def imageclassifier():
    if(session.get("logged_in")):
        form = UploadImage()
        return render_template("imageclassifier.html",form=form)
    else:
        return redirect("/")

@app.route("/ic_model",methods=['post'])
def ic_model():
    form = UploadImage()
    img_data = form.file.data
    img_data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],secure_filename(img_data.filename)))
    dir_path = "D:\\DataScience\\Flask\\static\\images"
    img_path = os.listdir(dir_path)
    model = icmodel.ImageClassifier()
    model_response = model.image_classifier_model(dir_path, img_path)
    file_list = os.listdir(dir_path)
    for file in file_list:
        file_name = os.path.join(dir_path,file)
        os.remove(file_name)
    return render_template("imageclassifier.html",form =form ,result = model_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)