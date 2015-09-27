from flask_blog import app

@app.route('/')
def slash():
    return "Hello World!"

@app.route('/index')
def index():
    return "Hello World!"
