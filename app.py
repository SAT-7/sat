from website import create_app
import os
from os.path import join, dirname
from flask import Blueprint, render_template, Flask, redirect, url_for, request
from flask_dance.contrib.github import make_github_blueprint, github
from flask_caching import Cache
import json

# configuration for cache
config = {
    "DEBUG": True,
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "cache/",
    "CACHE_DEFAULT_TIMEOUT": 300
}

# create the app, see __init__.py
app = create_app()

# using the cache config, tie it to app and instantiate cache object
app.config.from_mapping(config)
cache = Cache(app)

# create secret values and blueprint
app.secret_key = os.urandom(24)
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
#github_bp = make_github_blueprint(scope='read:org',redirect_to='github.authorized')
# note that we need both org and user scopes, in order to read orgs and see their members
github_bp = make_github_blueprint(scope='read:org,read:user',authorized_url="http://sustainabilityauditingtool.herokuapp.com/login/github/authorized",login_url="https://sustainabilityauditingtool.herokuapp.com/login/github",redirect_url="https://sustainabilityauditingtool.herokuapp.com/connect")
app.register_blueprint(github_bp, url_prefix="/login")

# connect is the page through which the oauth is performed
@app.route("/connect")
def connect():
    # if github is not already authorized, go to the login page
    if not github.authorized:
        return redirect(url_for("github.login"))
    # get json from the github api for the authenticated user
    resp = github.get("/user/memberships/orgs")
    # make sure it came through right
    assert resp.ok
    # stick the json in the cache for later
    cache.set("gh_json",resp.json())
    return render_template("githubauth.html",gh_json=resp.json())

# later function for choosing a repo once an organization has been chosen
@app.route("/repo")
def repo():
    return render_template("repochoose.html",gh_json=cache.get("gh_json"))

# models is the main page, fed by a get request for initial values    
@app.route('/models',methods = ['POST', 'GET'])
def models():
    # get the organization from githubauth template html
    if request.method == 'POST':
        chosen_org = request.form['orgform']
        cache.set("cached_org",chosen_org)
    else:
        chosen_org = request.args.get('orgform')
        cache.set("cached_org",chosen_org)

    num_agents = 5
    chosen_org = "SAT-7"
    if cache.get("cached_org"):
        chosen_org = cache.get("cached_org")

    members_resp = github.get("/orgs/SAT-7/members")
    assert members_resp.ok
    members = json.dumps(members_resp.json(), separators=(',', ':'))

    if len(members) > 0:
        num_agents = len(members)

    write_new_html(0)
    write_new_html(1,filename="comparemodel")
    return render_template("models.html",gh_json=members)

# helper function to inject variables into Netlogo model HTML    
def write_new_html(site,num_agents=5,filename="currentmodel"):
    uncertainty = 0.55
    reevaluate_rate = 0.55
    unit = 0.55
    horizon = 5.5
    max_noise = 55.0
    sites = ['anatomyofamodel.html','osdcCoOpStripped.html']
    with open('website/static/models/'+sites[site],'r') as file:
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
    with open('website/static/models/'+filename+'.html', 'w') as file:
        file.writelines(lines)

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
