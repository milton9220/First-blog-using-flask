from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
import pymysql
pymysql.install_as_MySQLdb()

with open('templates/config.json','r') as c:
    params=json.load(c)['param']

local_server=True

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']  

db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True,nullable=False)
    phone = db.Column(db.String(120), unique=True,nullable=False)
    message = db.Column(db.String(80),nullable=False)
    date = db.Column(db.String(120),nullable=True)

@app.route('/')
def home():
    
    return render_template('index.html',pass_param=params)

@app.route('/about')
def about():
    return render_template('about.html',pass_param=params)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name=request.form.get('name') #fetch data from contact.html file
        email=request.form.get('email') #fetch data from contact.html file
        phone=request.form.get('phone') #fetch data from contact.html file
        message=request.form.get('msg')  #fetch data from contact.html file
        entry=Contacts(name=name,email=email,phone=phone,message=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + phone
                          )
        

    return render_template('contact.html',pass_param=params)

@app.route('/post')
def post():
    return render_template('post.html',pass_param=params)

app.run(debug=True)    