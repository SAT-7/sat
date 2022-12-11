from website import create_app
import os
from os.path import join, dirname
from flask import Blueprint, render_template, Flask, redirect, url_for, request
from flask_dance.contrib.github import make_github_blueprint, github
from flask_caching import Cache
import json

config = {
    "DEBUG": True,
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "cache/",
    "CACHE_DEFAULT_TIMEOUT": 300
}

samp_json = {"login":"Brianna-Adams","id":67566208,"node_id":"MDQ6VXNlcjY3NTY2MjA4","avatar_url":"https://avatars.githubusercontent.com/u/67566208?v=4","gravatar_id":"","url":"https://api.github.com/users/Brianna-Adams","html_url":"https://github.com/Brianna-Adams","followers_url":"https://api.github.com/users/Brianna-Adams/followers","following_url":"https://api.github.com/users/Brianna-Adams/following{/other_user}","gists_url":"https://api.github.com/users/Brianna-Adams/gists{/gist_id}","starred_url":"https://api.github.com/users/Brianna-Adams/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/Brianna-Adams/subscriptions","organizations_url":"https://api.github.com/users/Brianna-Adams/orgs","repos_url":"https://api.github.com/users/Brianna-Adams/repos","events_url":"https://api.github.com/users/Brianna-Adams/events{/privacy}","received_events_url":"https://api.github.com/users/Brianna-Adams/received_events","type":"User","site_admin":false},{"login":"cedwards1012","id":113752853,"node_id":"U_kgDOBse7FQ","avatar_url":"https://avatars.githubusercontent.com/u/113752853?v=4","gravatar_id":"","url":"https://api.github.com/users/cedwards1012","html_url":"https://github.com/cedwards1012","followers_url":"https://api.github.com/users/cedwards1012/followers","following_url":"https://api.github.com/users/cedwards1012/following{/other_user}","gists_url":"https://api.github.com/users/cedwards1012/gists{/gist_id}","starred_url":"https://api.github.com/users/cedwards1012/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/cedwards1012/subscriptions","organizations_url":"https://api.github.com/users/cedwards1012/orgs","repos_url":"https://api.github.com/users/cedwards1012/repos","events_url":"https://api.github.com/users/cedwards1012/events{/privacy}","received_events_url":"https://api.github.com/users/cedwards1012/received_events","type":"User","site_admin":false},{"login":"Hussnain-Azhar","id":104384831,"node_id":"U_kgDOBjjJPw","avatar_url":"https://avatars.githubusercontent.com/u/104384831?v=4","gravatar_id":"","url":"https://api.github.com/users/Hussnain-Azhar","html_url":"https://github.com/Hussnain-Azhar","followers_url":"https://api.github.com/users/Hussnain-Azhar/followers","following_url":"https://api.github.com/users/Hussnain-Azhar/following{/other_user}","gists_url":"https://api.github.com/users/Hussnain-Azhar/gists{/gist_id}","starred_url":"https://api.github.com/users/Hussnain-Azhar/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/Hussnain-Azhar/subscriptions","organizations_url":"https://api.github.com/users/Hussnain-Azhar/orgs","repos_url":"https://api.github.com/users/Hussnain-Azhar/repos","events_url":"https://api.github.com/users/Hussnain-Azhar/events{/privacy}","received_events_url":"https://api.github.com/users/Hussnain-Azhar/received_events","type":"User","site_admin":false},{"login":"JohnBurneson","id":89563180,"node_id":"MDQ6VXNlcjg5NTYzMTgw","avatar_url":"https://avatars.githubusercontent.com/u/89563180?v=4","gravatar_id":"","url":"https://api.github.com/users/JohnBurneson","html_url":"https://github.com/JohnBurneson","followers_url":"https://api.github.com/users/JohnBurneson/followers","following_url":"https://api.github.com/users/JohnBurneson/following{/other_user}","gists_url":"https://api.github.com/users/JohnBurneson/gists{/gist_id}","starred_url":"https://api.github.com/users/JohnBurneson/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/JohnBurneson/subscriptions","organizations_url":"https://api.github.com/users/JohnBurneson/orgs","repos_url":"https://api.github.com/users/JohnBurneson/repos","events_url":"https://api.github.com/users/JohnBurneson/events{/privacy}","received_events_url":"https://api.github.com/users/JohnBurneson/received_events","type":"User","site_admin":false},{"login":"whatcoloris","id":7896287,"node_id":"MDQ6VXNlcjc4OTYyODc=","avatar_url":"https://avatars.githubusercontent.com/u/7896287?v=4","gravatar_id":"","url":"https://api.github.com/users/whatcoloris","html_url":"https://github.com/whatcoloris","followers_url":"https://api.github.com/users/whatcoloris/followers","following_url":"https://api.github.com/users/whatcoloris/following{/other_user}","gists_url":"https://api.github.com/users/whatcoloris/gists{/gist_id}","starred_url":"https://api.github.com/users/whatcoloris/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/whatcoloris/subscriptions","organizations_url":"https://api.github.com/users/whatcoloris/orgs","repos_url":"https://api.github.com/users/whatcoloris/repos","events_url":"https://api.github.com/users/whatcoloris/events{/privacy}","received_events_url":"https://api.github.com/users/whatcoloris/received_events","type":"User","site_admin":false}

app = create_app()

app.config.from_mapping(config)
cache = Cache(app)

app.secret_key = os.urandom(24)
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
#github_bp = make_github_blueprint(scope='read:org',redirect_to='github.authorized')
github_bp = make_github_blueprint(scope='read:org,read:user',redirect_url='https://sustainabilityauditingtool.herokuapp.com/connect')
app.register_blueprint(github_bp, url_prefix="/login")

@app.route("/connect")
def connect():
    #if not github.authorized:
    #    return redirect(url_for("github.login"))
    #resp = github.get("/user")
    #resp = github.get("/user/repos")
    #resp = github.get("/user/memberships/orgs")
    #assert resp.ok
    #cache.set("gh_json",resp.json())
    #return "You are @{login} on GitHub".format(login=resp.json()["login"])
    #return render_template("githubauth.html",gh_json=cache.get("gh_json",resp.json()))
    return render_template("githubauth.html",gh_json=samp_json)

@app.route("/repo")
def repo():
    return render_template("repochoose.html",gh_json=cache.get("gh_json"))
    
@app.route('/models',methods = ['POST', 'GET'])
def models():
    #if request.method == 'POST':
    #    chosen_org = request.form['orgform']
    #    cache.set("cached_org",chosen_org)
    #else:
    #    chosen_org = request.args.get('orgform')
    #    cache.set("cached_org",chosen_org)
    num_agents = 55
    #org_json = cache.get("gh_json")
    #chosen_org = "SAT-7"
    #if cache.get("cached_org"):
    #    chosen_org = cache.get("cached_org")
    #members_resp = github.get("/orgs/SAT-7/members")
    #assert members_resp.ok
    #members = json.loads(members_resp.json(), separators=(',', ':'))
    members = samp_json
    if len(members) > 0:
        num_agents = len(members)
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
    return render_template("models.html",gh_json=members)
    
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
