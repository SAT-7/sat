from flask import Blueprint, render_template, request, flash, jsonify
import json

views = Blueprint('views', __name__)

#@views.route('/')
#def home():
#    return render_template("models.html")

@views.route('/models')
def models():
    return render_template("models.html")


@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/login/github/authorized')
def login():
    return render_template("models.html")