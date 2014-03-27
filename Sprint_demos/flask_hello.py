from flask import Flask, url_for, request
app = Flask(__name__)

@app.route("/")
def hello():
    print "printing request"
    print request
    return "Hello World!"

@app.route('/projects/')
def projects():
    print "printing request"
    print request
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

if __name__ == "__main__":
    app.run()
