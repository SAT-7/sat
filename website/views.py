from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route("/")
def index():
    return 

@views.route('/models')
def models():
    return render_template("models.html")


@views.route('/about')
def about():
    return render_template("about.html")
