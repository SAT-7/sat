from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template("homepage.html") 

@views.route('/home')
def homepage():
  return render_template("homepage.html") 

@views.route('/about')
def about():
    return render_template("base.html")