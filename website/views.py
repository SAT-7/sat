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
    print(lines)
    count = 0
    for line in lines:
        if line.__contains__(str(54)):
            print(str(line) + str(count))
            if line[0] == '5' and line[1] == '4':
                print("fifty four")
                lines[count] = str(55)+'\n'
        count += 1
    with open('website/static/models/anatomyofamodel.html', 'w') as file:
        file.writelines(lines)
    return render_template("models.html")


@views.route('/about')
def about():
    return render_template("about.html")