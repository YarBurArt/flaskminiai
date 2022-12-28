from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from transformers import pipeline
from werkzeug.security import check_password_hash, generate_password_hash

from logic import app, db
from logic.models import Message, User

gpt_messages = '...'
text_generation = pipeline("text-generation")


def new_text(old_text):
    return text_generation(old_text, max_length=30, do_sample=False)[0]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/main')
@login_required
def main():
    return render_template("main.html", messages=Message.query.all())


@app.route('/add_message', methods=['POST'])
@login_required
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    db.session.add(Message(text, tag))
    db.session.commit()

    return redirect(url_for('main'))


@app.route('/return_ai')
@login_required
def return_ai():
    return render_template('return_ai.html', tex=gpt_messages)


@app.route('/return_ai_text', methods=['POST'])
@login_required
def return_ai_text():
    global gpt_messages

    text = request.form['text']
    gpt_messages = new_text(text)

    return redirect(url_for('return_ai'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please fill login and password and retype password')
        elif password != password2:
            flash('Passwords are not equal')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_singin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response
