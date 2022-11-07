from flask import Blueprint, render_template, request, flash, jsonify
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("models.html")

@views.route('/models')
def models():
    return render_template("models.html")

@views.route('/compare')
def compare():
    return render_template("compare.html")

@views.route('/about')
def about():
    return render_template("about.html")