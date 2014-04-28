import os
from flask import render_template, Flask, request, redirect, url_for, jsonify, send_file, g, make_response
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.base import Admin
from flask.ext.admin.contrib import sqla
from datetime import datetime
import time

app = Flask(__name__)
app.config.from_object('config')
server_root = app.config['UPLOAD_FOLDER']
db = SQLAlchemy(app)
db.create_all()
lm = LoginManager()
lm.init_app(app)

class SavedFile(db.Model):
    __tablename__ = "files"
    file_id = db.Column('file_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), index=True)
    filename = db.Column('filename', db.String(20))
    modified_at = db.Column('modified_at', db.Float)
    admin_deleted = db.Column('admin_deleted', db.Boolean)
    
    def __init__(self, username, filename, modified_at):
        self.username = username
        self.filename = filename
        self.modified_at = modified_at
        self.admin_deleted = False

    def is_deleted(self):
        return self.admin_deleted
    
    def get_id(self):
        return unicode(self.file_id)

    def user_upload(self, compare_time):
        return str(compare_time) > str(self.modified_at)

    def user_download(self, compare_time):
        return str(compare_time) < str(self.modified_at)

    def __repr__(self):
        return '<SavedFile %r>' % self.filename

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
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
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@lm.request_loader
def load_user_from_request(req):
    if 'username' in req.args:
        username = req.args['username']
        return User.query.filter_by(username=username).first()
    else:
        return User.query.filter_by(username='admin').first()
        
@app.before_request
def before_request():
    g.user = current_user

@app.route('/main', methods=['GET', 'POST', 'DELETE'])
def sync_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        old_entry = SavedFile.query.filter_by(username=request.args['username'], filename=filename).first()
        if old_entry is None:
            new_file = SavedFile(request.args['username'], filename, request.args['modified_at'])
            db.session.add(new_file)
        else:
            old_entry.modified_at = request.args['modified_at'] 
        db.session.commit()
        save_dir = server_root + g.user.username + '/'
        file.save(os.path.join(save_dir, filename))
        return make_response()
    if request.method == 'DELETE':
        filename = request.args['file']
        old_entry = SavedFile.query.filter_by(username=str(request.args['username']), filename=str(filename)).first()
        if old_entry is not None:
            db.session.delete(old_entry)
            db.session.commit()
        save_dir = server_root + g.user.username + '/'
        os.remove(os.path.join(save_dir, filename))
        return make_response()
    if request.method == 'GET':
        save_dir = server_root + g.user.username + '/'
        filename = os.path.join(save_dir, request.args['file'])
        resp = send_file(filename, as_attachment=True)
        return resp

@app.route('/query', methods=['GET'])
def respond_requests():
    if request.method == 'GET':
        file_info = request.args
        username = file_info['username']
        save_dir = server_root + g.user.username + '/'
        server_files = os.listdir(save_dir)
        uploadneed = []
        downloadneed = []
        deleteneed = []
        for each in file_info:
            if each == 'username' or each == 'modified_at':
                continue
            found_file = SavedFile.query.filter_by(username=username, filename=each).first()
            if found_file is None:
                uploadneed.append(each)
            else:
                if found_file.user_upload(file_info[each]):
                    uploadneed.append(each)
                if found_file.user_download(file_info[each]):
                    downloadneed.append(each)
        for each in server_files:
            if not each in file_info:
                downloadneed.append(each)
        current_table = SavedFile.query.filter_by(username=username).all()
        for each in current_table:
            if each.is_deleted():
                deleteneed.append(each.filename)
                db.session.delete(each)
        db.session.commit()
        resp = jsonify(upload=uploadneed, download=downloadneed, delete=deleteneed)
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

@app.route('/change_password', methods=['POST'])
def changepassword():
    orig_user = User.query.filter_by(username=request.args['username']).first()
    orig_user.password = request.args['password']
    db.session.commit()
    resp = jsonify(success=True)
    return resp

@app.route('/login', methods=['POST'])
def login():
    username = request.args['username']
    password = request.args['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        resp = jsonify(success=False)
        return resp
    login_user(registered_user, remember=True)
    resp = jsonify(success=True)
    return resp

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    #logout_user()
    resp = jsonify(success=True)
    return resp

if __name__ == '__main__':
    admin = Admin(app, 'OneDir')
    admin.add_view(sqla.ModelView(User, db.session))
    admin.add_view(sqla.ModelView(SavedFile, db.session))
    # app.debug = True
    # app.run()
    app.run(host='0.0.0.0')
