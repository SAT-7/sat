#from flask import Flask
#app = Flask(__name__)

#@app.route("/")
#def index():
#    return render_template('basic.html')

from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
