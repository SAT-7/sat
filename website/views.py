from flask import Blueprint, render_template, request, flash, jsonify
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("models.html")

@views.route('/models')
def models():
    testval = 55
    with open('website/static/models/anatomyofamodel.html','r') as file:
        lines = file.readlines()
    #print(lines)
    count = 0
    for line in lines:
        if line.__contains__("-num_agents-"):
            lines[count] = str(testval)+'\n'
        count += 1
    with open('website/static/models/currentmodel.html', 'w') as file:
        file.writelines(lines)
    return render_template("models.html")


@views.route('/about')
def about():
    return render_template("about.html")