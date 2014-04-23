import os
from flask import Flask, request, redirect, url_for, jsonify, send_file, g
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')
server_root = app.config['UPLOAD_FOLDER']
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer)
    username = db.Column('username', db.String(20), primary_key=True, unique=True, index=True)
    password = db.Column('password', db.String(10))
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        print unicode(self.id)
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

@lm.user_loader
def load_user(id):
    print "here in lm.user_loader"
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/main', methods=['GET', 'POST', 'DELETE'])
def sync_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        print os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response()
    if request.method == 'DELETE':
        filename = request.args['file']
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response()
    if request.method == 'GET':
        filename = os.path.join(app.config['UPLOAD_FOLDER'], request.args['file'])
        resp = send_file(filename, as_attachment=True)
        return resp

@app.route('/query', methods=['GET'])
def respond_requests():
    if request.method == 'GET':
        file_info = request.args
        server_files = os.listdir(app.config['UPLOAD_FOLDER'])
        server_info = {}
        for each in server_files:
            server_info[each] = os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], each))
        uploadneed = []
        downloadneed = []
        for each in file_info:
            if not each in server_info:
                uploadneed.append(each)
            else:
                if server_info[each] > file_info[each]:
                    downloadneed.append(each)
                else:
                    uploadneed.append(each)
        for each in server_info:
            if not each in file_info:
                downloadneed.append(each)
        resp = jsonify(upload=uploadneed, download=downloadneed)
        return resp

@app.route('/register', methods=['POST'])
def register():
    username_entered = request.args['username']
    user = User(username_entered, request.args['password'])
    db.session.add(user)
    db.session.commit()
    user_path = server_root + username_entered + '/'
    if not os.path.exists(user_path):
        os.makedirs(user_path)
        resp = jsonify(success=True)
        return resp
    else:
        resp = jsonify(success=False)
        return resp

@app.route('/login', methods=['POST'])
def login():
    username = request.args['username']
    password = request.args['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        resp = jsonify(success=False)
        return resp
    login_user(registered_user)
    app.config['UPLOAD_FOLDER'] = server_root + username + '/'
    resp = jsonify(success=True)
    return resp

@app.route('/logout')
def logout():
    logout_user()
    app.config['UPLOAD_FOLDER'] = server_root
    resp = jsonify(success=True)
    return resp

if __name__ == '__main__':
    app.run()
