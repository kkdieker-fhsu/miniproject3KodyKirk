#starting with the flask tutorial to get familiar with it

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Home page</h1>'
@app.route('/hello')
def hello_world():
    return '<p>Hello World!</p>'
