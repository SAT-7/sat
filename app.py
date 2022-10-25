#from flask import Flask, render_template
#app = Flask(__name__)

#@app.route("/")
#def index():
#    return render_template('basic.html')

#if __name__ == "__main__":
#    app.run(debug=True, use_reloader=True)

try:
    from flask import Flask,render_template,url_for,request,redirect, make_response
    import random
    import json
    from time import time
    from random import random
    from flask import Flask, render_template, make_response
    from flask_dance.contrib.github import make_github_blueprint, github
except Exception as e:
    print("Some Modules are Missings {}".format(e))


app = Flask(__name__)
app.config["SECRET_KEY"]="thisisasecret"

github_blueprint = make_github_blueprint(client_id='2637ef304e72336e70dd',
                                         client_secret='a032a8f9997e0b9a5f73744362a34e637a65022f')

app.register_blueprint(github_blueprint, url_prefix='/github_login')


@app.route('/')
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            return '<h1>Your Github name is {}'.format(account_info_json['login'])

    return '<h1>Request failed!</h1>'


if __name__ == "__main__":
    app.run(debug=True)

