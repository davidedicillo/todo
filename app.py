from os import environ

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	todo_text = db.Column(db.String(100), index = True)

class TodoForm(FlaskForm):
	todo = StringField("Todo")
	submit = SubmitField("Add")

db.create_all()

@app.route('/', methods=["GET", "POST"])
def index():
	if 'todo' in request.form:
		db.session.add(Todo(todo_text=request.form['todo']))
		try:
			db.session.commit()
		except:
			db.session.rollback()
	return render_template('index.html', template_todos=Todo.query.all(), template_form=TodoForm())
	
	
@app.route('/<int:id>/delete', methods=["GET", "POST"])
def delete(id):
	db.session.delete(Todo.query.get(id))
	db.session.commit()
	return redirect(url_for('index'))