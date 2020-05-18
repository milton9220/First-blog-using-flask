from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ict_learner'
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
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

    return render_template('contact.html')

@app.route('/post')
def post():
    return render_template('post.html')

app.run(debug=True)    