from flask import render_template, url_for, flash, redirect, request
from Test import app, db, bcrypt
from Test.models import User
from flask_login import login_user, current_user, logout_user, login_required
from Test.forms import RegistrationForm, LoginForm, UpdateAccountForm
import secrets
import os
from PIL import Image

##################for email
import smtplib
from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import os
from werkzeug import secure_filename
#################

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if(form.validate_on_submit()):
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if(form.validate_on_submit()):
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'img/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)


##################################email
@app.route("/inbox")
def inbox():
    return render_template('inbox.html')

@app.route("/compose")
def compose():
    return render_template('compose.html')


"""def send_mail(recipient, subject, message):

    username = "logixpltd@gmail.com"
    password = "timebomb321"

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    print('sending mail to ' + recipient + ' on ' + subject)
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(username, recipient, msg.as_string())
    mailServer.close()"""

@app.route('/emailSent',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      #send_mail(result['to'],result['subject'],result['message'])
      #send_mail('sriharshav99@gmail.com','tokka','bokka')
      ##########email
      server = smtplib.SMTP('smtp.gmail.com', 587)

      server.starttls()

      #Next, log in to the server
      print("------------------------>"+current_user.email)
      print("------------------------>"+current_user.password)
      server.login(current_user.email, "Hacchi44/gmail")
      #Send the mail
      #############file handling
      if request.method == 'POST':
          f = request.files['file']
          f.save(secure_filename(f.filename))
#############file handling
#############message
      msg = MIMEMultipart()
      # storing the senders email address
      msg['From'] = current_user.email
      # storing the receivers email address
      msg['To'] = result['to']
      # storing the subject
      msg['Subject'] = result['subject']
      # string to store the body of the mail
      body = result['message']
      # attach the body with the msg instance
      msg.attach(MIMEText(body, 'plain'))
      # open the file to be sent
      filename = f.filename
      attachment = open(f.filename, "rb")
      # instance of MIMEBase and named as p
      p = MIMEBase('application', 'octet-stream')
      # To change the payload into encoded form
      p.set_payload((attachment).read())
      # encode into base64
      encoders.encode_base64(p)
      p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
      # attach the instance 'p' to instance 'msg'
      msg.attach(p)
      message=msg.as_string()
      #msg="Subject: "+result['subject']+"\n\n"+result['message']
#############message
      server.sendmail(current_user.email, result['to'], message)
      server.quit()
      #########email
      return "email sent"
##################################
