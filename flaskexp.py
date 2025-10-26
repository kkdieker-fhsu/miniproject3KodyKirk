#starting with the flask tutorial to get familiar with it

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello World!</p>'