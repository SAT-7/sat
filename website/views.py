from flask import Blueprint, render_template, request, flash, jsonify
import os
from flask import redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

views = Blueprint('views', __name__)

views.secret_key = os.urandom(24)
views.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
views.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
views.register_blueprint(github_bp, url_prefix="/login")

@views.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    #return "You are @{login} on GitHub".format(login=resp.json()["login"])
    #return "{response}".format(response=resp.json())
    return render_template("jsontest.html", gh_json=resp.json())
    
@views.route('/models')
def models():
    return render_template("models.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/login')
def login():
    return render_template("models.html")