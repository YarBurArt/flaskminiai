from collections import namedtuple

from transformers import pipeline
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://drevo:123@localhost/drevo'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)

    def __init__(self, text, tags):
        self.text = text.strip()
        self.tags = [
            Tag(text=tag.strip()) for tag in tags.split(',')
        ]

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tags', lazy=True))

with app.app_context():
    db.create_all()

gpt_messages = '...'

text_generation = pipeline("text-generation")

def new_text(old_text):
    return text_generation(old_text, max_length=30, do_sample=False)[0]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template("main.html", messages=Message.query.all())

@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    db.session.add(Message(text, tag))
    db.session.commit()

    return redirect(url_for('main'))

@app.route('/return_ai')
def return_ai():
    return render_template('return_ai.html', tex=gpt_messages)

@app.route('/return_ai_text', methods=['POST'])
def return_ai_text():
    global gpt_messages

    text = request.form['text']
    gpt_messages = new_text(text)

    return redirect(url_for('return_ai'))
