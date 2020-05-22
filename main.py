from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
import pymysql
import os
from werkzeug.utils import secure_filename
pymysql.install_as_MySQLdb()

with open('templates/config.json','r') as c:
    params=json.load(c)['param']

local_server=True

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_URL']=params['upload_location']
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

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),nullable=True)
    slug = db.Column(db.String(120), unique=True,nullable=False)
    content = db.Column(db.String(120),nullable=True)
    image = db.Column(db.String(80),nullable=True)
    date = db.Column(db.String(20),nullable=True)    

@app.route('/')
def home():
    posts=Posts.query.filter_by().all()[0:params['num_of_post']]
    return render_template('index.html',pass_param=params,posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',pass_param=params)

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method=='POST':
        f=request.files['file']
        f.save(os.path.join(app.config['UPLOAD_URL'],secure_filename(f.filename)))
        return "Uploda successfully"

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if ('user' in session and session['user']==params['admin_name']):
        posts=Posts.query.all()
        return render_template('dashboard.html',pass_param=params,posts=posts)

    if request.method=='POST':
        user_name=request.form.get('user_name')
        password=request.form.get('password')
        if (user_name ==params['admin_name'] and password==params['password']):
            session['user']=user_name
            posts=Posts.query.all()
            return render_template('dashboard.html',pass_param=params,posts=posts)

    
    return render_template('login.html',pass_param=params) 
       
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

@app.route('/insert',methods=['GET','POST'])
def insert():
    if request.method=='POST':
        title=request.form.get('title') #fetch data from contact.html file
        slug=request.form.get('slug') #fetch data from contact.html file
        content=request.form.get('content') #fetch data from contact.html file
        image=request.form.get('image')  #fetch data from contact.html file
        entry=Posts(title=title,slug=slug,content=content,image=image,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
       
        

    return render_template('insert.html',pass_param=params)


@app.route('/edit/<string:id>',methods=['GET','POST'])
def edit(id):
    if request.method=='POST':
        post=Posts.query.filter_by(id=id).first()
        post.title=request.form.get('title')
        post.slug=request.form.get('slug')
        post.content=request.form.get('content')
        post.image=request.form.get('image')
        post.date=datetime.now()
        
        db.session.commit()
        return redirect('/dashboard')
    posts=Posts.query.filter_by(id=id).first()
    return render_template('edit.html',pass_param=params,posts=posts)    


@app.route('/post/<string:post_slug>',methods=['GET'])
def post(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',pass_param=params,post=post)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')

app.run(debug=True)    