#import flask library making code available to the rest of the app
from flask import Flask, request, jsonify, render_template
#flask provides with jsonify function to convert lists and dict to JSON 
from flask_cors import CORS

#creates the Flask app object, contains data about the app and methods (object functions)
#functions tell the app to do certain actions
app = Flask(__name__)
CORS(app)

#starts the debugger -- if code is malformed an error will appear
app.config["DEBUG"] = True

#ask for int user input
@app.route('/')
def ask_user():
    num = input('Enter a value:')
    print(num)
    return "<h1>que dise</p>"

#ask for int user input
@app.route('/hola')
def hola():
    return render_template("w3template.html")


#method to do the action of run the app/ this runs the app server
app.run()
