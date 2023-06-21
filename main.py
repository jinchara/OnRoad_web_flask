import os
from flask import Flask, redirect, url_for, render_template, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from api import temp_tbilisi, temp_kutaisi, temp_batumi
import smtplib
from time import sleep



app = Flask(__name__)
app.config['SECRET_KEY'] = 'onroadpython'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite'
db = SQLAlchemy(app)


class MailBase(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __str__(self):
        return f'Email -  {self.email}'


with app.app_context():
    db.create_all()


@app.route('/')
def home():

    return render_template('index.html', temp_tbilisi=temp_tbilisi(), temp_kutaisi=temp_kutaisi(), temp_batumi=temp_batumi())


@app.route('/tbilisi')
def tbilisi():
    return render_template('tbilisi.html',temp_tbilisi=temp_tbilisi(), temp_kutaisi=temp_kutaisi(), temp_batumi=temp_batumi())


@app.route('/kutaisi')
def kutaisi():
    return render_template('kutaisi.html',temp_tbilisi=temp_tbilisi(), temp_kutaisi=temp_kutaisi(), temp_batumi=temp_batumi())


@app.route('/batumi')
def batumi():
    return render_template('batumi.html',temp_tbilisi=temp_tbilisi(), temp_kutaisi=temp_kutaisi(), temp_batumi=temp_batumi())


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        existing_email = MailBase.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists!', 'error')
        else:
            new_email = MailBase(email=email)
            try:
                db.session.add(new_email)
                db.session.commit()
                flash('Email submitted successfully!', 'success')
                sleep(2)
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash('Error occurred while submitting the email!', 'error')
                print(str(e))

    return render_template('email.html', error=error)


@app.route('/aboutus')
@app.route('/about')
def about_us():
    return render_template('aboutus.html')


@app.route('/contactus', methods=['GET', 'POST'])
@app.route('/contact', methods=['GET', 'POST'])
def contact_us():

    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')

        # Send the email
        sender_email = email
        sender_password = request.form.get('password')
        receiver_email = 'gukajincharadze@gmail.com'

        try:

            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)

            subject = 'Hello My Dear!'
            body = f"Email: {email}\n\nMessage: {message}"
            email_message = f"Subject: {subject}\n\n{body}"
            smtp_server.sendmail(sender_email, receiver_email, email_message)

            smtp_server.quit()
            return redirect(url_for('home'))
        except smtplib.SMTPAuthenticationError:
            return 'Authentication failed. Please check your email and password.'
        except Exception as e:
            return f'An error occured: {str(e)}'

    return render_template('contactus.html')


@app.route('/kutaisi_map')
def download_image_kutaisi():
    image_path = 'static/img/kutaisi-map-0.jpg'
    image_filename = image_path.split('/')[-1]
    return send_from_directory(os.path.dirname(image_path), image_filename, as_attachment=True)


@app.route('/tbilisi_map')
def download_image_tbilisi():
    image_path = 'static/img/tbilisi-map-0.jpg'
    image_filename = image_path.split('/')[-1]
    return send_from_directory(os.path.dirname(image_path), image_filename, as_attachment=True)


@app.route('/batumi_map')
def download_image_batumi():
    image_path = 'static/img/batumi_map.jpg'
    image_filename = image_path.split('/')[-1]
    return send_from_directory(os.path.dirname(image_path), image_filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

