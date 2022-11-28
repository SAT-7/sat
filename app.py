from website import create_app
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Blueprint, render_template, Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_caching import Cache

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

config = {
    "DEBUG": True,
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "cache/",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = create_app()

app.config.from_mapping(config)
cache = Cache(app)

app.secret_key = os.urandom(24)
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint(scope='read:org')
app.register_blueprint(github_bp, url_prefix="/login")

@app.route("/connect")
def connect():
    if not github.authorized:
        return redirect(url_for("github.login"))
    #resp = github.get("/user")
    #resp = github.get("/user/repos")
    resp = github.get("/user/memberships/orgs")
    assert resp.ok
    cache.set("gh_json",resp.json())
    #return "You are @{login} on GitHub".format(login=resp.json()["login"])
    return render_template("githubauth.html",gh_json=resp.json())


@app.route('/models')
def models():
   return render_template("models.html",gh_json=cache.get("gh_json"))
    
if __name__ == "__main__":
    app.run(debug=True)
