from flask import Blueprint, render_template, request, flash, jsonify
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template("homepage.html") 

@views.route('/login') 
def github1():
    return render_template("githubauth.html") 

@views.route('/about')
def about():
    return render_template("base.html")

@views.route('/models')
def models():
   return render_template("models.html")