import os
from website import create_app
from flask import Flask, request, g, session, redirect, url_for
from flask import render_template_string, jsonify
from flask_github import GitHub

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'sqlite:////github-flask.db'
SECRET_KEY = os.urandom(24)
DEBUG = True

# Set these values
GITHUB_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")

# setup flask
#app = create_app() #this line is necessary to get to the "real site"
app = Flask(__name__)
app.config.from_object(__name__)

# setup github-flask
github = GitHub(app)

# setup sqlalchemy
engine = create_engine(app.config['DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    github_access_token = Column(String(255))
    github_id = Column(Integer)
    github_login = Column(String(255))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

init_db()

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response


@app.route('/')
def index():
    if g.user:
        t = 'Hello! %s <a href="{{ url_for("user") }}">Get user</a> ' \
            '<a href="{{ url_for("repo") }}">Get repo</a> ' \
            '<a href="{{ url_for("logout") }}">Logout</a>'
        t %= g.user.github_login
    else:
        t = 'Hello! <a href="{{ url_for("login") }}">Login</a>'

    return render_template_string(t)


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db_session.add(user)

    user.github_access_token = access_token
    g.user = user

    # Not necessary to get these details here
    # but it helps humans to identify users easily.
    #g.user = user
    #github_user = github.get('/user')
    #user.github_id = github_user['id']
    #user.github_login = github_user['login']

    db_session.commit()

    session['user_id'] = user.id
    return redirect(next_url)


@app.route('/login')
def login():
    redirect_uri="https://sustainabilityauditingtool.herokuapp.com/github-callback"
    if session.get('user_id', None) is None:
        return github.authorize(scope="org,repo,user",redirect_uri=redirect_uri)
    else:
        return 'Already logged in'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# this throws a bad credentials error 401
#@app.route('/user')
#def user():
#    return jsonify(github.get('/user'))

# this works
@app.route('/repo')
def repo():
    return jsonify(github.get('/repos/cenkalti/github-flask'))


if __name__ == '__main__':
    #init_db()
    app.run(debug=True)