from website import create_app
import os
from os.path import join, dirname
from flask import Blueprint, render_template, Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_caching import Cache

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
#github_bp = make_github_blueprint(scope='read:org',redirect_to='github.authorized')
github_bp = make_github_blueprint(scope='read:org',redirect_url='https://sustainabilityauditingtool.herokuapp.com/connect')
app.register_blueprint(github_bp, url_prefix="/login")

@app.route("/connect")
def connect():
    if not github.authorized:
        return redirect(url_for("github.login"))
    #resp = github.get("/user")
    #resp = github.get("/user/repos")
    #if not cache.get("gh_json",resp.json()):
    #    resp = github.get("/user/memberships/orgs")
    #    assert resp.ok
    #    cache.set("gh_json",resp.json())
    #return "You are @{login} on GitHub".format(login=resp.json()["login"])
    #return render_template("githubauth.html",gh_json=cache.get("gh_json",resp.json()))
    return render_template("githubauth.html")
    
@app.route('/models')
def models():
    num_agents = 55
    uncertainty = 0.55
    reevaluate_rate = 0.55
    unit = 0.55
    horizon = 5.5
    max_noise = 55.0
    sites = ['anatomyofamodel.html','osdcCoOpStripped.html']
    with open('website/static/models/'+sites[0],'r') as file:
        lines = file.readlines()
    #print(lines)
    count = 0
    for line in lines:
        if line.__contains__("-num_agents-"):
            lines[count] = str(num_agents)+'\n'
        if line.__contains__("-uncertainty-"):
            lines[count] = str(uncertainty)+'\n'
        if line.__contains__("-reevaluate_rate-"):
            lines[count] = str(reevaluate_rate)+'\n'
        if line.__contains__("-unit-"):
            lines[count] = str(unit)+'\n'
        if line.__contains__("-horizon-"):
            lines[count] = str(horizon)+'\n'
        if line.__contains__("-max_noise-"):
            lines[count] = str(max_noise)+'\n'
        count += 1
    with open('website/static/models/currentmodel.html', 'w') as file:
        file.writelines(lines)
    return render_template("models.html",gh_json=cache.get("gh_json"))
    
def unused_code():
    entry = 0
    #for org in resp:
    #    members = github.get("/orgs/{org['login']}/members")
    #    #print(members)
    #    cache.set("{mem_count[entry]}",len(members.json()))
    #    entry += 1
    #return render_template("githubauth.html",gh_json=resp.json())

if __name__ == "__main__":
    app.run(debug=True)
