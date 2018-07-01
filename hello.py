from flask import Flask

app = Flask(__name__)

# the toolbar is only enabled in debug mode:

@app.route('/')
def hello_world():
    return 'Hello, World!'