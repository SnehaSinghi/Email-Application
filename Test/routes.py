from flask import render_template, url_for, flash, redirect, request, Flask
from Test import app, db, bcrypt
from Test.models import User
from flask_login import login_user, current_user, logout_user, login_required
from Test.forms import RegistrationForm, LoginForm, UpdateAccountForm
import secrets
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
from werkzeug import secure_filename
import smtplib
import imaplib
import email
import time
from PIL import Image

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
        user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inbox'))
    form = LoginForm()
    if(form.validate_on_submit()):
            user = User.query.filter_by(email = form.email.data).first()
            if user and (user.password == form.password.data):
                login_user(user, remember = form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('inbox'))
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

@app.route("/inbox")
def inbox():
    FROM_EMAIL  = current_user.email
    FROM_PWD    = current_user.password
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT   = 993
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[10])
        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(str(i), "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    email_date = msg["Date"]
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print(email_from + "\n")

    except Exception as e:
        print(e)
    return render_template('inbox.html', title = 'Inbox')


@app.route("/compose")
def compose():
    return render_template('compose.html', title = 'Compose')

@app.route('/emailSent',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(current_user.email, current_user.password)
      if request.method == 'POST':
          f = request.files['file']
          f.save(secure_filename(f.filename))
      msg = MIMEMultipart()
      msg['From'] = current_user.email
      msg['To'] = result['to']
      msg['Subject'] = result['subject']
      body = result['message']
      msg.attach(MIMEText(body, 'plain'))
      filename = f.filename
      attachment = open(f.filename, "rb")
      p = MIMEBase('application', 'octet-stream')
      p.set_payload((attachment).read())
      encoders.encode_base64(p)
      p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
      msg.attach(p)
      message=msg.as_string()
      server.sendmail(current_user.email, result['to'], message)
      server.quit()
      flash('Email has been succesfully sent', 'success')
      return redirect(url_for('inbox'))
